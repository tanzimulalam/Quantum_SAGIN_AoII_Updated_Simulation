"""Figure 1: the system model. The drawing is a TikZ source, paper/figures/system_model.tex (black and white, Font
Awesome icons, drawn at IEEE column width so the paper includes it without scaling). This script compiles it with
pdflatex into paper/figures/system_model.pdf, copies the PDF to figures/, and renders figures/system_model.png with
MiKTeX's Ghostscript (mgs) when it is available.
"""
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "paper" / "figures" / "system_model.tex"


def main():
    with tempfile.TemporaryDirectory() as tmp:
        cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"-output-directory={tmp}", SRC.name]
        run = subprocess.run(cmd, cwd=SRC.parent, capture_output=True, text=True)
        if run.returncode != 0:
            print(run.stdout[-3000:])
            raise SystemExit("pdflatex failed")
        pdf = Path(tmp) / "system_model.pdf"
        shutil.copy(pdf, SRC.with_suffix(".pdf"))
        (ROOT / "figures").mkdir(exist_ok=True)
        shutil.copy(pdf, ROOT / "figures" / "system_model.pdf")
        gs = shutil.which("mgs") or shutil.which("gswin64c") or shutil.which("gs")
        if gs:
            subprocess.run([gs, "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m", "-r300",
                            f"-sOutputFile={ROOT / 'figures' / 'system_model.png'}", str(pdf)], check=True)
    print("written", SRC.with_suffix(".pdf"), "and figures/system_model.pdf" + (" + .png" if gs else ""))


if __name__ == "__main__":
    main()
