# The World in One Day — 17 November 2026

Competition: `news-image-20261117` on make.fun ($250, 50 paid places).
Deadline: 2026-11-19 00:00 UTC (07:00 WIB).

## The image

A newspaper front page summing up Tuesday 17 November 2026 in six stories,
each verified against reporting of that day:

1. **Ukraine** — Kerch Bridge hit again: Ukraine strikes the bridge to Crimea
   for a second day; a road span collapses into the strait.
2. **The Gulf** — Iranian drones hit a US radar site in Bahrain; Bahrain says
   all were intercepted. Tankers hit mines near the Strait of Hormuz.
3. **Gaza** — UK, Australia, Canada and Italy press Israel to open aid
   crossings, calling the crisis catastrophic; the UN warns 1.7m remain
   displaced as winter nears.
4. **Asia** — Trump opens his Asia trip in Manila with a Quad summit; Trump,
   Xi and Putin are set to meet in Shenzhen on Thursday.
5. **Europe** — Five EU states (Austria, Denmark, Germany, Greece, the
   Netherlands) plan a migrant return hub in Rwanda.
6. **Tech & Markets** — The US closes a chip-export loophole targeting
   data centres renting computing power to China; Bitcoin holds below $65,000.

The date is named in the masthead and the footer, and every story is dated
to 17 November 2026. The image is original work drawn with Pillow
(`gen.py`); no photographs, no copied artwork.

## The program

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png`, then verifies it is a whole PNG and under the 1 MiB
gate, failing loudly otherwise. No network, no randomness, no model calls
at run time — a plain byte copy, so two runs always write the same bytes.

`gen.py` is the build script that drew `entry.png` (Pillow, local fonts);
it is not run by the entry and is kept in the repo so the image is
reproducible.

## Run / test it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# run it twice and compare:
mkdir -p out2 && MAKEFUN_OUTPUT_DIR=out2 python3 main.py
sha256sum out/entry.png out2/entry.png   # identical
python3 -c "from PIL import Image; print(Image.open('out/entry.png').format, Image.open('out/entry.png').size)"
```

Expected: PNG, 1024x1024, 108,739 bytes, sha256
`af4bdbf64ba911a602f33024193b2863d85a64c99331b04e0b44e9605c16445a`.

Regenerate the image from scratch with `python3 gen.py`.

## License

MIT — see LICENSE.
