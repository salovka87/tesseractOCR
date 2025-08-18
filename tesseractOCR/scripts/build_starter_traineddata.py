#!/usr/bin/env python3
import subprocess, sys, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TXT = ROOT/"data/training_texts/training_text.txt"
VENDOR = ROOT/"vendor/langdata_lstm"
UCHAR = ROOT/"langdata_oriogo/oriogo.unicharset"
LANGTXT = ROOT/"langdata_oriogo/oriogo.training_text"
STARTER = ROOT/"tessdata/oriogo-starter.traineddata"
def run(cmd):
    print(">>", " ".join(map(str, cmd))); subprocess.run(cmd, check=True)
def ensure_langdata():
    if VENDOR.exists(): return
    VENDOR.parent.mkdir(parents=True, exist_ok=True)
    run(["git","clone","--depth","1","https://github.com/tesseract-ocr/langdata_lstm", str(VENDOR)])
def main():
    (ROOT/"langdata_oriogo").mkdir(parents=True, exist_ok=True)
    ensure_langdata()
    LANGTXT.write_text(TXT.read_text(encoding="utf-8"), encoding="utf-8")
    run(["unicharset_extractor","--output_unicharset", str(UCHAR), str(LANGTXT)])
    run(["set_unicharset_properties","-U", str(UCHAR),"-O", str(UCHAR),"--script_dir", str(VENDOR)])
    run(["combine_lang_model","--input_unicharset", str(UCHAR),"--script_dir", str(VENDOR),"--lang","oriogo","--pass_through_recoder","1","--version_str","oriogo-starter"])
    gen = Path("oriogo.traineddata")
    if gen.exists():
        STARTER.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(gen), str(STARTER))
        print(f"✅ Starter created: {STARTER}")
    else:
        print("❌ Failed to create starter"); sys.exit(1)
if __name__ == "__main__":
    main()
