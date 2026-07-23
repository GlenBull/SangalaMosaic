# Sangala Mosaic — project guide for Claude Code

A browser tool that turns a photo into a **LEGO-tile mosaic** a person can build by hand on a
baseplate. Import a photo, remove its background, frame it under a grid, and map it to a grid of
1×1 tiles (target 32×32, the standard baseplate) using **only the tile colors the builder actually
owns** — then read off a build chart and a parts list. Built for the same course and the same
schools as Sangala Studio; piloted by Moses Kumenya at Hawthorne-Scribner High School in the
Mt. Elgon region of Uganda, where a student's animal (the buffalo, the crested crane) becomes a
mosaic.

**This is a SEPARATE app from Sangala Studio, deliberately.** It shares the look and feel and can
borrow code, but it lives in its own repo so Sangala Studio does not get overloaded. It may be
folded into Sangala Studio later; for now, keep them apart. The sibling project is
`D:\Code Projects\Silhouette Tools` (Sangala Studio).

## What makes this different from Sangala Studio
- **No bridge.** Sangala Studio carries a C# USB bridge because it drives a die cutter. Sangala
  Mosaic drives nothing — it outputs a chart and a parts list a person builds by hand. So it is a
  **single self-contained HTML file, pure browser, no server, no USB, no install.** Do not add a
  bridge. If a print is ever needed, it prints from the browser.
- Everything else about the environment is inherited from Sangala Studio: **no admin rights, no
  install, works offline.** This constraint is absolute — the schools have no admin access.

## The feature that matters most (do not lose sight of it)
**Build to the tiles you actually have.** A generic photo-to-pixels filter is a toy; what makes
this a build tool is mapping to a chosen SET of real tile colors and telling the builder how many
of each they need.
- Quantize to a palette that IS the builder's inventory, not "reduce to N colors."
- Preload real LEGO 1×1 tile colors (BrickLink RGB values); let the builder check which they own.
- Produce a **bill of materials** — "47 black, 23 white, 8 red…" — and optionally cap a color at
  the number owned, letting the next-nearest available color absorb the overflow.
This is the through-line. Resolution/pixelation sliders and pretty previews are secondary to it.

## Agreed feature plan (2026-07-23, from the design discussion)
Priority order, not a checklist to rush:
1. **Palette-constrained mapping + bill of materials** (above). The centerpiece.
2. **Photo layer** — import .jpg/.png, remove background offline, move/resize/zoom as a floating
   layer under the grid. *Borrowable* from Sangala Studio (see below).
3. **Grid layer** — a W×H grid (default 32×32) slid independently over the photo to set framing;
   physical-size readout (32 × 8 mm ≈ 256 mm ≈ 10 in); optional seams where baseplates meet.
   "Resolution" and "grid size" are the SAME knob here — the baseplate fixes it.
