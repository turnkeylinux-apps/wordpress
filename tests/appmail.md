# Live app email acceptance

Run `appmail-e2e.py` from a trusted controller against a disposable WordPress
appliance already connected to the Hub. The appliance uses its normal system
mail path. The test requires a controlled administrator mailbox and a Maildir
receiver accessible over SSH.

The controller submits a plain test message, creates a temporary WordPress user,
requests registration and password-reset messages, and waits for the actual
recipient copies. It then validates the received reset key, authenticates with
the new password, rejects replay and removes its temporary user. SES message IDs
must match the relay's provider-acceptance records.

Write a private configuration file with these fields:

```json
{
  "appliance_ssh": ["ssh", "wordpress-qa"],
  "receiver_ssh": ["ssh", "mail-receiver-qa"],
  "relay_ssh": ["ssh", "relay-qa"],
  "maildir": "/var/lib/qa-mail/Maildir/new",
  "recipient_pattern": "qa+{run}@example.org",
  "admin_recipient": "qa+admin@example.org",
  "app_acceptance_script": "/absolute/path/to/tests/appmail.php"
}
```

The SSH accounts need the corresponding `sudo` permissions. Set the fixture's
WordPress administrator email to `admin_recipient` before running; the test
refuses a different destination. Use a unique recipient pattern in a mailbox
you control.

```sh
python3 tests/appmail-e2e.py --config /private/appmail-qa.json \
    --output /private/appmail-results
```

Results and received messages are private because the messages contain live
reset credentials. Keep the output directory private and remove it after the
reviewed evidence has been retained. A separate automated browser pass should
open an actual received link and inspect its success state. SES event reporting
should independently correlate delivery, bounce and complaint outcomes; the
controller's receipt proof and relay acceptance records establish different
points in delivery.

The generic integration lives in the inithooks `turnkey-mail` helper and Hub
relay. This directory contains only WordPress acceptance code; it adds no SMTP
plugin or application runtime change.
