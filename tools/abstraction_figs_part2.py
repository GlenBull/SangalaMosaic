"""Second half of abstraction_figures.py: the parts of the crane on each grid, and the five lesson figures.
Kept as a sibling module so the first half (grid reading, sampling, drawing) stays short."""
import os
from PIL import Image, ImageDraw
from abstraction_figures import PAL, font, draw_grid, crop_cells

# ---- the parts, as cell sets on each grid (0-based rows and columns) ----------------------------
def cells(*rects):
    out = set()
    for r0, c0, r1, c1 in rects:
        out |= {(r, c) for r in range(r0, r1+1) for c in range(c0, c1+1)}
    return out

def live(g, s):                       # keep only the cells that hold a tile
    return {(r, c) for (r, c) in s if g[r][c] >= 0}

def parts_proto(g):
    crown = cells((2,20,3,25), (4,20,4,21))
    bill  = {(5,26), (6,25), (6,26)}
    head  = cells((4,22,4,25), (5,20,5,26), (6,21,6,26)) - bill
    neck  = cells((7,21,10,24), (11,21,11,24), (12,23,12,24))
    body  = cells((11,7,21,24), (22,7,22,9)) - neck
    legs  = cells((22,11,27,18))
    feet  = cells((28,10,29,20))
    P = {"Crown":crown, "Head":head, "Bill":bill, "Neck":neck, "Body":body, "Legs":legs, "Feet":feet}
    return {k: live(g, v) for k, v in P.items()}

def parts_styl(g):
    """Crane 5.mosaic, 0-based: crown D-F, head G-J, bill the red cells, neck K-O at columns 19-20,
    body O-U, legs V-AA (one tile wide each), feet the black run on AB, ground the green."""
    crown = cells((3,17,5,21))
    bill  = {(r, c) for r in range(6, 10) for c in range(17, 24) if g[r][c] == 2}
    neck  = {(9,18), (9,19)} | cells((10,18,14,19))
    head  = cells((6,17,9,23)) - bill - neck
    legs  = cells((21,13,21,16)) | {(r, c) for r in range(22, 27) for c in (13, 15)}
    body  = {(r, c) for r in range(14, 21) for c in range(8, 20)} - neck
    feet  = {(27, c) for c in range(8, 26) if g[27][c] == 1}
    ground = {(r, c) for r in range(27, 31) for c in range(6, 27) if g[r][c] == 11}
    P = {"Crown":crown, "Head":head, "Bill":bill, "Neck":neck, "Body":body, "Legs":legs, "Feet":feet, "Ground":ground}
    return {k: live(g, v) for k, v in P.items()}

PART_COLOR = {"Crown":(230,160,0), "Head":(30,30,30), "Bill":(200,30,30), "Neck":(0,120,200),
              "Body":(0,150,90), "Legs":(120,60,180), "Feet":(120,60,180), "Ground":(60,120,40)}

def bbox(s):
    rs = [r for r, c in s]; cs = [c for r, c in s]
    return min(rs), min(cs), max(rs), max(cs)

def clean_stylized(g):
    g = [row[:] for row in g]
    for c in range(32):                 # the baseplate's bottom edge came through the sampling as a stray row
        g[30][c] = -1
    return g

import math
def fit_ellipse(s, k=1.25, n=72):
    """An ellipse along the part's own principal axis, from the covariance of its cell centers."""
    pts = [(r+0.5, c+0.5) for r, c in s]; m = len(pts)
    mr = sum(p[0] for p in pts)/m; mc = sum(p[1] for p in pts)/m
    srr = sum((p[0]-mr)**2 for p in pts)/m; scc = sum((p[1]-mc)**2 for p in pts)/m; src = sum((p[0]-mr)*(p[1]-mc) for p in pts)/m
    tr, det = srr+scc, srr*scc-src*src
    l1 = tr/2 + math.sqrt(max(0, tr*tr/4-det)); l2 = tr/2 - math.sqrt(max(0, tr*tr/4-det))
    ang = 0.5*math.atan2(2*src, srr-scc) if abs(srr-scc) > 1e-9 or abs(src) > 1e-9 else 0
    a, b = k*2*math.sqrt(max(l1, 0.05)), k*2*math.sqrt(max(l2, 0.05))
    out = []
    for i in range(n):
        t = 2*math.pi*i/n; u, v = a*math.cos(t), b*math.sin(t)
        out.append((mr + u*math.cos(ang) - v*math.sin(ang), mc + u*math.sin(ang) + v*math.cos(ang)))
    return out

