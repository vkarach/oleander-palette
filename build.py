import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "palette.json")
TEMPLATE = os.path.join(ROOT, "template.html")
OUT = os.path.join(ROOT, "docs", "index.html")

palette = json.load(open(SRC, encoding="utf-8"))
payload = json.dumps(palette, ensure_ascii=False).replace("</", "<\\/")

html = open(TEMPLATE, encoding="utf-8").read().replace("__DATA__", payload)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8", newline="\n").write(html)

count = sum(len(g["colors"]) for g in palette["groups"])
print(f"wrote {OUT} | {count} colors")
