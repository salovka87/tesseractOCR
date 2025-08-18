#!/usr/bin/env python3
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TXT = ROOT/"data/training_texts/training_text.txt"
OUT = ROOT/"data/synth/train"
REQ = ROOT/"data/charset/required_chars.txt"
FONTS = ["Open Sans","Arial","Times New Roman","Courier New","Calibri","Verdana","Tahoma","DejaVu Sans","DejaVu Serif","DejaVu Sans Mono","Noto Sans","Noto Serif","Roboto"]
SIZES = [12,14,16,18,20,22]
def run(cmd):
    print(">>", " ".join(map(str, cmd))); subprocess.run(cmd, check=True)
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for font in FONTS:
        for size in SIZES:
            base = OUT / f"oriogo_{font.replace(' ','_')}_{size}"
            cmd = ["text2image",f"--text={TXT}",f"--outputbase={base}",f"--fonts_dir=/usr/share/fonts:/usr/local/share/fonts:~/.fonts:~/Library/Fonts:/Library/Fonts",f"--font={font}",f"--ptsize={size}","--resolution=300","--xsize=2400","--ysize=3400","--exposure=0",f"--unicharset_file={REQ}","--leading=28","--char_spacing=0.0","--min_coverage=1"]
            try: run(cmd)
            except subprocess.CalledProcessError: print(f"⚠️ Font not available, skipped: {font}")
    print("✅ Synthetic TIFF+BOX in", OUT)
if __name__ == "__main__":
    main()
