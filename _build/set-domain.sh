#!/usr/bin/env bash
# Point the whole site at a real domain, then rebuild and re-check.
# Usage:  bash set-domain.sh https://www.yourdomain.com
set -e
[ -z "$1" ] && { echo "usage: bash set-domain.sh https://www.yourdomain.com"; exit 1; }
cd "$(dirname "$0")"
NEW="${1%/}"
python3 - "$NEW" <<'PY'
import sys, re
new = sys.argv[1]
s = open('build.py').read()
old = re.search(r'SITE_URL = "([^"]+)"', s).group(1)
s = s.replace('SITE_URL = "%s"' % old, 'SITE_URL = "%s"' % new, 1)
open('build.py', 'w').write(s)
print("%s  ->  %s" % (old, new))
PY
python3 build.py
python3 mkog.py
echo
echo "Now run:  python3 verify.py    (it will fail if any URL still points at the old domain)"
