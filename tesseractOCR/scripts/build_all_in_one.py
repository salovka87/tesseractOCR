#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
STEPS = [
    ("Download ces", "download_models.py"),
    ("Build starter", "build_starter_traineddata.py"),
    ("Generate synth", "generate_synth.py"),
    ("Make LSTMF", "make_lstmf.py"),
    ("Train oriogo", "train_oriogo.py"),
    ("Verify charset", "verify_charset.py"),
]
def run_py(script):
    print(f"\n=== {script} ===")
    subprocess.run([sys.executable, str(ROOT/"scripts"/script)], check=True)
def main():
    for _, s in STEPS: run_py(s)
    final = ROOT/"tessdata/oriogo.traineddata"
    if final.exists():
        print(f"\n✅ DONE: {final}\nUse: tesseract invoice.tif stdout --tessdata-dir ./tessdata -l oriogo --psm 6")
    else:
        print("\n❌ Build finished without oriogo.traineddata")
if __name__ == "__main__":
    main()
