"""Baut die zweisprachige Seite (docs/de + docs/en) und zeigt sie lokal an.

    python build_multilingual_site.py            # rendern + Vorschau-Server
    python build_multilingual_site.py --no-serve # nur rendern

Schritte:
  1. `quarto render --profile deutsch` und `--profile english`
  2. fertige Seiten nachbearbeiten (ohne JavaScript):
     - Sprachwahl im Globus-Menü: die Einträge "#sprache-de"/"#sprache-en" aus
       _quarto-deutsch.yml/_quarto-english.yml werden zu Links auf DIESELBE Seite
       in der anderen Sprache (docs/de/... <-> docs/en/...), aktuelle Sprache markiert
     - Knopf „Alle ausklappen“ unten in der Seitenleiste (Kästchen, Wirkung per CSS
       in styles.css)
  3. docs/index.html: leitet je nach Browsersprache auf de/ oder en/ weiter
  4. lokaler Server auf http://localhost:8000/de/

In `quarto preview` fehlt Schritt 2: dort bleiben die Sprachlinks ohne Wirkung und
der Knopf fehlt.
"""
import http.server
import os
import re
import socketserver
import subprocess
import sys
import time
import webbrowser

base_dir = os.path.dirname(os.path.abspath(__file__))
site_dir = os.path.join(base_dir, "docs")
profiles = ["deutsch", "english"]

REDIRECT_HTML = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>Weiterleitung / Redirect</title>
<script>
  var sprache = (navigator.language || "de").slice(0, 2).toLowerCase();
  window.location.replace(sprache === "de" ? "de/" : "en/");
</script>
<noscript><meta http-equiv="refresh" content="0; url=de/"></noscript>
</head>
<body>
<p><a href="de/">Deutsch</a> · <a href="en/">English</a></p>
</body>
</html>
"""

print("\n" + "=" * 50)
print("MULTILINGUAL WEBSITE BUILDER")
print("=" * 50)

# STEP 1: RENDER QUARTO
print(f"\n[STEP 1] Rendering {len(profiles)} language(s)...")
for i, profile in enumerate(profiles, 1):
    print(f"\n  [{i}/{len(profiles)}] Rendering '{profile}'...")
    print("  " + "-" * 40)
    process = subprocess.Popen(
        ["quarto", "render", "--profile", profile],
        cwd=base_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    for line in process.stdout or []:
        print(f"    {line}", end="")
    process.wait()
    print("  " + "-" * 40)
    if process.returncode != 0:
        print(f"  [{i}/{len(profiles)}] '{profile}' - ERROR! Aborting.")
        sys.exit(1)
    print(f"  [{i}/{len(profiles)}] '{profile}' - done.")

# STEP 2: NACHBEARBEITEN
SPRACHEN = {"deutsch": "de", "english": "en"}
SPRACH_LINK = re.compile(r'<a class="dropdown-item" href="[^"]*#sprache-(de|en)">')
KNOPF_TEXT = {"de": ("Alle ausklappen", "Alle einklappen"),
              "en": ("Expand all", "Collapse all")}
# Ende der Seitenleiste: </ul> des Menüs, </div> des Menü-Containers, </nav>
SEITENLEISTE_ENDE = re.compile(r"(\s*</ul>\s*)(</div>\s*</nav>)")


def nachbearbeiten(html, sprache, rel):
    tiefe = rel.count("/")

    def sprach_link(m):
        ziel = m.group(1)
        # relativ, damit es lokal und auf Pages gleich funktioniert; ohne #Anker,
        # die Überschriften-IDs unterscheiden sich zwischen den Sprachen
        href = "../" * (tiefe + 1) + ziel + "/" + rel
        if ziel == sprache:
            return f'<a class="dropdown-item active" aria-current="true" href="{href}">'
        return f'<a class="dropdown-item" href="{href}">'

    html = SPRACH_LINK.sub(sprach_link, html)

    start = html.find('<nav id="quarto-sidebar"')
    if start != -1 and "sidebar-alle-ausklappen" not in html:
        m = SEITENLEISTE_ENDE.search(html, start)
        # nur wenn es überhaupt einklappbare Abschnitte gibt
        if m and "sidebar-section" in html[start:m.end()]:
            auf, zu = KNOPF_TEXT[sprache]
            knopf = ('<label class="sidebar-alle-ausklappen"><input type="checkbox">'
                     f'<span class="auf">\u25bc {auf}</span>'
                     f'<span class="zu">\u25b2 {zu}</span></label>\n    ')
            html = html[:m.end(1)] + knopf + html[m.start(2):]
    return html


print("\n[STEP 2] Nachbearbeiten (Sprachwahl, Knopf „Alle ausklappen“)...")
for profile in profiles:
    sprache = SPRACHEN[profile]
    ordner = os.path.join(site_dir, sprache)
    anzahl = 0
    for root, dirs, files in os.walk(ordner):
        dirs[:] = [d for d in dirs if d != "site_libs"]
        for name in files:
            if not name.endswith(".html"):
                continue
            pfad = os.path.join(root, name)
            rel = os.path.relpath(pfad, ordner).replace(os.sep, "/")
            with open(pfad, encoding="utf-8", newline="") as f:
                alt = f.read()
            neu = nachbearbeiten(alt, sprache, rel)
            if neu != alt:
                with open(pfad, "w", encoding="utf-8", newline="") as f:
                    f.write(neu)
                anzahl += 1
    print(f"  {sprache}/: {anzahl} Seite(n) angepasst")

# STEP 3: ROOT REDIRECT
print("\n[STEP 3] Writing docs/index.html (redirect to de/ or en/)...")
with open(os.path.join(site_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(REDIRECT_HTML)

if "--no-serve" in sys.argv:
    print("\nDone.")
    sys.exit(0)

# STEP 4: START PREVIEW SERVER
PORT = 8000
print("\n[STEP 4] Starting preview server...")
print(f"  > http://localhost:{PORT}/de/")
print("  > Press CTRL+C to stop\n")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=site_dir, **kwargs)


socketserver.TCPServer.allow_reuse_address = True
time.sleep(1)
webbrowser.open(f"http://localhost:{PORT}/de/")
try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\nServer stopped.")
