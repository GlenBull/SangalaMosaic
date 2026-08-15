"""Sangala Mosaic Technical Manual, Ver 1.0 - the script the document is built from.

Formatting comes from Sangala Studio's makedocx, imported rather than copied, so the three
applications' documents keep one format. The manual follows Studio's 3.6 and Blocks' 1.1 in shape:
the same numbered sections, a glossary, and an appendix.
"""
import sys
sys.path.insert(0, r"D:\Code Projects\Silhouette Tools\tools")
from makedocx import Doc

OUT = r"D:\Code Projects\Mosaic\Documents"

d = Doc()
d.title("Sangala Mosaic Technical Manual")

d.body("This manual describes how Sangala Mosaic is built, how its parts fit together, and what a "
       "developer needs to know before changing it. The companion User Guide describes how the "
       "application is used. Matters common to all three Sangala applications — the shared repository, "
       "the branch and pull request workflow, and the conventions the family holds to — are covered by "
       "the Sangala Tools Technical Manual and are referred to here rather than repeated.")

# ---------------------------------------------------------------- 1
d.heading("1. Downloading and Installing")
d.body("What is needed: a computer with a web browser. Nothing else, and nothing is installed.")
d.body("The repository is obtained from GitHub:", before_list=True)
d.code("https://github.com/GlenBull/SangalaMosaic")
d.body("The application is the single file SangalaMosaic.html, which runs by being opened in a "
       "browser. Two conveniences travel with it. Create Desktop Shortcut.cmd puts a turaco icon on "
       "the Desktop that opens the page, and Update SangalaMosaic.cmd fetches the current version "
       "from GitHub, checks that what arrived is a complete page, and swaps it in only when the "
       "version differs — keeping the previous copy as a backup. Running the updater on its own is "
       "enough to install the application, since it will fetch the page and the icon and then make "
       "the shortcut.")
d.body("A small launcher program, built once from SangalaMosaicLauncher.cs, is offered for managed "
       "Windows computers, which block a .cmd file but run a compiled program.")

# ---------------------------------------------------------------- 2
d.heading("2. What Sangala Mosaic Is, and the Rule That Shapes It")
d.body("Sangala Mosaic turns a photograph into a mosaic of 1 x 1 LEGO tiles that a person builds by "
       "hand on a baseplate. A photograph is placed under a grid, the grid is framed over the part "
       "that matters, and each cell of the grid becomes one tile in one of the colors the palette "
       "holds. The application produces a picture to build from and a list of the tiles it takes.")
d.body("ONE CONSTRAINT SHAPES THE CODE: the application drives nothing. Sangala Studio carries a "
       "local bridge because it operates a die cutter; Sangala Blocks carries one because it runs a "
       "renderer. Mosaic outputs a chart and a list that a person follows, so it is a single "
       "self-contained HTML file — no server, no bridge, no installation, and it works offline. Do "
       "not add a bridge. If something must be printed, it prints from the browser.")
d.body("A SECOND RULE GOVERNS THE WORDING RATHER THAN THE CODE. The palette is the set of colors the "
       "mosaic uses. Matching it to the tiles a builder owns is one way to work, never the frame: a "
       "student may design first and obtain tiles afterward. Interface text and documentation stay "
       "neutral on that point, and the parts list is the list to order from or build against.")

# ---------------------------------------------------------------- 3
d.heading("3. Architecture")
d.body("One file, one script, one canvas.", before_list=True)
d.item("The Page. ", "SangalaMosaic.html, about 2,000 lines: markup, style and a single script "
                     "holding the compositor, the palette, the mapping pipeline, the hand-editing "
                     "tools and the file writers.")
d.item("The Canvas. ", "A live compositor rather than a series of views. Photographs, the grid and "
                       "the built mosaic all occupy one canvas at once and are all draggable at any "
                       "time.")
d.item("The Launcher. ", "SangalaMosaic.exe, compiled from a few lines of C#, which does nothing but "
                         "open the page. It exists because managed school computers block scripts and "
                         "allow programs.")
