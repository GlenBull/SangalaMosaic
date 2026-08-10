"""Screenshot Sangala Mosaic headlessly, for the User Guide's figures.

The application is one self-contained HTML file whose script is an IIFE, so nothing can be called
from outside it. A temporary COPY of the page is written with a setup script appended; that script
only does what a user would do - it hands a saved .mosaic to the real file input and clicks real
buttons - so what is captured is the application's own output, not a mock-up.
"""
import json, os, subprocess, sys, tempfile

APP = r"D:\Code Projects\Mosaic\SangalaMosaic.html"
PROJ = r"D:\Code Projects\Mosaic\Projects"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")
EDGE = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]

SETUP = """
<script>
(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const proj = %s;                      // the saved project, embedded so nothing has to be fetched
  const f = new File([proj], "%s", {type: "application/json"});
  const dt = new DataTransfer(); dt.items.add(f);
  const inp = document.getElementById("file");
  inp.files = dt.files;
  inp.dispatchEvent(new Event("change", {bubbles: true}));
  await wait(1200);                     // FileReader + image decode + the rebuild
  %s                                    // per-figure extra steps
  document.title = "SHOT-READY";
})();
</script>
"""


def edge():
    for p in EDGE:
        if os.path.exists(p):
            return p
    raise SystemExit("Microsoft Edge not found")


def shoot(name, project, extra="", size=(1500, 950), settle=2500):
    os.makedirs(OUT, exist_ok=True)
    html = open(APP, encoding="utf-8").read()
    proj_text = open(os.path.join(PROJ, project), encoding="utf-8").read()
    html += SETUP % (json.dumps(proj_text), project, extra)
    png = os.path.join(OUT, name + ".png")
    if os.path.exists(png):
        os.remove(png)
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "shot.html")
        open(page, "w", encoding="utf-8").write(html)
        subprocess.run([edge(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2",          # 2x, so the figure stays sharp in print
                        "--virtual-time-budget=%d" % settle,
                        "--screenshot=" + png, "--window-size=%d,%d" % size,
                        "file:///" + page.replace("\\", "/")],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    print(("%-22s %s" % (name, "%d bytes" % os.path.getsize(png) if os.path.exists(png) else "NOT WRITTEN")))
    return png


if __name__ == "__main__":
    shoot(sys.argv[1] if len(sys.argv) > 1 else "screen", "Sample.mosaic")
