"""Stamp a build id into index.html and version.json.

GitHub Pages serves index.html with its own Cache-Control and there is no way to
override it, so a phone can keep showing an old copy long after a push. The page
compares its baked-in build against version.json (fetched no-store) and, if they
differ, reloads itself via a new query string -- a different URL is the one thing
guaranteed to miss the HTTP cache.

Run this before committing any index.html change.
"""
import datetime, io, json, re, sys

build = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

html = io.open("index.html", encoding="utf-8").read()
new, n = re.subn(r'var BUILD = "[^"]*";', 'var BUILD = "%s";' % build, html, count=1)
if not n:
    sys.exit("no `var BUILD = \"...\";` line found in index.html")
io.open("index.html", "w", encoding="utf-8", newline="\n").write(new)
io.open("version.json", "w", encoding="utf-8", newline="\n").write(
    json.dumps({"build": build}, indent=2) + "\n")
print("build", build)
