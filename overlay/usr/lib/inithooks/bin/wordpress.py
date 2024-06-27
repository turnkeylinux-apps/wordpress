#!/usr/bin/python3
"""Set Wordpress admin password and email

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively
    --domain=   optional
                - if not provided, empty string, or 'http://' or 'https://'
                  protocol only (no fqdn), will ask interactively
                - if 'NONE', no domain will be set
                - if string with 'http://' or 'https://' prefix, will assume
                  full url
                - if string with no 'http://' or 'https://' prefix, will assume
                  fqdn and add https protocol prefix
"""

import sys
import getopt
import hashlib
from typing import Optional, NoReturn

import inithooks_cache
from libinithooks.dialog_wrapper import Dialog
from mysqlconf import MySQL

# default interactive value is to set no domain/url in wp-config.php
DEFAULT_DOMAIN = 'NONE'


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

    if domain != 'NONE':
        domain = process_domain(domain)
        while True:
            domain = d.get_input(
                'WordPress domain (optional)',
                "Enter domain to serve, if no protocol prefix, will assume"
                " https. Enter 'NONE' to not set a domain",
                DEFAULT_DOMAIN)
            domain = process_domain(domain)
            if not domain:
                d.error("Domain must be set - or 'NONE'")
            else:
                break

    inithooks_cache.write('APP_DOMAIN', domain)

    assert password is not None
    hashpass = hashlib.md5(password.encode('utf8')).hexdigest()

    m = MySQL()
    m.execute('UPDATE wordpress.wp_users'
              ' SET user_email=\"%s\"'
              ' WHERE user_nicename=\"admin\";' % email)
    m.execute('UPDATE wordpress.wp_users'
              ' SET user_pass=\"%s\"'
              ' WHERE user_nicename=\"admin\";' % hashpass)

    TODO UPDATE_DOMAIN_HERE!


if __name__ == "__main__":
    main()
