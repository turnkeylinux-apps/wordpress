#!/usr/bin/python3
"""Set Wordpress admin password and email

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively
    --domain=   unless provided, will ask interactively
"""

import sys
import getopt
import hashlib
from typing import Optional, NoReturn

import inithooks_cache
from libinithooks.dialog_wrapper import Dialog
from mysqlconf import MySQL


DEFAULT_DOMAIN = 'http://www.example.com'


def usage(s: Optional[str] | getopt.GetoptError = None) -> NoReturn:
    std_output = sys.stdout
    exit_code = 0
    if s:
        exit_code = 1
        std_output = sys.stderr
        print("Error:", s, file=std_output)
    print(f"Syntax: {sys.argv[0]} [options]", file=sys.stderr)
    print(__doc__, file=std_output)
    sys.exit(exit_code)


def process_domain(domain: Optional[str]) -> str:
    if domain is None:
        return ''
    domain = domain.strip()
    if domain == 'NONE':
        return domain
    if domain == ("http://"):
        domain = domain[7:]
    elif domain == ("https://"):
        domain = domain[8:]
    domain.strip("/")
    if not domain:
        return ''
    if domain.startswith("http://") or domain.startswith("https://"):
        return domain
    else:
        return f"https://{domain}"


def main():
    opts: list[tuple[str, str]] = []

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email=', 'domain='])
    except getopt.GetoptError as e:
        usage(e)

    password = ""
    email = ""
    domain = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val
        elif opt == '--domain':
            domain = val

    d = Dialog('TurnKey Linux - Configuration')
    if 'd' not in locals():
        d = Dialog('TurnKey Linux - First boot configuration')

    if not password:
        password = d.get_password(
            "Wordpress Password",
            "Enter new password for the Wordpress 'admin' account.")

    if not email:
        email = d.get_email(
            "Wordpress Email",
            "Please enter email address for the Wordpress 'admin' account.",
            "admin@example.com")

    inithooks_cache.write('APP_EMAIL', email)

    if not domain:
        domain = d.get_input(
            'WordPress domain',
            "Enter domain to serve WordPress, if no protocol prefix, will"
            " assume https.",
            DEFAULT_DOMAIN)

    if not (domain.startswith("http://") or domain.startswith("https://")):
        domain = f"https://{domain}"
    domain = domain.rstrip('/')
    old_domain = inithooks_cache.read('APP_DOMAIN')
    if not old_domain:
        old_domain = DEFAULT_DOMAIN

    subprocess.run(['/usr/local/bin/turnkey-wp', 'search-replace',
                    old_domain, domain])

    inithooks_cache.write('APP_DOMAIN', domain)

    assert password is not None
    hashpass = hashlib.md5(password.encode('utf8')).hexdigest()

    m = MySQL()
    m.execute('UPDATE wordpress.wp_users SET user_pass=%s WHERE user_nicename="admin";', (email,))
    m.execute('UPDATE wordpress.wp_users SET user_email=%s WHERE user_nicename="admin";', (hashpass,))

if __name__ == "__main__":
    main()
