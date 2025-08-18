#!/usr/bin/env python3
import argparse, json, subprocess
from pathlib import Path
import cv2, numpy as np
def run(cmd, capture=False, check=True):
    print(">>", " ".join(map(str, cmd))); return subprocess.run(cmd, check=check, capture_output=capture, text=True)
def color_name(bgr):
    names = {"red":(0,0,255),"green":(0,255,0),"blue":(255,0,0),"cyan":(255,255,0),"magenta":(255,0,255),"yellow":(0,255,255),"orange":(0,165,255),"purple":(128,0,128),"black":(0,0,0),"white":(255,255,255)}
    import math; best, db = None, 1e9
    for n, ref in names.items():
        d = math.dist(bgr, ref)
        if d<db: db=d; best=n
    return best
def detect_boxes(img):
    b,g,r = cv2.split(img)
    spread = cv2.max(cv2.max(cv2.absdiff(r,g), cv2.absdiff(r,b)), cv2.absdiff(g,b))
    _, mask = cv2.threshold(spread, 40, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3,3), np.uint8), iterations=1)
    contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes=[]
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if w*h<800: continue
        pts = cnt.reshape(-1,2); cols = img[pts[:,1], pts[:,0]]
        med = np.median(cols, axis=0).astype(np.uint8)
        color_hex = "#{:02x}{:02x}{:02x}".format(int(med[2]), int(med[1]), int(med[0]))
        boxes.append({"bbox":{"x":int(x),"y":int(y),"w":int(w),"h":int(h)},"color":{"name": color_name(tuple(med.tolist())), "hex": color_hex},"median_bgr":[int(med[0]),int(med[1]),int(med[2])]})
    boxes.sort(key=lambda b:(b["bbox"]["y"], b["bbox"]["x"]))
    return boxes
def choose_lang():
    langs = run(["tesseract","--list-langs"], capture=True, check=False).stdout.lower()
    return "oriogo" if "oriogo" in langs else ("ces" if "ces" in langs else "eng")
def tesseract_crop_text(crop, lang, psm="6"):
    import tempfile, uuid, os
    tmp = Path(tempfile.gettempdir())/f"crop_{uuid.uuid4().hex}.png"
    cv2.imwrite(str(tmp), crop)
    try: out = run(["tesseract", str(tmp), "stdout", "-l", lang, "--psm", psm, "--oem", "1"], capture=True).stdout
    finally:
        try: os.remove(tmp)
        except: pass
    return out.strip()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output_dir", required=True)
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--psm", default="6")
    args = ap.parse_args()
    in_path = Path(args.input); out_root = Path(args.output_dir); out_root.mkdir(parents=True, exist_ok=True)
    files = [in_path] if in_path.is_file() else sorted(in_path.rglob("*.png"))
    if not files: raise SystemExit("No PNGs found.")
    lang = choose_lang()
    for f in files:
        img = cv2.imread(str(f), cv2.IMREAD_COLOR)
        if img is None: print("[WARN] cannot read", f); continue
        det = detect_boxes(img)
        results=[]
        for d in det:
            x,y,w,h = d["bbox"]["x"], d["bbox"]["y"], d["bbox"]["w"], d["bbox"]["h"]
            x2,y2=max(x+2,0),max(y+2,0); w2,h2=max(w-4,1),max(h-4,1)
            crop = img[y2:y2+h2, x2:x2+w2]
            txt = tesseract_crop_text(crop, lang, psm=args.psm)
            results.append({"bbox": d["bbox"], "color": d["color"], "text": txt})
        out_json = out_root/(f.stem+".layout.json")
        out_json.write_text(json.dumps({"file": f.name, "boxes": results}, ensure_ascii=False, indent=2), encoding="utf-8")
        if args.debug:
            import cv2
            dbg = img.copy()
            for r in results:
                x,y,w,h = r["bbox"]["x"], r["bbox"]["y"], r["bbox"]["w"], r["bbox"]["h"]
                hx = r["color"]["hex"].lstrip("#"); rgb = tuple(int(hx[i:i+2],16) for i in (0,2,4))
                cv2.rectangle(dbg, (x,y), (x+w, y+h), (rgb[2],rgb[1],rgb[0]), 2)
            (out_root/(f.stem+".debug.png")).write_bytes(cv2.imencode(".png", dbg)[1].tobytes())
        print(f"✅ {f.name}: {len(results)} boxes → {out_json.name}")
    print("Done:", out_root.resolve())
if __name__ == "__main__":
    main()
