"""Round the corners of Turaco.ico to match Sangala Studio's badge.

    python tools/round_icon.py

WHY. The three applications sit side by side on the Desktop and should read as one family. Studio's
badge is a rounded square; Mosaic's was a hard-edged one. Glen, 2026-08-14: "round the corners of the
mosaic badge so that it matches the other two."

THE RADIUS IS MEASURED, NOT CHOSEN. Sangala.ico's 256 px entry is transparent along its top row until
x = 39, so the corner radius is 39/256 of the side. Expressed as a fraction it holds at every size,
from 256 down to 16.

This rounds the icon that already exists rather than rebuilding it from the source picture, so the
crop, the colours and the seven sizes are exactly as they were - only the corners change. Every entry
in the file is a 32-bit PNG, which is what makes that possible. There is no Pillow on this machine;
PyMuPDF decodes and re-encodes, and the mask is computed here.
"""
import os
import struct
import sys

import fitz

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICO = os.path.join(HERE, "Turaco.ico")
RADIUS = 39.0 / 256.0


def round_corners(png_bytes, size):
    """Cut the corners of one icon entry, keeping whatever transparency it already had."""
    pm = fitz.Pixmap(png_bytes)
    if pm.width != size or pm.height != size:
        return None
    had_alpha = pm.alpha
    src, n, stride = pm.samples, pm.n, pm.stride
    r = RADIUS * size
    centers = ((r, r), (size - r, r), (r, size - r), (size - r, size - r))
    out = bytearray(size * size * 4)
    for y in range(size):
        for x in range(size):
            cov = 0
            for sy in (0.17, 0.5, 0.83):
                for sx in (0.17, 0.5, 0.83):
                    px, py = x + sx, y + sy
                    inside = True
                    for cx, cy in centers:
                        if ((px < cx) == (cx < size / 2)) and ((py < cy) == (cy < size / 2)):
                            if (px - cx) ** 2 + (py - cy) ** 2 > r * r:
                                inside = False
                            break
                    if inside:
                        cov += 1
            i, o = (y * stride) + x * n, (y * size + x) * 4
            out[o:o + 3] = src[i:i + 3]
            # multiply, never overwrite: an entry that was already transparent somewhere stays so
            a = src[i + n - 1] if had_alpha else 255
            out[o + 3] = (a * ((cov * 255) // 9)) // 255
    return fitz.Pixmap(fitz.csRGB, size, size, bytes(out), True).tobytes("png")


def main():
    if not os.path.isfile(ICO):
        sys.exit("missing: %s" % ICO)
    d = open(ICO, "rb").read()
    count = struct.unpack("<H", d[4:6])[0]
    entries = []
    for i in range(count):
        w, h, c, r, pl, bc, size, off = struct.unpack("<BBBBHHII", d[6 + 16 * i:22 + 16 * i])
        side = w or 256
        payload = d[off:off + size]
        if payload[:8] != b"\x89PNG\r\n\x1a\n":
            sys.exit("entry %d is not a PNG; this script only rounds PNG entries" % side)
        rounded = round_corners(payload, side)
        if rounded is None:
            sys.exit("entry %d did not decode to a %dx%d image" % (side, side, side))
        entries.append((side, rounded))

    offset = 6 + 16 * len(entries)
    head = struct.pack("<HHH", 0, 1, len(entries))
    dirs, body = b"", b""
    for side, data in entries:
        b = 0 if side == 256 else side
        dirs += struct.pack("<BBBBHHII", b, b, 0, 0, 1, 32, len(data), offset)
        body += data
        offset += len(data)
    with open(ICO, "wb") as f:
        f.write(head + dirs + body)

    print("rounded %s" % ICO)
    for side, data in entries:
        print("   %3d x %-3d  %6d bytes" % (side, side, len(data)))
    print("%d bytes total" % os.path.getsize(ICO))
    print("Now rebuild the launcher: \"Build SangalaMosaic Launcher.cmd\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