d.body("THE WORKSPACE IS MODELESS, by decision rather than by accident. There is no photograph mode, "
       "no mosaic mode and no compare view; earlier versions had them and they were removed. One "
       "canvas always shows the photographs, the grid over them, and — once built — the mosaic drawn "
       "inside the grid. Comparing a mosaic with its source is done by dragging the photograph "
       "alongside it.")

# ---------------------------------------------------------------- 4
d.heading("4. Repository Layout")
d.table("Table 1. What Each File and Folder Holds",
        ["Path", "What it is"],
        [["SangalaMosaic.html", "The whole application, in one file"],
         ["SangalaMosaicLauncher.cs", "The launcher, for computers that block scripts"],
         ["SangalaMosaic.exe", "The built launcher, committed so it need not be rebuilt"],
         ["Build SangalaMosaic Launcher.cmd", "Compiles the launcher with the in-box compiler"],
         ["Update SangalaMosaic.cmd", "Fetches the current page from GitHub"],
         ["Create Desktop Shortcut.cmd", "Puts the turaco icon on the Desktop"],
         ["Turaco.ico", "The application icon, a Mt. Elgon turaco"],
         ["Documents\\", "This manual, the User Guide and the About document"],
         ["Images\\", "Test photographs and reference mosaics"],
         ["Projects\\", "Sample .mosaic files"],
         ["tools\\", "Scripts: the icon builder, the screenshot tool, the document generators"]],
        weights=[38, 62])

# ---------------------------------------------------------------- 5
d.heading("5. Build and Run")
d.body("There is no build step. The page is opened and it runs; a change to it is a browser refresh. "
       "Only the launcher is compiled, once, with the .NET compiler already present in Windows.")
d.body("The page carries a version marker as an HTML comment on its second line, "
       "SANGALA_MOSAIC_VERSION, following the same date convention as the other two applications. "
       "The updater compares that marker and does nothing when it matches, so the marker must be "
       "raised on any change that ships or the updater will report that a stale copy is current.")

# ---------------------------------------------------------------- 6
d.heading("6. The Browser Interface")
d.body("Four regions, carrying the family's names: the menu bar across the top, the Toolbar down the "
       "left, the workspace, and the control panel down the right. The look is shared with Sangala "
       "Studio by copying rather than by a live dependency — the style classes were lifted across "
       "deliberately, and a change to one application's appearance is made in both.")
d.body("The workspace is pinned to the viewport and the control panel scrolls within itself, so the "
       "page never scrolls as a whole. The canvas is rendered at the device's own pixel ratio, so "
       "tiles and cell lines stay crisp on a high-resolution screen.")

# ---------------------------------------------------------------- 7
d.heading("7. The Compositor")
d.body("Two kinds of object share the canvas, and both are moved by direct manipulation rather than "
       "by a tool.", before_list=True)
d.item("Image Layers. ", "Every Open or drop ADDS a photograph rather than replacing one, so a scene "
                         "can be composed — a landscape behind, an animal in front. Each is placed at "
                         "its native size, scaled down only if it will not fit, and never scaled up. "
                         "Dragging the body moves it; dragging a corner resizes it with the aspect "
                         "ratio locked and the opposite corner anchored.")
d.item("The Frame. ", "The grid region: a movable, resizable frame whose aspect ratio is locked to "
                      "the grid so cells stay square. It carries the cell lines and the coordinate "
                      "labels — numbers across the top, letters down the side — drawn just outside "
                      "it. Whatever falls inside the frame becomes the mosaic.")
d.body("Background removal is a per-image toggle. It floods in from the corners, feathers the edge "
       "and decontaminates the fringe, and it produces a SEPARATE drawing source rather than "
       "replacing the photograph, so the original is never lost and the toggle is reversible.")

# ---------------------------------------------------------------- 8
d.heading("8. The Palette and the Baseplate")
d.body("The palette holds 43 real LEGO tile colors, each with a name and an RGB value taken from the "
       "manufactured color rather than chosen by eye, and a flag recording whether the builder has "
       "it. The baseplate is chosen from eight colors LEGO actually makes baseplates in, so the "
       "preview shows something that can exist.")
