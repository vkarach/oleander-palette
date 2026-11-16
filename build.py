import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "templates")
DOCS = os.path.join(ROOT, "docs")
PAGES = ["index.html", "details.html", "playground.html"]

palette = json.load(open(os.path.join(ROOT, "palette.json"), encoding="utf-8"))
payload = json.dumps(palette, ensure_ascii=False).replace("</", "<\\/")
style = open(os.path.join(TEMPLATES, "style.css"), encoding="utf-8").read()

os.makedirs(DOCS, exist_ok=True)
for page in PAGES:
    html = open(os.path.join(TEMPLATES, page), encoding="utf-8").read()
    html = html.replace("__STYLE__", style).replace("__DATA__", payload)
    open(os.path.join(DOCS, page), "w", encoding="utf-8", newline="\n").write(html)

count = sum(len(g["colors"]) for g in palette["groups"]) + len(palette["matches"])
print(f"wrote {', '.join(PAGES)} | {count} colors")
