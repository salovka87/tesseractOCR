# tesseractOCR

Tento repozitář obsahuje kompletní sadu skriptů a nástrojů pro **trénink
vlastního OCR modelu** v Tesseractu.\
Cílem je vytvořit model `oriogo.traineddata`, který vychází z
`ces.traineddata` a je rozšířený o znaky používané v češtině,
slovenštině, němčině, polštině, dánštině, rumunštině a švédštině +
měnové symboly.

## Obsah

-   `preprocess_pdf_to_tiff.py` -- převod PDF → TIFF pro trénink (600
    DPI, odšumění, kontrast).\
-   `generate_training_texts.py` -- generování training_text.txt s
    rozšířeným unicharsetem.\
-   `train_tesseract_oriogo.py` -- hlavní Python skript, který:
    -   připraví data (.tif → .box → .gt.txt),
    -   spustí Tesseract training pipeline,
    -   vygeneruje `oriogo.traineddata`.

## Docker prostředí

Trénink může probíhat v Docker kontejneru, takže není potřeba řešit venv.

### 1. Build image

``` bash
docker build -t oriogo-ocr .
```

### 2. Spuštění kontejneru

``` bash
docker run -it --rm -v $(pwd):/app oriogo-ocr bash
```

### 3. Trénink modelu

V kontejneru spusť:

``` bash
python train_tesseract_oriogo.py --input ./training_data --output ./models
```

Výsledkem bude `models/oriogo.traineddata`.

## Struktura repozitáře

    oriogo-ocr/
    │
    ├── Dockerfile
    ├── README.md
    ├── preprocess_pdf_to_tiff.py
    ├── generate_training_texts.py
    ├── train_tesseract_oriogo.py
    ├── tessdata/        # sem se automaticky stáhne ces.traineddata
    ├── training_data/   # vstupní .pdf nebo .tif faktury
    └── models/          # výstupní .traineddata

## Stažení původního modelu

Skript `train_tesseract_oriogo.py` při prvním spuštění stáhne oficiální
`ces.traineddata` z [tessdata
GitHubu](https://github.com/tesseract-ocr/tessdata_best) a použije jej
jako základ pro fine-tuning.