d.body("ONE RULE ABOUT THE PALETTE IS ABSOLUTE: NEW COLORS ARE APPENDED AT THE END. A saved .mosaic "
       "file records each cell as an index into this array, so inserting a color in the middle or "
       "reordering the list silently recolors every mosaic ever saved. Appending cannot do that.")
d.body("The built mosaic is drawn on a studded baseplate, with each tile raised above it by a bevel, "
       "a shadow and a seam, so a tile reads as placed rather than painted. Empty cells show the "
       "bare plate. The plate is cached and redrawn only when it changes, since it is the most "
       "expensive thing on the canvas.")

# ---------------------------------------------------------------- 9
d.heading("9. How a Mosaic Is Built")
d.body("Build It! is the centerpiece, and it runs a pipeline rather than a filter. Each stage exists "
       "because the stage before it is not enough:", before_list=True)
d.step("The framed composite is sampled to an offscreen canvas with image smoothing turned OFF, "
       "eight samples to a cell.")
d.step("Each cell AVERAGES its non-background samples, which flattens the texture that feathering "
       "and photographic noise leave behind.")
d.step("Those averages are clustered by k-means into the number of colors the Colors control asks "
       "for, and each cluster is snapped to its nearest available tile color. Clustering before "
       "snapping is what makes a textured animal one gray rather than five.")
d.step("Two gentle cleanup passes fill pinholes, drop lone strays and recolor outvoted speckle. They "
       "are deliberately conservative, so that a leg one tile wide survives.")
d.body("The result fills the bill of materials — the count of each color, totaling the tiled cells. "
       "Changing any option remaps immediately once a mosaic exists.")
d.body("THE MOSAIC IS A SNAPSHOT, AND ONLY BUILD IT! MAKES ONE. Moving or resizing the grid or a "
       "photograph, adding or deleting images, toggling background removal or a tile color: none of "
       "these disturb an existing mosaic. Only a change to the grid's cell count discards it, "
       "because the mosaic no longer has the same number of cells to occupy. That rule is what "
       "allows everything on the canvas to stay draggable after a build.")

# ---------------------------------------------------------------- 10
d.heading("10. Hand Editing")
d.body("Automatic conversion gets most of the way; faces and eyes are placed by hand. Three tools in "
       "the Toolbar work on a built mosaic: Paint sets cells to the current color by click or drag "
       "and clears them on a right-click, Erase clears them back to bare plate, and Pick samples a "
       "cell's color and switches to Paint.")
d.body("UNDO IS BY STROKE, NOT BY CELL. One press-drag-release is one step, however many cells it "
       "crossed, so an accidental line across the mosaic is reverted by a single Ctrl-Z rather than "
       "forty. Each stroke accumulates the before and after value of every cell it touches and is "
       "committed as one entry when the button is released; undo and redo replay the net value per "
       "cell without re-recording themselves. A fresh build clears the history, because it discards "
       "the hand edits the history refers to.")

# ---------------------------------------------------------------- 11
d.heading("11. The Project File")
d.body("A .mosaic file is JSON and is SELF-CONTAINED: each photograph is embedded in it as a PNG "
       "data URL, alongside the frame, the grid size, the built mosaic with its cell indices and "
       "counts, which colors are owned, the baseplate, the visibility checkboxes, the options and "
       "the paint color. A student can carry one file between computers and lose nothing.")
d.body("Opening one restores all of it, reloading each embedded photograph in order and re-running "
       "background removal for the layers that had it. There is ONE Open rather than a separate "
       "Load: the file input accepts photographs and project files alike and dispatches on what "
       "arrives, and drag-and-drop goes through the same path. Opening a project asks before "
       "replacing work on screen.")
d.body("Saving uses the browser's native Save dialog, so the person chooses the folder and the name. "
       "A plain download is the fallback only where that dialog does not exist. It is not to be "
       "reverted to a download: writing files to the Downloads folder without asking was a defect, "
       "not a shortcut.")

# ---------------------------------------------------------------- 12
d.heading("12. What the Application Writes")
d.body("Everything is reached from the one Save menu, which offers the project and the image, with "
       "the image disabled until a mosaic exists. Print is beside it in the menu bar.")
