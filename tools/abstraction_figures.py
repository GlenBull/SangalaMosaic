"""Figures for the "stylizing a mosaic" lesson: the crested crane prototype beside its stylized version.

Two grids drive everything:
  proto.txt  - Sangala Mosaic's own Build It! of Images/Crested Crane.png (32 x 32, Fit to Photo,
               Ignore background, Colors 16), read straight out of the page's `built.idx`.
  stylized   - sampled here from Images/Crane (AI).png (a 32 x 48 rendered mosaic) and fitted into
               the same 32 x 32 layout the lesson's screenshot shows (28 rows tall, columns 8-24).

Run:  python tools\abstraction_figures.py <proto.txt> <out folder>
Writes the grid renderings and the lesson figures as PNG into <out folder>.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(os.path.dirname(HERE), "Images")

# Sangala Mosaic's palette, by index (the first 79 as of 2026-09-03.92). Only the entries the two
# grids use need to be right; the rest are carried so an index never falls off the end.
PAL = {
  0:("White",[242,243,242]), 1:("Black",[27,42,52]), 2:("Red",[196,40,28]), 5:("Yellow",[245,205,48]),
  8:("Nougat",[204,142,104]), 9:("Reddish Brown",[105,64,39]), 10:("Dark Brown",[55,33,21]),
  11:("Bright Green",[75,159,74]), 12:("Green",[40,127,70]), 17:("Dark Blue",[32,50,90]),
  20:("Light Gray",[160,165,169]), 21:("Dark Gray",[89,93,96]), 26:("Medium Gray",[108,110,104]),
  27:("Aqua",[211,242,234]), 29:("Brick Yellow",[204,185,141]), 32:("Bright Orange",[214,121,35]),
  40:("Dark Stone Grey",[100,100,100]), 51:("Medium Nougat",[170,125,85]),
  52:("Medium Stone Grey",[150,150,150]), 57:("Sand Yellow",[137,125,98]),
}

def read_grid(path):
    rows = [l.rstrip("\n") for l in open(path) if l.strip()]
    g = []
    for l in rows:
        g.append([-1 if l[i:i+2] == ".." else int(l[i:i+2]) for i in range(0, len(l), 2)])
    return g

# ---- the stylized crane, sampled from the rendered 32 x 48 mosaic ---------------------------------
STYL_COLORS = {          # the stylized vocabulary; each source cell snaps to the nearest of these
  "Yellow":5, "Black":1, "White":0, "Red":2, "Light Gray":20, "Dark Gray":21, "Dark Blue":17,
  "Bright Green":11, "Sky":-1,
}
SKY = [159,195,233]

def nearest(rgb, cands):
    best, bd = None, 1e18
    for name, c in cands:
        d = sum((a-b)**2 for a, b in zip(rgb, c))
        if d < bd: best, bd = name, d
    return best

def sample_stylized():
    im = Image.open(os.path.join(IMAGES, "Crane (AI).png")).convert("RGB")
    W, H = im.size; cols, rows = 32, 48
    cands = [(n, SKY if n == "Sky" else PAL[i][1]) for n, i in STYL_COLORS.items()]
    src = []
    for r in range(rows):
        row = []
        for c in range(cols):
            # average a small patch at the cell center (skips the bevel edges of the rendered tile)
            x0, y0 = int((c+0.5)*W/cols), int((r+0.5)*H/rows)
            px = [im.getpixel((x, y)) for x in range(x0-1, x0+2) for y in range(y0-1, y0+2)]
            rgb = [sum(p[k] for p in px)/len(px) for k in range(3)]
            n = nearest(rgb, cands)
            row.append(-1 if n == "Sky" else STYL_COLORS[n])
        src.append(row)
    # fit into the lesson's 32 x 32 layout: 28 rows tall starting at row 3, 17.5 columns wide from column 7
    out = [[-1]*32 for _ in range(32)]
    scale = 28/48
    for r in range(32):
        for c in range(32):
            sr = int((r-3)/scale); sc = int((c-7)/scale)
            if 0 <= sr < rows and 0 <= sc < cols and 3 <= r < 31:
                # majority vote over the source cells that land in this target cell
                votes = {}
                for rr in range(int((r-3)/scale), int((r-2)/scale)):
                    for cc in range(int((c-7)/scale), int((c-6)/scale)):
                        if 0 <= rr < rows and 0 <= cc < cols:
                            v = src[rr][cc]; votes[v] = votes.get(v, 0) + 1
                if votes:
                    out[r][c] = max(votes.items(), key=lambda kv: (kv[1], kv[0] >= 0))[0]
    return src, out

# ---- drawing ------------------------------------------------------------------------------------
def font(sz, bold=False):
    for name in (["arialbd.ttf"] if bold else ["arial.ttf"]):
        try: return ImageFont.truetype(name, sz)
        except Exception: pass
    return ImageFont.load_default()

def draw_grid(g, cell=14, labels=True, hi=None, outline=None, origin=(0,0), img=None, pad=None):
    """Render a grid of palette indices as flat tiles on a light plate. `hi` = set of (r,c) to spotlight
    (others dimmed); `outline` = list of (kind, geometry, color) shapes drawn over it."""
    gh, gw = len(g), len(g[0])
    pad = pad if pad is not None else (22 if labels else 4)
    W, H = gw*cell + pad + 4, gh*cell + pad + 4
    if img is None:
        img = Image.new("RGB", (W, H), (248, 246, 240))
    d = ImageDraw.Draw(img, "RGBA")
    ox, oy = origin[0] + pad, origin[1] + pad
    f = font(9)
    for r in range(gh):
        for c in range(gw):
            x, y = ox + c*cell, oy + r*cell
            v = g[r][c]
            if v >= 0:
                col = tuple(PAL[v][1])
                if hi is not None and (r, c) not in hi:
                    col = tuple(int(k*0.35 + 235*0.65) for k in col)
                d.rectangle([x, y, x+cell-1, y+cell-1], fill=col, outline=(255,255,255,90))
            else:
                d.rectangle([x, y, x+cell-1, y+cell-1], fill=(232,230,224), outline=(255,255,255,120))
    if labels:
        for c in range(gw):
            d.text((ox + c*cell + cell/2, origin[1] + pad/2), str(c+1), fill=(90,80,60), font=f, anchor="mm")
        for r in range(gh):
            lab = chr(65 + r) if r < 26 else "A" + chr(65 + r - 26)
            d.text((origin[0] + pad/2, oy + r*cell + cell/2), lab, fill=(90,80,60), font=f, anchor="mm")
    for kind, geo, color in (outline or []):
        if kind == "rect":   # geo = (r0,c0,r1,c1) inclusive cells
            r0, c0, r1, c1 = geo
            d.rectangle([ox+c0*cell, oy+r0*cell, ox+(c1+1)*cell-1, oy+(r1+1)*cell-1], outline=color, width=3)
        elif kind == "ellipse":
            r0, c0, r1, c1 = geo
            d.ellipse([ox+c0*cell, oy+r0*cell, ox+(c1+1)*cell-1, oy+(r1+1)*cell-1], outline=color, width=3)
        elif kind == "poly":  # geo = list of (r,c) corner points in cell units (floats allowed)
            pts = [(ox + c*cell, oy + r*cell) for r, c in geo]
            d.polygon(pts, outline=color, width=3) if hasattr(d, "polygon") else d.line(pts + [pts[0]], fill=color, width=3)
        elif kind == "line":
            (r0, c0), (r1, c1) = geo
            d.line([ox+c0*cell, oy+r0*cell, ox+c1*cell, oy+r1*cell], fill=color, width=3)
    return img

def crop_cells(g, r0, c0, r1, c1):
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def count(g, cells):
    return sum(1 for (r, c) in cells if g[r][c] >= 0)

def region(g, r0, c0, r1, c1):
    return {(r, c) for r in range(r0, r1+1) for c in range(c0, c1+1) if g[r][c] >= 0}


if __name__ == "__main__":
    proto = read_grid(sys.argv[1]); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    src, styl = sample_stylized()
    sys.path.insert(0, HERE)
    from abstraction_figs_part2 import make_all, clean_stylized
    styl = clean_stylized(styl)
    draw_grid(proto, 16).save(os.path.join(out, "grid_prototype.png"))
    draw_grid(styl, 16).save(os.path.join(out, "grid_stylized.png"))
    with open(os.path.join(out, "stylized.txt"), "w") as f:
        for row in styl: f.write("".join(".." if v < 0 else "%02d" % v for v in row) + "\n")
    pp, ps = make_all(proto, styl, out)
    print("figures written to", out)
    print({k: len(v) for k, v in pp.items()}); print({k: len(v) for k, v in ps.items()})
