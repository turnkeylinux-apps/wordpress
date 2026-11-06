# WordPress feed parsing

WordPress's dashboard news feeds use its bundled SimplePie parser. On the
published v19 image, logging in succeeded while both feed widgets reported
`XML or PCRE extensions not loaded!`. PHP's PCRE extension was present, but
XML, DOM and SimpleXML were absent. The WordPress package plan now includes
Debian's `php-xml` package.

The [WordPress hosting requirements](https://make.wordpress.org/hosting/handbook/server-environment/#php-extensions)
recommend XML support for parsing remote content. Test the feature that uses
an extension, rather than inferring it from a working PHP page or login.

## Regression

Run on an initialized disposable WordPress appliance, with this checkout's
tests readable by `www-data`:

```sh
turnkey-wp eval-file /path/to/tests/rss.php
```

The test uses the installed WordPress parser to read a deterministic RSS feed
and verifies its title, entry and link. It requires no remote feed, database
writes or cache files. The main `tests/v19.sh` suite invokes it before its
other application checks. The published runtime fails this check with the same
missing-extension error shown in the dashboard.

Also inspect the actual dashboard after installing the correction. A feed
retrieval failure can have a separate network cause; record that separately
from parsing failures. A diagnostic package installation establishes the cause
and repair, while replacement acceptance still requires the clean source build
and configured application journey.

## Existing v19 installations

Install the missing package and restart the web runtime as root:

```sh
apt-get update
apt-get install php-xml
systemctl restart apache2
```

Then reload the dashboard and confirm the feeds render. This correction retains
the appliance's existing core ownership and supervised update policy.

## Corrective evidence, 6 November 2026

The exact regression failed on the unchanged published WordPress filesystem
with `XML or PCRE extensions not loaded!` and exit status 1. A diagnostic copy
then installed `php-xml` and restarted Apache. The same regression passed;
XML, DOM and SimpleXML were loaded. APT also updated PHP from 8.4.24 to 8.4.27.
The original failed fixture remains unchanged.

Private logs include package inventories before and after installation,
APT output and both regression results under
`turnkey-release-state/library-qa-20261106/wordpress-xml/`. The separate
permalink correction and this dependency change will receive one combined
clean build and full application gate. That aggregate validation remains
pending; this focused result does not establish replacement-image acceptance.
