#!/usr/bin/env bash
# Rebuild the site, push source to the `source` branch, and publish only the built
# files (site/) to `main`. Hostinger auto-deploys `main`, so no source files reach the server.
set -euo pipefail
cd "$(dirname "$0")"
python3 build.py
git add -A
git diff --cached --quiet || git commit -m "Rebuild site"
git push origin source
git subtree split --prefix site -b publish-tmp >/dev/null
git push -f origin publish-tmp:main
git branch -D publish-tmp >/dev/null
echo "Published site/ to main (Hostinger auto-deploys it)."
