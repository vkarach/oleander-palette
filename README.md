# oleander-palette

A rose and maroon dark color palette.

**Live page:** https://palette.vkarach.com

## Layout

| Path | What |
| --- | --- |
| `palette.json` | the palette, source of truth |
| `template.html` | HTML shell, `__DATA__` is the injection point |
| `build.py` | renders `docs/index.html` from `palette.json` |
| `docs/` | the published page (GitHub Pages) |
| `palette/Oleander.tdesktop-palette` | optional Telegram Desktop theme using the same colors |

## Build

```
python build.py
```

Commit the updated `docs/index.html`.
