#!/usr/bin/env python3
import argparse, json, subprocess
from pathlib import Path
def run(cmd, capture=False, check=True):
    print(">>", " ".join(map(str, cmd))); return subprocess.run(cmd, check=check, capture_output=capture, text=True)
def choose_lang():
    test = run(["tesseract", "--list-langs"], capture=True, check=False).stdout.lower()
    return "oriogo" if "oriogo" in test else ("ces" if "ces" in test else "eng")
def parse_tsv(tsv_text: str):
    lines = tsv_text.strip().splitlines()
    if not lines: return {"full_text":"", "pages":[]}
    header = lines[0].split("\t"); idx = {k:i for i,k in enumerate(header)}
    pages = {}; full = []
    for line in lines[1:]:
        cols = line.split("\t")
        if len(cols)!=len(header): continue
        level = int(cols[idx["level"]]); page = int(cols[idx["page_num"]])
        left = int(cols[idx["left"]]); top = int(cols[idx["top"]]); width = int(cols[idx["width"]]); height=int(cols[idx["height"]])
        text = cols[idx["text"]]; conf = cols[idx["conf"]]
        try: conf = float(conf)
        except: conf = None
        if page not in pages: pages[page] = {"page_num":page, "words":[]}
        if level==5 and text.strip():
            pages[page]["words"].append({"text":text,"bbox":{"x":left,"y":top,"w":width,"h":height},"conf":conf})
            full.append(text)
    return {"full_text":" ".join(full).strip(), "pages":[pages[k] for k in sorted(pages)]}
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output_dir", required=True)
    ap.add_argument("--recursive", action="store_true")
    ap.add_argument("--psm", default="6")
    args = ap.parse_args()
    in_path = Path(args.input); out_root = Path(args.output_dir); out_root.mkdir(parents=True, exist_ok=True)
    files = []
    if in_path.is_file(): files=[in_path]
    else:
        pattern = "**/*" if args.recursive else "*"
        files = [p for p in in_path.glob(pattern) if p.suffix.lower() in {".tif",".tiff",".png",".jpg",".jpeg"}]
    lang = choose_lang(); print(f"[INFO] Lang: {lang}")
    for f in files:
        base = out_root / f.with_suffix("").name
        txt = run(["tesseract", str(f), "stdout", "-l", lang, "--psm", args.psm, "--oem", "1"], capture=True).stdout
        (base.with_suffix(".txt")).write_text(txt, encoding="utf-8")
        tsv = run(["tesseract", str(f), "stdout", "-l", lang, "--psm", args.psm, "--oem", "1", "tsv"], capture=True).stdout
        js = parse_tsv(tsv)
        (base.with_suffix(".json")).write_text(json.dumps(js, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Hotovo. Výstupy v: {out_root.resolve()}")
if __name__ == "__main__":
    main()
