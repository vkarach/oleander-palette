"""One-time bootstrap: recolor a base tdesktop palette toward oleander pink and
factor repeated colors into named constants. Not part of the build; the palette
is maintained by hand after this ran once.

Usage: python tools/recolor.py <base-palette> [target_bg_hex_or_lightness] [out]
"""
import re, sys, os, colorsys, collections

SRC = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("OLEANDER_BASE_PALETTE", "")
if not SRC or not os.path.isfile(SRC):
    sys.exit("base palette not found; pass it as argv[1] or set OLEANDER_BASE_PALETTE")

# Keys that must keep their color: deliberate multi-color sets and brand colors.
KEEP = re.compile(
    r"^(historyPeer\d|msgFile[1-4]Bg|mediaview(Red|Yellow|Green|Blue)|"
    r"mediaviewFile(Red|Yellow|Green|Blue)CornerFg|trayCounterBgMute|"
    r"trayCounter(Bg|Fg)MacInvert|youtubePlayIconBg)")

TARGET_BG = sys.argv[2] if len(sys.argv) > 2 else "4d2b33"  # hex, or a bare lightness like 0.17
if TARGET_BG.startswith("0."):
    TARGET_BG = float(TARGET_BG)
OUT = sys.argv[3] if len(sys.argv) > 3 else "Oleander.tdesktop-palette"
HUE_SHIFT = -13.0     # degrees: maroon (h~5) -> rose (h~352), matches the flowers
SAT_GAIN  = 1.08      # nudge saturation so it reads pink, not brick
LOW = 335.0           # only touch the red/maroon family
HIGH = 25.0

def lightness(hexval, gamma):
    """Raise HLS lightness by L**gamma. Neutrals and full alpha values pass through."""
    r, g, b = (int(hexval[i:i+2], 16) / 255 for i in (0, 2, 4))
    alpha = hexval[6:]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.08:
        return hexval
    l = min(1.0, l ** gamma)
    # lifting lightness makes saturated tones look neon; pull them back toward dusty rose
    s *= max(0.62, min(1.0, 1.0 - 0.9 * (l - 0.33)))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "%02x%02x%02x" % (round(r*255), round(g*255), round(b*255)) + alpha


def lum(hx):
    r, g, b = (int(hx[i:i+2], 16) / 255 for i in (0, 2, 4))
    return colorsys.rgb_to_hls(r, g, b)[1]


def gamma_for(src_hex, target):
    """Exponent mapping the source lightness onto target (a hex color or a raw L)."""
    import math
    dst = target if isinstance(target, float) else lum(target)
    return math.log(dst) / math.log(lum(src_hex))


def shift(hexval):
    """hexval: 6 or 8 hex digits (RGB or RGBA). Returns the recolored string."""
    r, g, b = (int(hexval[i:i+2], 16) / 255 for i in (0, 2, 4))
    alpha = hexval[6:]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    hd = h * 360
    if s < 0.08:                                   # neutral, leave alone
        return hexval
    if not (hd >= LOW or hd <= HIGH):              # green / blue / purple, leave alone
        return hexval
    hd = (hd + HUE_SHIFT) % 360
    s = min(1.0, s * SAT_GAIN)
    r, g, b = colorsys.hsv_to_rgb(hd / 360, s, v)
    return "%02x%02x%02x" % (round(r*255), round(g*255), round(b*255)) + alpha

line_re = re.compile(r"^(\w+):\s*(#([0-9a-fA-F]{6,8})|\w+);(.*)$")

GAMMA = gamma_for(shift("261614"), TARGET_BG)   # anchor: windowBg
print(f"lightness gamma = {GAMMA:.3f}")

src = open(SRC, encoding="utf-8").read().splitlines()
rows, header = [], []
for ln in src:
    m = line_re.match(ln)
    if not m:
        header.append(ln)
        continue
    key, raw, hexval, comment = m.group(1), m.group(2), m.group(3), m.group(4)
    if hexval and not KEEP.match(key):
        raw = "#" + lightness(shift(hexval), GAMMA)
    rows.append([key, raw, comment])

# ---- factor the most repeated colors into named constants -------------------
counts = collections.Counter(v for _, v, _ in rows if v.startswith("#"))
NAMES = {}   # value -> constant name, seeded from the semantically meaningful keys
SEED = [
    ("windowBg",            "OLEANDER_BG"),
    ("sideBarBg",           "OLEANDER_BG_DEEP"),
    ("windowBgOver",        "OLEANDER_BG_OVER"),
    ("windowBgRipple",      "OLEANDER_BG_RIPPLE"),
    ("titleBgActive",       "OLEANDER_BG_PANEL"),
    ("windowBgActive",      "OLEANDER_ACCENT"),
    ("activeButtonBg",      "OLEANDER_ACCENT_DEEP"),
    ("windowActiveTextFg",  "OLEANDER_ACCENT_LIGHT"),
    ("windowFg",            "OLEANDER_TEXT"),
    ("contactsStatusFg",    "OLEANDER_TEXT_SUB"),
    ("msgInBg",             "OLEANDER_BUBBLE_IN"),
    ("msgOutBg",            "OLEANDER_BUBBLE_OUT"),
    ("msgInBgSelected",     "OLEANDER_BUBBLE_SEL"),
]
by_key = {k: v for k, v, _ in rows}
for key, name in SEED:
    val = by_key.get(key)
    if val and val.startswith("#") and val not in NAMES:
        NAMES[val] = name

