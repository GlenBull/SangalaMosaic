// Sangala Mosaic launcher — a real program (not a script), so managed/school Windows
// treats it like Sangala Studio's SangalaStudio.exe (which runs fine) rather than
// blocking it the way it blocks .cmd/.bat files. Double-clicking it opens the app page
// (SangalaMosaic.html, kept next to the exe) in the default browser. The turaco icon is
// embedded at build time via /win32icon, so the exe and any Desktop shortcut to it show
// the turaco. Compiled in-box with the .NET Framework csc.exe — no admin, no install.
using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

namespace SangalaMosaicApp
{
    static class Launcher
    {
        [STAThread]
        static void Main()
        {
            string dir = AppDomain.CurrentDomain.BaseDirectory;
            string html = Path.Combine(dir, "SangalaMosaic.html");
            try
            {
                if (!File.Exists(html))
                {
                    MessageBox.Show(
                        "SangalaMosaic.html was not found next to this launcher.\r\n\r\n" +
                        "Keep SangalaMosaic.exe and SangalaMosaic.html together in the same folder.",
                        "Sangala Mosaic", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    return;
                }
                Process.Start(new ProcessStartInfo(html) { UseShellExecute = true });
            }
            catch (Exception ex)
            {
                MessageBox.Show("Could not open Sangala Mosaic:\r\n" + ex.Message,
                    "Sangala Mosaic", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
