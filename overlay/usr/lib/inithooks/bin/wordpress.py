#!/usr/bin/python
"""Set Wordpress admin password and email

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively

"""

import sys
import getopt
import hashlib

from dialog_wrapper import Dialog
from mysqlconf import MySQL


def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)


def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    email = ""
    adminuser = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val

    if not adminuser:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        adminuser = d.get_input(
            "Wordpress Admin Username",
            "Please enter a username for your WordPress admin-account. "
            "This is used to access the WordPress Admin Dashboard.",
            "admin")

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "WordPress Password",
            "Enter new password for your WordPress '{0}' account.".format(adminuser))

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "WordPress Email",
            "Please enter email address for your WordPress '{0}' account.".format(adminuser),
            "admin@example.com")
    
    hashpass = hashlib.md5(password).hexdigest()

    m = MySQL()
    m.execute('UPDATE wordpress.wp_users SET user_email=\"%s\" WHERE user_nicename=\"admin\";' % email)
    m.execute('UPDATE wordpress.wp_users SET user_pass=\"%s\" WHERE user_nicename=\"admin\";' % hashpass)

    if adminuser != 'admin':
        m.execute('UPDATE wordpress.wp_users SET user_login=\"%s\" WHERE user_nicename=\"admin\";'
                  % adminuser)

if __name__ == "__main__":
    main()

