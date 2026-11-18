"""news-image-20261117 entry: copy the image this repository holds to
/output/entry.png.

Standard library only, no network, no randomness, no model calls. The copy
is a plain byte copy, so two runs always write the same bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, OUT)

# Fail loudly instead of shipping a truncated file: the gate requires a
# whole PNG, told apart by its first bytes and read through to its end.
with open(OUT, "rb") as f:
    data = f.read()
if not (data[:8] == b"\x89PNG\r\n\x1a\n" and data[-8:-4] == b"IEND"):
    raise SystemExit("entry.png is not a whole PNG")
# The gate refuses anything over 1 MiB: fail here rather than on the site.
if len(data) > 1048576:
    raise SystemExit("entry.png exceeds the 1 MiB gate")
print("wrote", OUT, len(data), "bytes")
