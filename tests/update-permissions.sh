#!/bin/bash
# Run on a disposable initialized fixture after its supervised core update.
set -euo pipefail

test "$(id -u)" -eq 0
turnkey-wp core check-update --format=json | python3 -c '
import json, sys
assert json.load(sys.stdin) == [], "Apply the supported core update before this no-op regression"
'

root=/var/www/wordpress
rewrite=$root/.htaccess
test -f "$rewrite" && test ! -L "$rewrite"
work=$(mktemp -d)
cp -a "$rewrite" "$work/original"
restore() {
    if test -d "$rewrite" && test ! -L "$rewrite"; then
        rmdir "$rewrite"
    else
        rm -f "$rewrite"
    fi
    cp -a "$work/original" "$rewrite"
    rm -rf "$work"
}
trap restore EXIT

printf 'unrelated file\n' >"$work/target"
chmod 0600 "$work/target"
cp -a "$work/target" "$work/target-before"
rm "$rewrite"
ln -s "$work/target" "$rewrite"
if turnkey-wordpress-update >"$work/symlink.log" 2>&1; then
    echo 'updater accepted a symlink rewrite file' >&2
    exit 1
fi
grep -Fq 'must be a regular file or absent' "$work/symlink.log"
cmp "$work/target-before" "$work/target"
test "$(stat -c '%U:%G %a' "$work/target")" = 'root:root 600'

rm "$rewrite"
mkdir "$rewrite"
if turnkey-wordpress-update >"$work/directory.log" 2>&1; then
    echo 'updater accepted a directory as its rewrite file' >&2
    exit 1
fi
grep -Fq 'must be a regular file or absent' "$work/directory.log"
rmdir "$rewrite"

turnkey-wordpress-update
test "$(stat -c '%U:%G %a' "$rewrite")" = 'www-data:www-data 644'
test ! -s "$rewrite"
rm "$rewrite"
cp -a "$work/original" "$rewrite"

before=$(turnkey-wp core version)
turnkey-wordpress-update
test "$(turnkey-wp core version)" = "$before"
cmp "$work/original" "$rewrite"
test "$(stat -c '%U:%G %a' "$rewrite")" = 'www-data:www-data 644'
runuser -u www-data -- test -w "$rewrite"
for path in "$root" "$root/index.php" "$root/wp-config.php"; do
    runuser -u www-data -- test ! -w "$path"
done
test "$(stat -c '%U:%G %a' "$root/wp-config.php")" = 'root:www-data 640'
printf '%s\n' 'rewrite type rejection, missing-file repair and no-op ownership/content preservation: PASS'
