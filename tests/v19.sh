#!/bin/bash
set -euo pipefail

result=${TKL_TEST_RESULT:?}
password=${TKL_TEST_APP_PASS:?}
work=/run/tkl-v19-tests/wordpress
base=https://localhost
curl_args=(-kfsS --resolve localhost:443:127.0.0.1)
hook=/usr/lib/inithooks/bin/wordpress.py
mkdir -p "$work"

systemctl --quiet is-active apache2.service mariadb.service multi-user.target
grep -q '\[40wordpress\] successfully completed' /var/log/inithooks.log

# Exercise validation through the real firstboot hook and restore the expected URL.
if "$hook" --pass="$password" --email=admin@example.com \
        --domain=ftp://localhost; then
    echo 'invalid WordPress scheme unexpectedly succeeded' >&2
    exit 1
fi
"$hook" --pass="$password" --email=admin@example.com --domain=localhost
test "$(turnkey-wp option get siteurl)" = https://localhost
"$hook" --pass="$password" --email=admin@example.com --domain=http://localhost
test "$(turnkey-wp option get siteurl)" = http://localhost
"$hook" --pass="$password" --email=admin@example.com --domain=https://localhost
test "$(turnkey-wp option get siteurl)" = https://localhost

# Authenticate as the provisioned administrator.
login_url=$base/wp-login.php
admin_url=$base/wp-admin/
curl "${curl_args[@]}" -c "$work/cookies" "$login_url" >/dev/null
curl "${curl_args[@]}" -L -b "$work/cookies" -c "$work/cookies" \
    --data-urlencode log=admin --data-urlencode "pwd=$password" \
    --data-urlencode wp-submit='Log In' \
    --data-urlencode "redirect_to=$admin_url" \
    --data-urlencode testcookie=1 "$login_url" >"$work/dashboard.html"
grep -Eq 'Dashboard|wp-admin-bar' "$work/dashboard.html"

# Create meaningful state, then prove it and the authenticated session survive restart.
post_id=$(turnkey-wp post create --post_status=publish \
    --post_title='TurnKey v19 acceptance' \
    --post_content='qa-wordpress-persistence' --porcelain)
test -n "$post_id"
test "$(turnkey-wp post get "$post_id" --field=post_content)" = \
    qa-wordpress-persistence

# Configure permalinks through the authenticated settings form. CLI post CRUD
# alone bypasses the rewrite rules needed by public URLs and the block editor.
htaccess=/var/www/wordpress/.htaccess
test "$(stat -c '%U:%G %a' "$htaccess")" = 'www-data:www-data 644'
runuser -u www-data -- test -w "$htaccess"
runuser -u www-data -- test ! -w /var/www/wordpress
printf '\n# TurnKey permalink regression\n' | \
    runuser -u www-data -- tee -a "$htaccess" >/dev/null
curl "${curl_args[@]}" -b "$work/cookies" \
    "${admin_url}options-permalink.php" >"$work/permalink-form.html"
nonce=$(python3 - "$work/permalink-form.html" <<'PY'
import re, sys
page = open(sys.argv[1]).read()
match = re.search(r'name="_wpnonce" value="([^"]+)"', page)
assert match, 'permalink settings nonce missing'
print(match.group(1))
PY
)
curl "${curl_args[@]}" -L -b "$work/cookies" \
    --data-urlencode "_wpnonce=$nonce" \
    --data-urlencode 'selection=/%postname%/' \
    --data-urlencode 'permalink_structure=/%postname%/' \
    "${admin_url}options-permalink.php" >"$work/permalink-saved.html"
grep -Fq 'Permalink structure updated.' "$work/permalink-saved.html"
! grep -Fq 'You should update your .htaccess file now' "$work/permalink-saved.html"
grep -Fq '# TurnKey permalink regression' "$htaccess"
grep -Fq '# BEGIN WordPress' "$htaccess"
post_url=$(turnkey-wp eval "echo get_permalink($post_id);")
curl "${curl_args[@]}" "$post_url" >"$work/pretty-post.html"
grep -Fq qa-wordpress-persistence "$work/pretty-post.html"
curl "${curl_args[@]}" "$base/wp-json/wp/v2/posts/$post_id" \
    >"$work/rest-post.json"
python3 -c 'import json,sys; assert json.load(open(sys.argv[1]))["id"] == int(sys.argv[2])' \
    "$work/rest-post.json" "$post_id"

before=$(turnkey-wp core version)
turnkey-wp core check-update --format=json >"$work/update.json"
python3 -c 'import json,sys; assert isinstance(json.load(open(sys.argv[1])), list)' \
    "$work/update.json"
test "$(turnkey-wp core version)" = "$before"
turnkey-wp core verify-checksums
if runuser -u www-data -- /usr/local/sbin/turnkey-wordpress-update; then
    echo 'non-root WordPress updater unexpectedly succeeded' >&2
    exit 1
fi

test "$(stat -c '%U:%G %a' /var/www/wordpress/wp-config.php)" = \
    'root:www-data 640'
runuser -u www-data -- test ! -w /var/www/wordpress/index.php
runuser -u www-data -- test ! -w /var/www/wordpress/wp-config.php
for dir in uploads cache upgrade plugins themes; do
    marker=/var/www/wordpress/wp-content/$dir/.tkl-v19-write-test
    runuser -u www-data -- touch "$marker"
    runuser -u www-data -- rm "$marker"
done

systemctl restart mariadb.service apache2.service
systemctl --quiet is-active mariadb.service apache2.service
test "$(turnkey-wp post get "$post_id" --field=post_content)" = \
    qa-wordpress-persistence
curl "${curl_args[@]}" -b "$work/cookies" "$admin_url" \
    >"$work/dashboard-after-restart.html"
grep -Eq 'Dashboard|wp-admin-bar' "$work/dashboard-after-restart.html"
curl "${curl_args[@]}" "$base/?p=$post_id" >"$work/post-after-restart.html"
grep -Fq 'qa-wordpress-persistence' "$work/post-after-restart.html"
turnkey-wp post delete "$post_id" --force >/dev/null

! grep -F -- "$password" /var/log/inithooks.log
for key in AUTH_KEY SECURE_AUTH_KEY LOGGED_IN_KEY NONCE_KEY \
        AUTH_SALT SECURE_AUTH_SALT LOGGED_IN_SALT NONCE_SALT; do
    secret=$(/usr/local/bin/wp --allow-root --path=/var/www/wordpress \
        config get "$key")
    test -n "$secret"
    ! grep -F -- "$secret" /var/log/inithooks.log
done

cat >"$result" <<EOF
package_source=official WordPress 7.1 archive pinned by SHA-256
installed_version=$before
runtime_checks=firstboot, domain validation, administrator authentication, permalink settings and public/REST routes, custom rewrite comment preservation, post persistence and authenticated session across restart, updater metadata, core checksums, ownership boundaries, and secret log hygiene
updater_command=turnkey-wp core check-update --format=json; turnkey-wordpress-update as root
updater_result=valid update JSON, installed version unchanged, and non-root updater use fails closed
updater_channel=official WordPress stable release channel
integrity_evidence=WordPress 7.1 archive SHA-256 d1ae02b5ae18428031ffc3943659fa87ab361d827f4aa804adf9276e4dc75df6 plus official per-file core checksums
EOF
