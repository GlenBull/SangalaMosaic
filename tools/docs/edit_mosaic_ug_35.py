"""Sangala Mosaic User Guide 3.4 -> 3.5.

Brings the guide level with SangalaMosaic .102, which moved Settings out of the control
panel and into a panel under the gear (as Sangala Studio has always done), moved Fit to
Photo the other way - it acts on the design, so it belongs beside Build It! - and gave the
tile numbering its own labeled control, Key / Number the Tiles, which the guide had never
described at all.

Run-level edits on Glen's own file: every replacement sits inside a single <w:t>, so no
run is merged, no style is touched, and nothing outside the listed paragraphs moves. The
one new paragraph clones the pPr of the Show item it follows, so it numbers with the list.
"""
import re, shutil, zipfile, os, sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "Documents")
SRC  = os.path.join(DOCS, "User Guide (Ver 3.4).docx")
OUT  = os.path.join(DOCS, "User Guide (Ver 3.5).docx")

# paragraph index -> list of (exact text inside one run, replacement)
EDITS = {
  25: [(" (the gear — opens Setup: the grid and the baseplate), and ways of looking at it: ",
        " (the gear — opens a panel holding the grid, the baseplate, and the medium), and ways of looking at it: ")],
  28: [(" button and everything that shapes the result: the ",
        " button, Fit to Photo, and everything that shapes the result: the "),
       (". The grid, the baseplate, and the medium live in Setup, behind ",
        ". The grid, the baseplate, and the medium are not in this panel; they open under ")],
  56: [(" — one press lays the grid over the photo for you: ",
        " — in the Build panel, directly beneath Build It!, one press lays the grid over the photo for you: ")],
  57: [(" section of Setup (press ", " section of the panel that opens under "),
       ("), set how many tiles ", ", set how many tiles ")],
  81: [(" swatches in Setup (press ", " swatches in the panel that opens under "),
       ("). These are limited", ". These are limited")],
  83: [("Medium (in Setup) chooses", "Medium (in Settings) chooses")],
 111: [("sorted most-used first, and the grand total.",
        "sorted most-used first, and the grand total. Every line begins with that color’s key number, "
        "whether or not Number the Tiles is on, so the list and the chart agree.")],
 118: [("the printout lists the tile counts by color.",
        "the printout lists the tile counts by color, each with its key number.")],
 133: [("Fit to Photo (in Setup)", "Fit to Photo (in the Build panel)")],
 135: [("Across and Down in the Grid section", "Across and Down in Settings, under Grid Controls")],
 145: [("Medium (in Setup)", "Medium (in Settings)")],
}

# The new list item, cloned from the Show item's pPr so it takes the same number sequence.
KEY_PARA = (
 '<w:p w14:paraId="3F1A0C58" w14:textId="77777777" w:rsidR="00BF2667" w:rsidRDefault="00C348C6">'
 '<w:pPr><w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="20"/></w:numPr>'
 '<w:spacing w:after="60"/><w:contextualSpacing w:val="0"/>'
 '<w:rPr><w:rFonts w:eastAsia="Times New Roman"/></w:rPr></w:pPr>'
 '<w:r><w:rPr><w:i/><w:iCs/></w:rPr><w:t>Key</w:t></w:r>'
 '<w:r><w:t xml:space="preserve"> — one checkbox, </w:t></w:r>'
 '<w:r><w:rPr><w:rStyle w:val="Strong"/><w:rFonts w:eastAsia="Times New Roman"/></w:rPr>'
 '<w:t>Number the Tiles</w:t></w:r>'
 '<w:r><w:t xml:space="preserve">, off until you turn it on. Each color then gets a number, printed on '
 'every tile of that color, and a key beneath the mosaic names them. The colors run by family and, within '
 'a family, from the lightest tone to the darkest, so two that look alike in the hand — the grays, dark '
 'blue and black — can be told apart by the number on the chart. The same numbers appear on the printed '
 'sheet and in the Tile List.</w:t></w:r></w:p>'
)
AFTER = 58          # the Show item

def main():
    if os.path.exists(OUT):
        sys.exit("refusing to overwrite " + OUT)
    shutil.copy2(SRC, OUT)
    z = zipfile.ZipFile(SRC)
    names = z.namelist()
    blobs = {n: z.read(n) for n in names}
    z.close()

    xml = blobs["word/document.xml"].decode("utf-8")
    paras = re.findall(r"<w:p[ >].*?</w:p>|<w:p/>", xml, re.S)

    for idx, subs in EDITS.items():
        p = paras[idx]
        for old, new in subs:
            if p.count(old) != 1:
                sys.exit("paragraph %d: %r found %d times" % (idx, old, p.count(old)))
            p = p.replace(old, new, 1)
        if xml.count(paras[idx]) != 1:
            sys.exit("paragraph %d is not unique in the document" % idx)
        xml = xml.replace(paras[idx], p, 1)
        paras[idx] = p

    anchor = paras[AFTER]
    if xml.count(anchor) != 1:
        sys.exit("the Show paragraph is not unique")
    xml = xml.replace(anchor, anchor + KEY_PARA, 1)

    blobs["word/document.xml"] = xml.encode("utf-8")

    out = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
    out.writestr("[Content_Types].xml", blobs["[Content_Types].xml"])
    for n in names:
        if n != "[Content_Types].xml":
            out.writestr(n, blobs[n])
    out.close()
    print("wrote", OUT)

if __name__ == "__main__":
    main()