def fit_bar(s, pad=0.15):
    """A rectangle along the part's principal axis, just enclosing its cells."""
    pts = [(r+0.5, c+0.5) for r, c in s]; m = len(pts)
    mr = sum(p[0] for p in pts)/m; mc = sum(p[1] for p in pts)/m
    srr = sum((p[0]-mr)**2 for p in pts)/m; scc = sum((p[1]-mc)**2 for p in pts)/m; src = sum((p[0]-mr)*(p[1]-mc) for p in pts)/m
    ang = 0.5*math.atan2(2*src, srr-scc)
    ur, uc = math.cos(ang), math.sin(ang); vr, vc = -uc, ur
    us = [ (p[0]-mr)*ur + (p[1]-mc)*uc for p in pts ]; vs = [ (p[0]-mr)*vr + (p[1]-mc)*vc for p in pts ]
    u0, u1, v0, v1 = min(us)-0.5-pad, max(us)+0.5+pad, min(vs)-0.5-pad, max(vs)+0.5+pad
    return [(mr + u*ur + v*vr, mc + u*uc + v*vc) for u, v in ((u0,v0),(u0,v1),(u1,v1),(u1,v0))]

def title(img, text, y=6, size=15, bold=True, x=None):
    d = ImageDraw.Draw(img); f = font(size, bold)
    d.text((img.width/2 if x is None else x, y), text, fill=(40,35,25), font=f, anchor="ma")

def hstack(imgs, gap=24, pad=16, bg=(255,255,255), top=0):
    W = sum(i.width for i in imgs) + gap*(len(imgs)-1) + 2*pad; H = max(i.height for i in imgs) + 2*pad + top
    out = Image.new("RGB", (W, H), bg); x = pad
    for i in imgs: out.paste(i, (x, pad + top)); x += i.width + gap
    return out

