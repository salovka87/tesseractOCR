#!/usr/bin/env python3
import argparse, json, subprocess, re
from pathlib import Path
import numpy as np
def run_tesseract(img, lang, psm="6"):
    return subprocess.run(["tesseract", str(img), "stdout", "-l", lang, "--psm", psm, "--oem", "1"], capture_output=True, text=True).stdout
def norm(s):
    return re.sub(r"[ \t]+"," ", s.replace("\u00A0"," ").replace("\u202F"," ").replace("\u2009"," ")).strip()
def cer(ref, hyp):
    n,m=len(ref),len(hyp); dp=np.zeros((n+1,m+1),dtype=int)
    for i in range(n+1): dp[i,0]=i
    for j in range(m+1): dp[0,j]=j
    for i in range(1,n+1):
        for j in range(1,m+1):
            dp[i,j]=min(dp[i-1,j]+1, dp[i,j-1]+1, dp[i-1,j-1]+(ref[i-1]!=hyp[j-1]))
    return 0.0 if n==0 and m==0 else (dp[n,m]/max(n,1))
def wer(ref, hyp):
    r,h=ref.split(), hyp.split(); n,m=len(r),len(h); dp=np.zeros((n+1,m+1),dtype=int)
    for i in range(n+1): dp[i,0]=i
    for j in range(m+1): dp[0,j]=j
    for i in range(1,n+1):
        for j in range(1,m+1):
            dp[i,j]=min(dp[i-1,j]+1, dp[i,j-1]+1, dp[i-1,j-1]+(r[i-1]!=h[j-1]))
    return 0.0 if n==0 and m==0 else (dp[n,m]/max(n,1))
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data", required=True); ap.add_argument("--langs", nargs="+", required=True)
    args=ap.parse_args(); d=Path(args.data)
    pairs=[(p, p.with_suffix(".gt.txt")) for p in sorted(d.glob("*.tif")) if p.with_suffix(".gt.txt").exists()]
    if not pairs: raise SystemExit("No *.tif + *.gt.txt pairs")
    results={L:{"CER":[], "WER":[]} for L in args.langs}
    for img,gt in pairs:
        ref=norm(gt.read_text(encoding="utf-8", errors="ignore"))
        for L in args.langs:
            hyp=norm(run_tesseract(img, L))
            results[L]["CER"].append(cer(ref,hyp))
            results[L]["WER"].append(wer(ref,hyp))
            print(f"[{L}] {img.name}: CER={results[L]['CER'][-1]:.3%}, WER={results[L]['WER'][-1]:.3%}")
    for L in args.langs:
        import numpy as np
        c=float(np.mean(results[L]["CER"])); w=float(np.mean(results[L]["WER"]))
        print(f"{L}: mean CER={c:.3%}, WER={w:.3%}")
    (d/"eval_summary.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
if __name__=="__main__": main()
