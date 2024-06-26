#!/usr/bin/python3
"""Set Wordpress admin password and email

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively

"""

import sys
import getopt
import inithooks_cache
import hashlib

from libinithooks.dialog_wrapper import Dialog
from mysqlconf import MySQL


def usage(s=None):
    if s:
        print("Error:", s, file=sys.stderr)
    print("Syntax: %s [options]" % sys.argv[0], file=sys.stderr)
    print(__doc__, file=sys.stderr)
    sys.exit(1)


def main():
    opts: list[tuple[str, str]] = []

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email='])
    except getopt.GetoptError as e:
        usage(e)

    password = ""
    email = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "Wordpress Password",
            "Enter new password for the Wordpress 'admin' account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "Wordpress Email",
            "Please enter email address for the Wordpress 'admin' account.",
            "admin@example.com")

    inithooks_cache.write('APP_EMAIL', email)

    assert password is not None
    hashpass = hashlib.md5(password.encode('utf8')).hexdigest()

    m = MySQL()
    m.execute('UPDATE wordpress.wp_users SET user_email=\"%s\" WHERE user_nicename=\"admin\";' % email)
    m.execute('UPDATE wordpress.wp_users SET user_pass=\"%s\" WHERE user_nicename=\"admin\";' % hashpass)


if __name__ == "__main__":
    main()
