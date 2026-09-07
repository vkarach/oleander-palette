# -*- coding: utf-8 -*-
"""Pull the live Oleander palette out of Telegram Desktop into the repo.

Copies tdata/Oleander.tdesktop-palette to palette/ (working copy) and drops a
timestamped snapshot in backups/. Override the source with $OLEANDER_PALETTE or argv[1].
"""
import os, sys, shutil, hashlib, datetime

DEFAULT_SRC = os.path.join(
    os.environ.get("APPDATA", os.path.expanduser("~")),
    "Telegram Desktop", "tdata", "Oleander.tdesktop-palette",
)
src = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("OLEANDER_PALETTE", DEFAULT_SRC)
if not os.path.isfile(src):
    sys.exit(f"palette not found: {src}")

root = os.path.dirname(os.path.abspath(__file__))
working = os.path.join(root, "palette", "Oleander.tdesktop-palette")
backups = os.path.join(root, "backups")
os.makedirs(os.path.dirname(working), exist_ok=True)
os.makedirs(backups, exist_ok=True)


def digest(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest() if os.path.isfile(path) else None


if digest(src) == digest(working):
    print("no change:", working)
    sys.exit(0)

shutil.copy2(src, working)
stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
snapshot = os.path.join(backups, f"Oleander-{stamp}.tdesktop-palette")
shutil.copy2(src, snapshot)
print("updated:", working)
print("snapshot:", snapshot)