d.body("THE PICTURE IS WHAT THE SCREEN SHOWS. The saved image and the printed page are produced by "
       "the same offscreen render, and both honor the three visibility checkboxes: the baseplate if "
       "it is shown, the tiles, the cell lines and coordinate labels when the grid is on, and the "
       "outline when the box is on. Grid on therefore yields a printable build chart with "
       "coordinates a student can follow away from the computer. With the baseplate hidden the image "
       "is written with a transparent background.")
d.body("Printing sets that same picture into a hidden element and calls the browser's print, with a "
       "print stylesheet that hides everything else on the page — so what prints is the mosaic and "
       "nothing around it.")

# ---------------------------------------------------------------- 13
d.heading("13. Verifying Changes")
d.body("A change is tested by refreshing the browser; there is nothing to rebuild. Beyond that:",
       before_list=True)
d.item("Test the Round Trip, Not the Save. ", "Saving is only half of a project file. Save, open the "
                                              "result, and compare what returns — the photographs, "
                                              "the mosaic, the counts and the checkboxes.")
d.item("Watch the Palette Indices. ", "Any change to the palette array is a change to the meaning of "
                                      "every saved file. Append, and check an old file still opens "
                                      "in its own colors.")
d.item("Check What a Build Discards. ", "Hand edits are lost by a rebuild and by a grid resize, and "
                                        "by nothing else. A change that widens that set takes work "
                                        "away from a student without saying so.")

# ---------------------------------------------------------------- 14
d.heading("14. Contributing")
d.body("Work proceeds one change at a time: make the change, let it be tested, then commit. Commit "
       "messages record why a change was made and what remains unverified, since the reasoning is "
       "what a later reader needs and the code already states what was done.")
d.body("Sangala Mosaic is a separate application from Sangala Studio on purpose. It shares the look "
       "and borrows code by copying, so that neither is coupled to the other; a feature that belongs "
       "to Studio — cutting, vector export, anything three-dimensional — is not to be pulled in here. "
       "That restraint is what the split exists to protect.")

# ---------------------------------------------------------------- 15
d.heading("15. Glossary")
d.table("Table 2. Terms Used in This Manual",
        ["Term", "Meaning"],
        [["Baseplate", "The studded plate the mosaic is built on, in one of eight LEGO colors"],
         ["Bill of materials", "The count of each tile color the mosaic uses"],
         ["Cell", "One square of the grid, which becomes one tile"],
         ["Composite", "The photographs on the canvas, taken together, as the grid sees them"],
         ["Frame", "The movable grid region; whatever falls inside it becomes the mosaic"],
         ["Layer", "One imported photograph on the canvas"],
         ["Palette", "The set of tile colors available to the mosaic"],
         ["Snapshot", "The built mosaic, which only Build It! remakes"],
         ["Stroke", "One press-drag-release of a hand-editing tool: one undo step"],
         ["Tile", "A flat 1 x 1 LEGO piece. The studs it snaps onto are round; the tile is square"]],
        weights=[26, 74])

d.heading("Appendix A. What Is Deliberately Absent")
d.body("Several things a reader might expect are missing on purpose, and adding them would undo a "
       "decision rather than fill a gap.")
d.body("There is no bridge and no server, because the application drives no machine. There is no "
       "vector export and no cutting, because nothing here is cut — tiles are placed. There is "
       "nothing three-dimensional. Those belong to Sangala Studio, and pulling them in is the "
       "overloading that keeping two applications apart is meant to prevent.")
d.body("Dithering is absent for a different reason: under tiles this large, flat blocks read better "
       "than a scattered approximation, so clustering is preferred to error diffusion. Generic image "
       "filters are absent because contrast and brightness before quantizing are what a photograph "
       "crushed to a few dozen colors actually needs, and the rest is decoration.")
d.body("Two things are absent only because they are not built yet: capping a color at the number of "
       "tiles a builder owns and letting the next-nearest color absorb the overflow, and a printed "
       "parts list beside the printed chart.")

print(d.save(OUT, "Tech Manual"))
