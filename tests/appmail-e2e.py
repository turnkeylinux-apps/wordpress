#!/usr/bin/env python3
"""Prove live appliance delivery and an app's received reset credential."""
import argparse
import base64
import email
import email.policy
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import time
from urllib.parse import parse_qs, urlsplit
import uuid


def remote(ssh, command, data=None):
    return subprocess.check_output(ssh + [command], input=data, timeout=90)


def write_private(path, data):
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'wb') as output:
        output.write(data)


def receipts(config):
    script = """import json,base64,pathlib
p=pathlib.Path(%r)
files=sorted(x for x in p.iterdir() if x.is_file())[-100:]
print(json.dumps([base64.b64encode(x.read_bytes()).decode() for x in files]))
""" % config['maildir']
    raw = remote(config['receiver_ssh'], 'sudo python3 -', script.encode())
    result = []
    for value in json.loads(raw):
        content = base64.b64decode(value)
        message = email.message_from_bytes(content, policy=email.policy.default)
        body = message.get_body(preferencelist=('plain',)).get_content() if message.is_multipart() else message.get_content()
        result.append((message, body, content))
    return result


def wait_receipt(config, predicate):
    deadline = time.monotonic() + 150
    while time.monotonic() < deadline:
        found = [item for item in receipts(config) if predicate(item[0], item[1])]
        if found:
            return found[-1]
        time.sleep(2)
    raise AssertionError('Required recipient mailbox evidence did not arrive')


def save_receipt(path, item):
    write_private(path, item[2])
    message_id = str(item[0]['Message-ID']).strip('<>')
    assert message_id.endswith('@email.amazonses.com'), 'Receipt did not identify SES transport'
    return message_id.split('@')[0]


def main(config, output):
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    output.chmod(0o700)
    run_id = uuid.uuid4().hex[:12]
    helper = '/usr/lib/inithooks/bin/turnkey-mail'
    status = json.loads(remote(config['appliance_ssh'], 'sudo ' + helper + ' status --json'))
    assert status['status'] == 'ready' and status['mode'] == 'hub'
    recipient = config['recipient_pattern'].format(run=run_id)
    plain_recipient = config['recipient_pattern'].format(run='plain-' + run_id)
    assert recipient != plain_recipient and '{' not in recipient
    submitted = json.loads(remote(config['appliance_ssh'], 'sudo ' + helper +
        ' test --json --recipient ' + shlex.quote(plain_recipient)))
    assert submitted['status'] == 'queued'
    plain = wait_receipt(config, lambda m, b: plain_recipient in str(m['To']) and
        m['Subject'] == 'TurnKey app email test' and 'appliance' in b)
    ids = [save_receipt(output / 'plain.eml', plain)]

    fixture = {'disposable': True, 'username': 'appmail_qa_' + run_id,
        'recipient': recipient, 'admin_recipient': config['admin_recipient']}
    root = '/var/lib/turnkey-appmail-e2e'
    path = root + '/config.json'
    php_path = root + '/appmail.php'
    remote(config['appliance_ssh'], 'sudo install -d -m 0700 -o www-data -g www-data ' + root)
    script = Path(config['app_acceptance_script']).read_bytes()
    remote(config['appliance_ssh'], 'sudo tee ' + php_path + ' >/dev/null', script)
    remote(config['appliance_ssh'], 'sudo chmod 0644 ' + php_path)

    def configure():
        remote(config['appliance_ssh'], 'sudo tee ' + path + ' >/dev/null', json.dumps(fixture).encode())
        remote(config['appliance_ssh'], 'sudo chown www-data:www-data ' + path + '; sudo chmod 0600 ' + path)

    command = 'sudo turnkey-wp eval-file ' + php_path + ' '
    configure()
    begun = False
    try:
        result = json.loads(remote(config['appliance_ssh'], command + 'begin ' + path))
        begun = True
        assert result['registered'] and result['reset_requested']
        registration = wait_receipt(config, lambda m, b: recipient in str(m['To']) and
            'Login Details' in str(m['Subject']) and fixture['username'] in b)
        notification = wait_receipt(config, lambda m, b: config['admin_recipient'] in str(m['To']) and
            'New User Registration' in str(m['Subject']) and fixture['username'] in b)
        reset = wait_receipt(config, lambda m, b: recipient in str(m['To']) and
            'Password Reset' in str(m['Subject']) and fixture['username'] in b)
        for label, item in [('registration', registration), ('notification', notification), ('reset', reset)]:
            ids.append(save_receipt(output / (label + '.eml'), item))
        links = re.findall(r'https?://[^\s<>]+', reset[1])
        credentials = [parse_qs(urlsplit(link).query) for link in links]
        credentials = [x for x in credentials if x.get('login') == [fixture['username']] and x.get('action') == ['rp']]
        assert len(credentials) == 1 and len(credentials[0].get('key', [])) == 1
        fixture['key'] = credentials[0]['key'][0]
        configure()
        result = json.loads(remote(config['appliance_ssh'], command + 'finish ' + path))
        begun = False
        assert all(result[x] for x in ('received_reset_accepted', 'new_password_authenticated', 'reset_replay_rejected'))
    finally:
        if begun:
            remote(config['appliance_ssh'], command + 'cleanup ' + path)
        remote(config['appliance_ssh'], 'sudo rm -f ' + path)

    query = """import sqlite3,json
c=sqlite3.connect('/var/lib/turnkey-appmail/mail.db')
ids=json.loads(%r)
rows=c.execute('SELECT provider_id,status FROM outcomes WHERE provider_id IN ('+','.join('?' for _ in ids)+')',ids).fetchall()
print(json.dumps(rows))
""" % json.dumps(ids)
    rows = json.loads(remote(config['relay_ssh'], 'sudo python3 -', query.encode()))
    accepted = {row[0] for row in rows if row[1] == 'provider_accepted'}
    assert set(ids) <= accepted, 'Mailbox receipts are missing matching relay provider-acceptance records'
    report = {'status': 'pass', 'run_id': run_id, 'ses_message_ids': ids,
        'checks': ['plain sendmail receipt', 'app registration receipt', 'app administrator notification receipt',
                   'app reset receipt', 'received reset key accepted', 'new password authenticated',
                   'reset replay rejected', 'matching relay provider acceptance']}
    write_private(output / 'result.json', (json.dumps(report, indent=2) + '\n').encode())
    print(json.dumps(report))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    main(json.loads(args.config.read_text()), args.output)
