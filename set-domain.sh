#!/usr/bin/env bash
# Point the whole site at a real domain, then rebuild.
# Usage:  bash set-domain.sh https://www.yourdomain.com
set -e
[ -z "$1" ] && { echo "usage: bash set-domain.sh https://www.yourdomain.com"; exit 1; }
NEW="${1%/}"
OLD=$(grep -m1 '^SITE_URL' build.py | sed 's/.*"\(.*\)".*/\1/')
python3 - "$OLD" "$NEW" <<'PY'
import sys,re
old,new=sys.argv[1],sys.argv[2]
s=open('build.py').read()
s=s.replace('SITE_URL = "%s"'%old,'SITE_URL = "%s"'%new,1)
open('build.py','w').write(s)
print("build.py: %s -> %s"%(old,new))
PY
python3 build.py
python3 mkog.py
echo
echo "Rebuilt. Now run:  python3 verify.py"
