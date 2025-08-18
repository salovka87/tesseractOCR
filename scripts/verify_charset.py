#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT/"tessdata/oriogo.traineddata"
REQ = ROOT/"data/charset/required_chars.txt"
TMP = ROOT/"build/oriogo"
def run(cmd): print(">>", " ".join(map(str, cmd))); return subprocess.run(cmd, check=True, capture_output=True, text=True)
def main():
    if not MODEL.exists(): print("❌ Model not found:", MODEL); sys.exit(1)
    TMP.parent.mkdir(parents=True, exist_ok=True)
    run(["combine_tessdata","-u", str(MODEL), str(TMP)])
    uni = (ROOT/"build/oriogo.lstm-unicharset")
    if not uni.exists(): print("❌ lstm-unicharset not found"); sys.exit(1)
    uni_text = uni.read_text(encoding="utf-8", errors="ignore")
    missing = []
    for ch in REQ.read_text(encoding="utf-8", errors="ignore"):
        if ch.strip() and ch not in "\n\r\t " and ch not in uni_text:
            missing.append(ch)
    if missing:
        print("⚠️ Missing chars:", "".join(sorted(set(missing)))); sys.exit(2)
    print("✅ Unicharset coverage OK.")
if __name__ == "__main__":
    main()