def vstack(imgs, gap=16, pad=16, bg=(255,255,255)):
    W = max(i.width for i in imgs) + 2*pad; H = sum(i.height for i in imgs) + gap*(len(imgs)-1) + 2*pad
    out = Image.new("RGB", (W, H), bg); y = pad
    for i in imgs: out.paste(i, ((W - i.width)//2, y)); y += i.height + gap
    return out

def captioned(img, text, size=13, bold=False, width=None):
    f = font(size, bold); d = ImageDraw.Draw(img)
    words, lines, cur = text.split(), [], ""
    maxw = (width or img.width) - 8
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur)
    lh = size + 4
    out = Image.new("RGB", (max(img.width, width or 0), img.height + 8 + lh*len(lines)), (255,255,255))
    out.paste(img, ((out.width - img.width)//2, 0)); d = ImageDraw.Draw(out)
    for i, l in enumerate(lines):
        d.text((out.width/2, img.height + 6 + i*lh), l, fill=(40,35,25), font=f, anchor="ma")
    return out

def crop_img(g, r0, c0, r1, c1, cell=20, margin=1, hi=None, outline=None):
    r0, c0 = max(0, r0-margin), max(0, c0-margin); r1, c1 = min(31, r1+margin), min(31, c1+margin)
    sub = crop_cells(g, r0, c0, r1, c1)
    hi2 = None if hi is None else {(r-r0, c-c0) for r, c in hi}
    ol = []
    for kind, geo, color in (outline or []):
        if kind == "line": ol.append((kind, tuple((r-r0, c-c0) for r, c in geo), color))
        elif kind == "poly": ol.append((kind, [(r-r0, c-c0) for r, c in geo], color))
        else: ol.append((kind, (geo[0]-r0, geo[1]-c0, geo[2]-r0, geo[3]-c0), color))
    return draw_grid(sub, cell, labels=False, hi=hi2, outline=ol)

def fig_two_levels(proto, styl, out):
    a = draw_grid(proto, 15); b = draw_grid(styl, 15)
    na, ka = sum(1 for r in proto for v in r if v >= 0), len({v for r in proto for v in r if v >= 0})
    nb, kb = sum(1 for r in styl for v in r if v >= 0), len({v for r in styl for v in r if v >= 0})
    a = captioned(a, "Prototype: Build It! from the photo. %d tiles, %d colors" % (na, ka), 14, True)
    b = captioned(b, "Stylized: the same crane, redrawn by hand. %d tiles, %d colors (sky left to the plate)" % (nb, kb), 14, True)
    img = hstack([a, b], top=30)
    title(img, "The same figure at two levels of abstraction", 12, 18)
    img.save(os.path.join(out, "Fig 1 - Two Levels.png"))

def outlined_grid(g, parts, cell=15):
    img = draw_grid(g, cell)
    d = ImageDraw.Draw(img); f = font(12, True)
    pad = 22
    for k, s in parts.items():
        if not s: continue
        r0, c0, r1, c1 = bbox(s)
        x0, y0, x1, y1 = pad + c0*cell - 2, pad + r0*cell - 2, pad + (c1+1)*cell + 1, pad + (r1+1)*cell + 1
        d.rectangle([x0, y0, x1, y1], outline=PART_COLOR[k], width=2)     # sits in the seam, covers no tile
        if k == "Body":
            x = x0 - 6; anchor = "rm"
        elif k == "Feet" and parts.get("Ground"):
            x = pad + bbox(parts["Ground"])[1]*cell - 8; anchor = "rm"
        else:
            x = x1 + 6; anchor = "lm"
        y = (y0 + y1)/2
        d.text((x, y), "%s  %d" % (k, len(s)), fill=PART_COLOR[k], font=f, anchor=anchor)
    return img

def fig_parts(proto, styl, pp, ps, out):
    a = captioned(outlined_grid(proto, pp), "Prototype: each part boxed, with its tile count", 14, True)
    b = captioned(outlined_grid(styl, ps), "Stylized: the same parts, boxed and counted", 14, True)
    img = hstack([a, b], top=30)
    title(img, "Step 3. The figure is a list of named parts, and every part survives the change", 12, 18)
    img.save(os.path.join(out, "Fig 2 - Named Parts.png"))

def fig_simple_shapes(proto, styl, pp, ps, out):
    cols = []
    spec = [
      ("Body becomes an OVAL",  "Body", [("poly", fit_ellipse(pp["Body"], 1.02), (0,150,90))],   [("poly", fit_ellipse(ps["Body"], 1.08), (0,150,90))]),
      ("Neck becomes a BAR",    "Neck", [("poly", fit_bar(pp["Neck"]), (0,120,200))],      [("poly", fit_bar(ps["Neck"]), (0,120,200))]),
      ("Head becomes a DISC",   "Head", [("poly", fit_ellipse(pp["Head"], 1.05), (30,30,30))], [("poly", fit_ellipse(ps["Head"], 1.05), (30,30,30))]),
      ("Bill becomes a WEDGE",  "Bill", [("poly", [(5,25),(5,27.5),(7,25)], (200,30,30))], [("poly", [(8,21),(8.6,24.3),(10,21)], (200,30,30))]),
      ("Legs become BARS",      "Legs", [("rect", (22,12,27,14), (120,60,180)), ("rect", (22,16,27,17), (120,60,180))],
                                        [("rect", (21,13,26,13), (120,60,180)), ("rect", (21,15,26,15), (120,60,180))]),
      ("Feet become a BAND",    "Feet", [("rect", (28,10,29,20), (60,120,40))],       [("rect", (27,7,30,24), (60,120,40))]),
    ]
    tops, bots, labels = [], [], []
    for label, key, olA, olB in spec:
        hiA = pp[key] | (pp["Feet"] if key == "Legs" else set())
        hiB = ps[key] | (ps["Ground"] if key == "Feet" else set()) | (ps["Feet"] if key == "Legs" else set())
        ra, rb = bbox(hiA), bbox(hiB)
        if key == "Bill": ra = (4, 24, 7, 27); rb = (7, 20, 10, 24)
        if key == "Feet": ra = (27, 9, 30, 21); rb = (26, 7, 30, 26)
        m = 2 if key == "Body" else 1
        tops.append(crop_img(proto, *ra, cell=16, margin=m, hi=hiA, outline=olA))
        bots.append(crop_img(styl,  *rb, cell=16, margin=m, hi=hiB, outline=olB))
        labels.append(label)
    fb = font(13, True); fr = font(12)
    d0 = ImageDraw.Draw(tops[0])
    colw = [max(a.width, b.width, int(d0.textlength(l, font=fb)) + 12) for a, b, l in zip(tops, bots, labels)]
    h1, h2 = max(a.height for a in tops), max(b.height for b in bots)
    gap, left, top = 18, 84, 30 + 30
    W = left + sum(colw) + gap*(len(colw)-1) + 16; H = top + h1 + 12 + h2 + 16
    img = Image.new("RGB", (W, H), (255,255,255)); d = ImageDraw.Draw(img)
    x = left
    for a, b, l, w in zip(tops, bots, labels, colw):
        d.text((x + w/2, top - 22), l, fill=(40,35,25), font=fb, anchor="ma")
        img.paste(a, (x + (w - a.width)//2, top + (h1 - a.height)//2))
        img.paste(b, (x + (w - b.width)//2, top + h1 + 12 + (h2 - b.height)//2))
        x += w + gap
    d.text((left - 10, top + h1/2), "prototype", fill=(90,80,60), font=fr, anchor="rm")
    d.text((left - 10, top + h1 + 12 + h2/2), "stylized", fill=(90,80,60), font=fr, anchor="rm")
    title(img, "Step 5. Each part is reduced to the nearest simple shape: the outline is the target, the tiles fill it", 10, 17)
    img.save(os.path.join(out, "Fig 3 - Simple Shapes.png"))

def fig_grid_rules(proto, styl, pp, ps, out):
    a1 = crop_img(proto, 4, 23, 7, 27, cell=22, hi={(5,26), (6,25), (6,26)})
    b1 = crop_img(styl, 7, 20, 10, 24, cell=22, hi=ps["Bill"])
    a2 = crop_img(proto, 26, 9, 30, 21, cell=16, hi=pp["Feet"])
    b2 = crop_img(styl, 25, 7, 30, 26, cell=16, hi=ps["Feet"] | ps["Ground"])
    bill_pair = hstack([captioned(a1, "prototype: a 1-tile bill", 11), captioned(b1, "stylized: a solid red block", 11)], gap=10, pad=4)
    feet_pair = hstack([captioned(a2, "prototype: toes 1 tile wide, scattered", 11), captioned(b2, "stylized: one solid row on a band", 11)], gap=10, pad=4)
    left = vstack([bill_pair, feet_pair], gap=10, pad=6)
    left = captioned(left, "Rule 1. A feature narrower than two tiles does not survive: widen it or drop it", 13, True, width=left.width)
    a3 = crop_img(proto, 10, 6, 23, 25, cell=14, hi=pp["Body"], outline=[("line", ((11, 24.5), (22.5, 7)), (220,40,40))])
    b3 = crop_img(styl, 13, 7, 22, 21, cell=14, hi=ps["Body"], outline=[("rect", bbox(ps["Body"]), (220,40,40))])
    right = hstack([captioned(a3, "prototype: the back runs at a slant, so every row steps", 11, width=a3.width+20),
                    captioned(b3, "stylized: the body sits upright, edges run with the grid", 11, width=b3.width+20)], gap=10, pad=4)
    right = captioned(right, "Rule 2. A diagonal renders as a staircase: straighten it where the pose allows", 13, True, width=right.width)
    img = hstack([left, right], gap=30, top=30)
    title(img, "Step 5. Two rules that come from the grid itself", 10, 17)
    img.save(os.path.join(out, "Fig 4 - Grid Rules.png"))

def fig_exaggerate(proto, styl, pp, ps, out):
    cell = 16; pad = 22
    img = Image.new("RGB", (32*cell + pad + 4, 32*cell + pad + 4), (248,246,240))
    d = ImageDraw.Draw(img, "RGBA")
    for r in range(32):
        for c in range(32):
            x, y = pad + c*cell, pad + r*cell
            d.rectangle([x, y, x+cell-1, y+cell-1], fill=(232,230,224), outline=(255,255,255,120))
            v = proto[r][c]
            if v >= 0:
                col = tuple(int(k*0.30 + 240*0.70) for k in PAL[v][1])
                d.rectangle([x, y, x+cell-1, y+cell-1], fill=col)
    for r in range(32):
        for c in range(32):
            v = styl[r][c]
            if v >= 0:
                x, y = pad + c*cell, pad + r*cell
                d.rectangle([x+1, y+1, x+cell-2, y+cell-2], fill=tuple(PAL[v][1]))
    f = font(9)
    for c in range(32): d.text((pad + c*cell + cell/2, pad/2), str(c+1), fill=(90,80,60), font=f, anchor="mm")
    for r in range(32):
        lab = chr(65 + r) if r < 26 else "A" + chr(65 + r - 26)
        d.text((pad/2, pad + r*cell + cell/2), lab, fill=(90,80,60), font=f, anchor="mm")
    over = captioned(img, "Stylized tiles laid over the ghosted prototype", 13, True)
    tp = sum(len(s) for k, s in pp.items()); ts = sum(len(s) for k, s in ps.items() if k != "Ground")
    rows = [("Part", "Prototype", "Stylized", "Share of the figure", "Shape")]
    shape = {"Crown":"tan mound to yellow fan", "Head":"gray patch to black disc", "Bill":"1-tile stub to red block",
             "Neck":"curved run to straight bar", "Body":"slanted mass to upright oval", "Legs":"bent stems to straight bars",
             "Feet":"scattered toes to one row"}
    for k in ["Crown","Head","Bill","Neck","Body","Legs","Feet"]:
        a, b = len(pp[k]), len(ps[k]); pa, pb = 100*a/tp, 100*b/ts
        d_ = pb - pa
        note = ("grew, %d%% to %d%%" if d_ >= 1 else "shrank, %d%% to %d%%" if d_ <= -1 else "held, %d%% to %d%%") % (round(pa), round(pb))
        rows.append((k, "%d tile%s" % (a, "" if a == 1 else "s"), "%d tile%s" % (b, "" if b == 1 else "s"), note, shape[k]))
    rows.append(("Figure", "%d tiles" % tp, "%d tiles" % ts, "", "ground band added: %d tiles" % len(ps["Ground"])))
    fb, fr = font(13, True), font(13)
    cw = [66, 90, 90, 160, 220]; rh = 26
    tbl = Image.new("RGB", (sum(cw) + 20, rh*len(rows) + 20), (255,255,255)); d = ImageDraw.Draw(tbl)
    for i, row in enumerate(rows):
        x = 10; y = 10 + i*rh
        if i == 0 or i == len(rows)-1: d.line([10, y + rh - 2, tbl.width - 10, y + rh - 2], fill=(120,110,90), width=1)
        for j, cellt in enumerate(row):
            d.text((x + 4, y + rh/2), cellt, fill=(40,35,25), font=fb if i == 0 else fr, anchor="lm"); x += cw[j]
    tbl = captioned(tbl, "Tiles per part, before and after", 13, True)
    tbl = captioned(tbl, "The identifying parts (crown, bill) take a larger share of the figure; the bulk (body) takes a smaller one. Every part also changed shape.", 12, width=tbl.width)
    img = hstack([over, tbl], gap=30, top=30)
    title(img, "Step 6. Exaggerate what identifies the figure, compact what does not", 10, 17)
    img.save(os.path.join(out, "Fig 5 - Exaggerate and Compact.png"))

def make_all(proto, styl, out):
    pp, ps = parts_proto(proto), parts_styl(styl)
    fig_two_levels(proto, styl, out)
    fig_parts(proto, styl, pp, ps, out)
    fig_simple_shapes(proto, styl, pp, ps, out)
    fig_grid_rules(proto, styl, pp, ps, out)
    fig_exaggerate(proto, styl, pp, ps, out)
    return pp, ps
