# ORIOGO – all‑in‑one OCR & training (CZ base → EU extended charset)

**Jazyky v unicharsetu:** Čeština (cs), Slovenština (sk), Němčina (de), Angličtina (en),
Polština (pl), Dánština (da), Švédština (sv), Norština (no), Rumunština (ro).
Včetně měn, typografických uvozovek a pomlček, NBSP/NNBSP/THIN mezer.

## Quick start (Mac/Linux) – FAST (syntetika):
```bash
# 1) systémové nástroje: Tesseract 5.x + training tools (brew/apt)
# macOS: brew install tesseract && brew install --cask font-open-sans
# 2) python deps
pip install -r requirements.txt
# 3) build (stáhne ces, vytvoří starter, vygeneruje syntetiku, LSTMF, trénuje, ověří)
python scripts/build_all_in_one.py
# výsledek: tessdata/oriogo.traineddata
```

## Preprocess → TIFF → OCR
```bash
python scripts/preprocess_pdf_to_tiff.py --input data/input_pdfs --output_dir data/preprocessed --mode pages --recursive --dpi 600 --compression group4
python scripts/ocr_with_bboxes.py --input data/preprocessed --output_dir data/output --recursive --psm 6
```

## Layout z orámovaných PNG (barva + bbox + text)
```bash
python scripts/parse_colored_boxes.py --input data/annotated_png --output_dir data/layout --debug --psm 6
```

Pozn.: Build používá pouze podporované utility (`combine_lang_model`, `combine_tessdata`, `lstmtraining`, `text2image`).
Žádné historické `-o` flagy.
