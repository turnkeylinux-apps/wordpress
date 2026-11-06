#!/usr/bin/python3
"""Exercise the installed hook on a disposable fixture without sending mail."""
import os
import subprocess
import sys

sys.path.insert(0, '/usr/lib/inithooks/bin')
from mysqlconf import MySQL
from libinithooks import inithooks_cache


def wp(*args):
    return subprocess.check_output(['turnkey-wp', *args], text=True).strip()


assert os.geteuid() == 0
password = os.environ['TKL_TEST_APP_PASS']
domain = wp('option', 'get', 'home')
site_before = wp('option', 'get', 'admin_email')
user_before = wp('user', 'get', 'admin', '--field=user_email')
hash_before = wp('eval', 'echo get_user_by("login", "admin")->user_pass;')
cache_before = inithooks_cache.read('APP_EMAIL')
database = MySQL()


def set_site_email(email):
    # Seed test cases directly so setup/cleanup cannot trigger notification mail.
    database.execute('UPDATE wordpress.wp_options SET option_value=%s '
                     'WHERE option_name="admin_email";', (email,))


def configure(email):
    subprocess.run(['/usr/lib/inithooks/bin/wordpress.py', '--pass=' + password,
                    '--email=' + email, '--domain=' + domain], check=True,
                   stdout=subprocess.DEVNULL)
    assert wp('user', 'get', 'admin', '--field=user_email') == email


try:
    set_site_email('admin@example.com')
    configure('initial-admin@example.invalid')
    assert wp('option', 'get', 'admin_email') == 'initial-admin@example.invalid'
    configure('initial-admin@example.invalid')
    assert wp('option', 'get', 'admin_email') == 'initial-admin@example.invalid'
    set_site_email('site-notices@example.invalid')
    configure('new-login@example.invalid')
    assert wp('option', 'get', 'admin_email') == 'site-notices@example.invalid'
finally:
    set_site_email(site_before)
    database.execute('UPDATE wordpress.wp_users SET user_email=%s, user_pass=%s '
                     'WHERE user_nicename="admin";', (user_before, hash_before))
    inithooks_cache.write('APP_EMAIL', cache_before)

print('firstboot factory email, repetition and customized site email preservation: PASS')
