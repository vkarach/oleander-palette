# oleander-palette

A rose-tinted dark theme for Telegram Desktop (`Oleander.tdesktop-palette`), plus
a generated reference page mapping every palette key to where it shows up in the UI.

**Reference page:** https://vkarach.github.io/oleander-palette/

## Layout

| Path | What |
| --- | --- |
| `palette/Oleander.tdesktop-palette` | the theme, version-tracked |
| `backups/` | timestamped snapshots (gitignored) |
| `template.html` | HTML shell for the reference page, `__DATA__` is the injection point |
| `build.py` | reads the palette, writes `docs/index.html` |
| `docs/index.html` | the published reference page (served by GitHub Pages) |
| `tools/recolor.py` | one-time bootstrap that generated the first palette from a base theme |

## Build the reference page

```
python build.py                                  # uses palette/Oleander.tdesktop-palette
python build.py path/to/Oleander.tdesktop-palette
```

Commit the updated `docs/index.html`; Pages serves it from `main` / `docs`.

## Back up the live palette

`backup.py` copies the palette out of Telegram Desktop into the repo and writes a
timestamped snapshot to `backups/`.

```
python backup.py                        # %APPDATA%/Telegram Desktop/tdata/Oleander.tdesktop-palette
python backup.py path/to/palette         # or set OLEANDER_PALETTE
```

The palette is committed, so git history is the version-tracked backup; `backups/`
holds local pre-change snapshots as a safety net.