4. **Per-tile manual override** — click a cell, pick a color. Auto never nails eyes/faces (the
   buffalo's eyes were hand-placed). Essential, not optional.
5. **Printable build chart** — coordinates (A1…) and a per-row run-length readout
   ("row 12: 5 black, 3 white, 2 black"), the way mosaic/cross-stitch patterns are followed.
6. **Image prep that earns its place at low resolution** — contrast/levels BEFORE quantizing
   (a photo crushed to ~10 colors goes to mud otherwise); a dither toggle **default OFF** (flat
   blocks — cluster-then-mode — usually beat Floyd–Steinberg under big tiles); background-fill
   color for the removed background (those cells become real tiles).
Deferred/out of scope, on purpose: generic filters (hue/saturation, art effects), any SVG or
print-and-cut export (nothing is cut — tiles are placed), anything 3D. Those belong to Sangala
Studio; pulling them in is the overloading this split is meant to avoid.

## Sharing look and feel with Sangala Studio
- The look is shared by **copying**, not by a live dependency. The CSS classes (`denim`, `cork`,
  `marker`, `header`/`logo`/`tbtn`/`menu`, `stage`/`panel`/`board`, form controls) are lifted from
  `Silhouette Tools/SangalaStudio.html`. When Studio's styling changes, port the change over
  deliberately — there is no automatic link, and that is on purpose (no coupling to break).
- The **buffalo icon** (inline base64) is shared as the About button, so the two apps read as one
  family. Keep it inline — the single-file, self-contained rule holds here too.
- Subtitle under the brand is **"Mosaic Design Tool"** — Title Case, every word capitalized
  including "Tool" (Glen confirmed 2026-07-23). Sangala Studio's subtitle was changed to match:
  "Digital Fabrication Tool", also Title Case.

## Borrowable code (copy, do not link)
- **Photo import + background removal + move/resize** already exist in Sangala Studio as the
  `refImg` layer (`SangalaStudio.html`) using `assets/imagetracer_v1.2.6.js`, offline. When we
  build the photo layer, PORT those functions across — copy them, keep this app self-contained.

## Conventions (same house rules as Sangala Studio)
- **American spelling everywhere** — color, center, gray, behavior. US project, US course.
- **NEVER write "honest", "honestly", "genuinely", or "straightforward"** — anywhere. Say the
  thing plainly. (Glen has had to correct this repeatedly in the sibling project.)
- Be concise and direct; prose over bullet lists unless a list is warranted. Do NOT use popup
  question dialogs — ask inline, one question at a time.
- The mosaic is built from 1×1 **tiles** (square, flat) placed on a baseplate; the **studs** the
  tiles snap onto are round. Do not conflate tiles and studs.
- **One change at a time, then let Glen test, then commit.** Commit after each verified-good state
  so a regression is a `git diff` away.

## Build & run
Single file: open `SangalaMosaic.html` in a browser. No build step, no server. UI-only, so a
change is just a refresh. Version marker on line 2 (`SANGALA_MOSAIC_VERSION`) follows the same
date convention as Sangala Studio; bump it on any shipped change.

## Approval & git
- **Standing approval (same as Sangala Studio):** work confined to THIS repo, the temp scratch
  folder, and pushing commits to this repo's GitHub once a remote exists. No need to ask.
- **Always ask first:** anything outside this repo, system/account settings, creating the GitHub
  remote, and any history-losing git (force-push, hard reset dropping commits, branch deletion).
- Remote is live: **https://github.com/GlenBull/SangalaMosaic** (public, branch `main`). Standing
  approval covers pushing to it.

## Current state (as of 2026-07-23)
- **Four-region layout** matching Studio: denim menu bar, left tool rail, cork workspace, right
  "Build" control panel. Subtitle "Mosaic Design Tool" (Title Case).
- **The workspace is a free compositor** (`SangalaMosaic.html`, one `<script>` IIFE):
  - `layers[]` — image layers. Each **Open/drop ADDS** an image (mountains behind, a buffalo in
    front = a composite), placed at native size, downscaled only to fit (never upscaled, so it
    stays crisp). Click to select; drag the body to move; drag a corner handle to resize
    (aspect-locked, opposite corner anchored) — Studio's refImg interaction. Delete key removes
    the selected image.
  - `frame` — the **grid region**, a movable/resizable frame (drag its border to move, corner to
    resize; aspect locked to the grid, so cells stay square). It carries the cell lines and the
    coordinate labels (numbers 1..gw across the top, letters A..Z, AA.. down the left, drawn just
    OUTSIDE the frame with a white halo). Changing Across/Down reshapes it. The mosaic will be
    whatever falls inside this frame. *Show grid* toggles the cells+labels; the frame border stays.
  - Rendered at device resolution (`dpr`) for crisp pixels. Canvas fills the board; objects hold
    absolute coords. Layers have a `draw` source separate from `img`, so **Remove background**
    (a per-image toggle in the Selected panel; flood-fill from the corners + feather + decontaminate)
    swaps a transparent version in without losing the original.
- **Build It! is live** (the centerpiece). `PALETTE` is ~25 real LEGO solid tile colors, each with
  an `own` flag; the swatch row toggles ownership (click). The pipeline (toward the "gold standard"
  clean look, per the design discussion): sample the framed composite to an offscreen (smoothing OFF,
  8/cell) → **average** each cell's non-background samples (flattens feather texture) → **k-means to
  K colors** (the `Colors` slider) and snap each group to its nearest OWNED tile (a textured body
  becomes one gray, not five) → **cleanup** (two gentle passes: fill pinholes, drop lone strays,
  recolour outvoted speckle; conservative so 1-tile legs survive). Fills the **bill of materials**
  (counts per colour; total = TILED cells). Options: **Ignore background** (default on — samples a
  `removeBg`-isolated copy per layer so the backdrop is empty and thin parts survive), **Colors**,
  **Clean up**, **Contrast**, **Brightness**; changing any re-maps live once a mosaic exists. The
  menu **View** button toggles photo↔mosaic; any edit to the composite invalidates it (`invalidate()`).
- The workspace is **pinned to the viewport** (body flex column, 100vh, overflow hidden); the panel
  scrolls internally if tall — no page scroll.
- Still disabled placeholders: **Print chart** (would print the chart + BOM), **Settings** (image
  prep), and the left tools (Photo/Frame/Paint/Pick — redundant with direct manipulation; decide
  whether to repurpose or drop). No dither/contrast controls yet.
- Test material in `images/`: `Crested Crane.png`, `African Buffalo (LEGO).jpg`, the crane/buffalo
  reference mosaics, `Samweli Wanda.png`.
- **Agreed direction (2026-07-23):** the auto-conversion gets you ~80% toward the "gold standard"
  hand-built mosaic; the rest is hand cleanup. So **the Paint tool is the priority next step** — click
  a cell to set its tile by hand, to fix legs/silhouette/features after Build. Then: **background
  fill** (fill empty cells with a chosen tile — the green baseplate + a grass row); owned-tile
  *quantities* (cap a colour, overflow to next-nearest); Print chart (numbered chart + parts list);
  porting Studio's ML background removal (u2netp) for busy backgrounds; optional dither.
