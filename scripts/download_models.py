#!/usr/bin/env python3
import urllib.request
from pathlib import Path
TESSDATA = Path("tessdata")
URLS = {"ces": "https://github.com/tesseract-ocr/tessdata_best/raw/main/ces.traineddata"}
def main():
    TESSDATA.mkdir(parents=True, exist_ok=True)
    out = TESSDATA/"ces.traineddata"
    if out.exists():
        print(f"✅ {out.name} already present"); return
    print(f"⬇️  Downloading {out.name} ...")
    urllib.request.urlretrieve(URLS["ces"], out)
    print(f"✅ Saved {out}")
if __name__ == "__main__":
    main()
