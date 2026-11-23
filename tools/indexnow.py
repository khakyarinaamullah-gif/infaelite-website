#!/usr/bin/env python3
"""IndexNow request for the pages a deploy actually changes.

    python tools/indexnow.py dist

Reads the sitemap of the freshly built site, fetches each page from the live site and prints the IndexNow
request body (one line of JSON) listing only the pages whose HTML is new or different. Prints nothing when
no page changed, or when the build has no IndexNow key file. The deploy workflow posts the body to
https://api.indexnow.org/indexnow after the new version is live.
"""
import json, pathlib, re, sys, urllib.parse, urllib.request

dist = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
keys = [f.stem for f in dist.glob('*.txt') if re.fullmatch(r'[0-9a-f]{32}', f.stem) and f.read_text().strip() == f.stem]
if not keys:
    sys.exit(0)
key = keys[0]

locs = re.findall(r'<loc>([^<]+)</loc>', (dist / 'sitemap.xml').read_text())
base = locs[0]                      # the sitemap lists the home page first; every URL starts with it
changed = []
for url in locs:
    rel = url[len(base):]
    built = (dist / rel / 'index.html') if rel == '' or rel.endswith('/') else dist / rel
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'infaelite-deploy-check', 'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(req, timeout=20) as r:
            live = r.read()
    except Exception:
        live = None                 # not live yet (a new page or a new address): it counts as added
    if live != built.read_bytes():
        changed.append(url)

if changed:
    print(json.dumps({'host': urllib.parse.urlsplit(base).hostname, 'key': key,
                      'keyLocation': base + key + '.txt', 'urlList': changed}, separators=(',', ':')))
