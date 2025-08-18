#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BEST = ROOT/"tessdata/ces.traineddata"
STARTER = ROOT/"tessdata/oriogo-starter.traineddata"
LIST = ROOT/"data/lstmf/list.train"
OUT = ROOT/"models/out"
FINAL = ROOT/"tessdata/oriogo.traineddata"
MAX_ITERS = "12000"
def run(cmd): print(">>", " ".join(map(str, cmd))); subprocess.run(cmd, check=True)
def main():
    for p in [BEST, STARTER, LIST]:
        if not p.exists(): print(f"❌ Missing: {p}"); sys.exit(1)
    OUT.mkdir(parents=True, exist_ok=True)
    run(["combine_tessdata","-e", str(BEST), str(OUT/"ces.lstm")])
    run(["lstmtraining","--model_output", str(OUT/"oriogo"),"--continue_from", str(OUT/"ces.lstm"),"--traineddata", str(STARTER),"--train_listfile", str(LIST),"--max_iterations", MAX_ITERS])
    ckpt = OUT/"oriogo_checkpoint"
    run(["lstmtraining","--stop_training","--continue_from", str(ckpt),"--traineddata", str(STARTER),"--model_output", str(FINAL)])
    print(f"✅ Model ready: {FINAL}")
if __name__ == "__main__":
    main()
