# oleander-palette

A rose and maroon dark color palette.

**Live page:** https://palette.vkarach.com

## Layout

| Path | What |
| --- | --- |
| `palette.json` | the palette, source of truth |
| `templates/` | `index.html` (color squares), `details.html` (detailed map), shared `style.css` |
| `build.py` | renders `docs/index.html` and `docs/details.html` from `palette.json` |
| `docs/` | the published pages (GitHub Pages) |
| `palette/Oleander.tdesktop-palette` | optional Telegram Desktop theme using the same colors |

## Build

```
python build.py
```

Commit the updated `docs/`.
