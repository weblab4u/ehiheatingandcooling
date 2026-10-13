#!/usr/bin/env bash
# Rebuild the site and publish only the built files (site/) to the `deploy` branch.
# Hostinger deploys from `deploy`, so source files never reach the web server.
set -euo pipefail
cd "$(dirname "$0")"
python3 build.py
git add -A
git diff --cached --quiet || git commit -m "Rebuild site"
git push origin main
git subtree split --prefix site -b deploy-tmp >/dev/null
git push -f origin deploy-tmp:deploy
git branch -D deploy-tmp >/dev/null
echo "Published site/ to the deploy branch."
