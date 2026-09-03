"""Build the TILE_ELEMENT table in SangalaMosaic.html from LEGO's own Pick a Brick data.

A LEGO Pick a Brick order is a CSV of elementId,quantity - LEGO's own template - and an
element ID names SHAPE AND COLOR, so it cannot be derived from anything the page ships.
The source is pab_3070_elements.json beside this script: the verbatim response from LEGO's
searchElements API for design 3070 (FLAT TILE 1X1), read 2026-09-03. Every element in it
reports availability AVAILABLE.

A palette color is matched to an element BY LEGO'S OWN COLOR NAME, never by nearest hex.
Guessing is the one thing this must not do: an element ID names shape and color together,
so a wrong one orders the right tile in the wrong color - a mistake that arrives in a box
weeks later. A palette color LEGO does not mold as a 1x1 tile gets no element and is not
buildable in tiles; it stays in the array (saved .mosaic files index by position) but is
flagged so build(), retile() and the swatch panel skip it.

    python tools\tile_elements.py            (prints the block to paste, and the audit)
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "..", "SangalaMosaic.html")
DATA = os.path.join(HERE, "pab_3070_elements.json")


def palette():
    src = open(HTML, encoding="utf-8").read()
    i = src.index("const PALETTE = [")
    j = src.index("DOT_ONLY_FROM = PALETTE.length", i)
    tile = re.findall(r'name:"([^"]+)",\s*rgb:\[(\d+),(\d+),(\d+)\]', src[i:j])
    k = src.index("].forEach(p=>PALETTE.push", j)
    dot = re.findall(r'name:"([^"]+)",\s*rgb:\[(\d+),(\d+),(\d+)\]', src[j:k])
    return [t[0] for t in tile], [d[0] for d in dot]


def main():
    els = json.load(open(DATA, encoding="utf-8"))
    by = {}
    for e in els:
        if e.get("designId") != "3070":
            continue
        by[e["facets"]["color"]["name"].strip().lower()] = e
    tiles, dots = palette()
    pairs, missing, unused = [], [], set(by)
    for i, name in enumerate(tiles):
        e = by.get(name.strip().lower())
        if e:
            pairs.append((i, e["id"], name))
            unused.discard(name.strip().lower())
        else:
            missing.append((i, name))
    body = ",".join('"%d":"%s"' % (i, el) for i, el, _ in pairs)
    print("/* GENERATED - do not edit by hand. tools/tile_elements.py builds this from")
    print("   tools/pab_3070_elements.json, LEGO's own Pick a Brick response for design 3070")
    print("   (FLAT TILE 1X1). Key is the PALETTE index; the value is LEGO's element ID, which")
    print("   names the tile AND its color. A palette color absent here is one LEGO does not")
    print("   mold as a 1x1 tile - it cannot be built or ordered, only used as a dot. */")
    print("  const TILE_ELEMENT={%s};" % body)
    print()
    print("--- audit ---")
    print("elements in LEGO's response : %d" % len(by))
    print("palette tile colors         : %d" % len(tiles))
    print("orderable (have an element) : %d" % len(pairs))
    print("not molded as a 1x1 tile    : %d" % len(missing))
    for i, n in missing:
        print("      %2d  %s" % (i, n))
    if unused:
        print("LEGO colors with no palette entry (candidates to append):")
        for n in sorted(unused):
            print("      %-24s %s  %s" % (by[n]["facets"]["color"]["name"],
                                          by[n]["id"], by[n]["colorHex"]))
    print("dot-only colors (unchanged) : %d" % len(dots))


if __name__ == "__main__":
    main()
