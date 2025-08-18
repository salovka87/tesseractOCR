
# Batch převod všech PDF v input složce na SAMOSTATNÉ TIFFy po stránkách.
# Preprocess: RGB->GRAY -> Gaussian blur -> Otsu -> median blur.
# Výstup: bilevel (1-bit) TIFF s CCITT Group4 kompresí (ideální pro Tesseract).

import argparse
from pathlib import Path
import numpy as np
from PIL import Image
import fitz  # PyMuPDF
import cv2

def preprocess_np(img_rgb: np.ndarray) -> np.ndarray:
    # OCR-friendly předzpracování (binarizace)
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thr = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thr = cv2.medianBlur(thr, 3)
    return thr  # 0/255

def render_pdf_page_to_rgb(page: fitz.Page, dpi: int) -> np.ndarray:
    # Render PDF stránky do RGB numpy pole při zvoleném DPI
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return np.array(img)

def save_group4_tiff(binary_np: np.ndarray, out_path: Path) -> None:
    # Uložení binárního obrazu jako Group4 TIFF (1-bit)
    img = Image.fromarray(binary_np).convert("1")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="TIFF", compression="group4")

def process_pdf(pdf_path: Path, out_dir: Path, dpi: int) -> int:
    # Zpracuje jedno PDF => uloží .tif pro každou stránku
    doc = fitz.open(pdf_path)
    saved = 0
    for i, page in enumerate(doc, start=1):
        rgb = render_pdf_page_to_rgb(page, dpi=dpi)
        bin_img = preprocess_np(rgb)
        out_path = out_dir / f"{pdf_path.stem}_p{i}.tif"
        save_group4_tiff(bin_img, out_path)
        saved += 1
    return saved

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_dir", default="data/input_pdf", help="Složka s PDF")
    ap.add_argument("--output_dir", default="data/preprocessed", help="Složka pro per-page TIFFy")
    ap.add_argument("--dpi", type=int, default=600, help="DPI renderu PDF")
    args = ap.parse_args()

    in_dir = Path(args.input_dir)
    out_dir = Path(args.output_dir)
    pdfs = sorted(in_dir.glob("*.pdf"))

    total_pages = 0
    for pdf in pdfs:
        saved = process_pdf(pdf, out_dir, args.dpi)
        print(f"✅ {pdf.name}: uloženo {saved} stránek do {out_dir}")
        total_pages += saved

    if not pdfs:
        print(f"ℹ️ Nenalezeny žádné PDF v {in_dir}")
    else:
        print(f"🎯 Hotovo: celkem uloženo {total_pages} TIFF stránek.")

if __name__ == "__main__":
    main()