def base_of(key):
    v = by_key[key]
    while not v.startswith("#"):
        v = by_key[v]
    return v

ALPHA_CONSTS = [
    ("OLEANDER_COMPOSE_BG", 0.00, "windowBg",
     ["historyComposeAreaBg"],
     "message field itself, fully transparent over the wallpaper"),
    ("OLEANDER_COMPOSE_EDGE", 0.85, "windowBg",
     ["historyReplyBg"],
     "strip framing the message field, 85% opaque"),
    ("OLEANDER_PANEL_85", 0.85, "windowBg",
     ["historyComposeButtonBg"],
     "unblock / join / mute panel, 85% opaque"),
    ("OLEANDER_ICON_85", 0.85, "menuIconFg",
     ["historyComposeIconFg"],
     "attach / emoji / mic icons, 85% opaque"),
    ("OLEANDER_BUBBLE_IN_85", 0.85, "msgInBg",
     ["msgInBg"],
     "incoming bubble, 85% opaque"),
    ("OLEANDER_BUBBLE_OUT_85", 0.85, "msgOutBg",
     ["msgOutBg"],
     "outgoing bubble, 85% opaque"),
    ("OLEANDER_ICON_85_OVER", 0.85, "menuIconFgOver",
     ["historyComposeIconFgOver"],
     "same icons with mouse over, 85% opaque"),
]

# rose .. coral, no cold tones; lightness alternates so users stay distinguishable
USERPIC_HUES = [312, 324, 336, 348, 358, 8, 18, 342]
USERPIC_L    = [0.58, 0.46, 0.62, 0.50, 0.56, 0.44, 0.60, 0.66]
USERPIC_S    = 0.28   # muted: these sit next to the chat list, they must not shout
userpic_lines = []
for i, (hue, ltop) in enumerate(zip(USERPIC_HUES, USERPIC_L), start=1):
    top    = colorsys.hls_to_rgb(hue / 360, ltop, USERPIC_S)
    bottom = colorsys.hls_to_rgb(hue / 360, ltop - 0.16, USERPIC_S + 0.06)
    for suffix, rgbv in (("", top), ("2", bottom)):
        hexv = "#%02x%02x%02x" % tuple(round(c * 255) for c in rgbv)
        key = f"historyPeer{i}UserpicBg{suffix}"
        for row in rows:
            if row[0] == key:
                row[1] = hexv
        userpic_lines.append(f"{key} {hexv}")

alpha_lines = []
for name, alpha, base_key, targets, note in ALPHA_CONSTS:
    val = f"{base_of(base_key)[:7]}{round(alpha * 255):02x}"
    alpha_lines.append(f"{name}: {val}; // {note}")
    for row in rows:
        if row[0] in targets:
            row[1] = name

const_lines = []
for key, name in SEED:
    val = by_key.get(key)
    if val and NAMES.get(val) == name:
        const_lines.append(f"{name}: {val}; // used {counts[val]}x")

def near(val, ref, tol=6):
    if len(val) != 7 or len(ref) != 7:
        return False
    a = [int(val[i:i+2], 16) for i in (1, 3, 5)]
    b = [int(ref[i:i+2], 16) for i in (1, 3, 5)]
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5 <= tol

snapped = 0
for row in rows:
    if not row[1].startswith("#") or row[1] in NAMES:
        continue
    is_fg = "Fg" in row[0] or row[0].endswith("Color")
    for ref, name in NAMES.items():
        # only snap like onto like: text shades onto text/accent, surfaces onto surfaces
        if "BUBBLE" in name:
            continue
        if is_fg and not ("TEXT" in name or "ACCENT" in name):
            continue
        if not is_fg and not ("BG" in name or "ACCENT" in name):
            continue
        if near(row[1], ref):
            row[1] = ref
            snapped += 1
            break

body = []
for key, val, comment in rows:
    if val in NAMES:
        val = NAMES[val]
    body.append(f"{key}: {val};{comment}")

refs = collections.Counter(l.split(": ", 1)[1].split(";")[0] for l in body)
used = set(refs)
const_lines = [re.sub(r"used \d+x", f"used {refs[l.split(':')[0]]}x", l) for l in const_lines]
const_lines = [l for l in const_lines if l.split(":")[0] in used]
alpha_lines = [l for l in alpha_lines if l.split(":")[0] in used]

out = []
out += header
out.append("")
out.append("// === OLEANDER CONSTANTS =====================================")
out.append("// Change a value here and every key below follows.")
out += const_lines
out += alpha_lines
out.append("// ============================================================")
out.append("")
out += body

open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")

print("constants:")
print("\n".join(const_lines))
print("\nsnapped near-duplicates:", snapped)
print("replaced hex -> constant:", sum(1 for _, v, _ in rows if v in NAMES), "of", len(rows), "keys")
