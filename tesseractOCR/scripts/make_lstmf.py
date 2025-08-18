#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SYN = ROOT/"data/synth/train"
LSTMF = ROOT/"data/lstmf"
LIST = ROOT/"data/lstmf/list.train"
def run(cmd): print(">>", " ".join(map(str, cmd))); subprocess.run(cmd, check=True)
def main():
    LSTMF.mkdir(parents=True, exist_ok=True)
    tifs = sorted(SYN.glob("*.tif"))
    if not tifs: print("❌ No .tif in", SYN); sys.exit(1)
    paths = []
    for tif in tifs:
        base = LSTMF / tif.stem
        run(["tesseract", str(tif), str(base), "--psm", "6", "lstm.train"])
        paths.append(str(base)+".lstmf")
    LIST.parent.mkdir(parents=True, exist_ok=True)
    LIST.write_text("\n".join(paths), encoding="utf-8")
    print(f"✅ Created {LIST} ({len(paths)} lines)")
if __name__ == "__main__":
    main()
