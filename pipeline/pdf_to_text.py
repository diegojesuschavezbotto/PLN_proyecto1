from pathlib import Path
import sys
import fitz  # PyMuPDF


def pdf_to_text(pdf_path: Path) -> str:
    """
    Extrae texto preservando layout real del documento.
    Mucho más preciso que PyPDF2 para documentos legales.
    """

    if not pdf_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {pdf_path}")

    print(f"[INFO] Leyendo PDF: {pdf_path}")

    doc = fitz.open(pdf_path)
    text_pages = []

    print(f"[INFO] Páginas detectadas: {len(doc)}")

    for i, page in enumerate(doc):
        blocks = page.get_text("blocks")

        page_text = ""
        for block in sorted(blocks, key=lambda b: (b[1], b[0])):
            page_text += block[4].strip() + "\n"

        text_pages.append(page_text)
        print(f"[DEBUG] Página {i+1} procesada")

    text = "\n".join(text_pages)

    print(f"[INFO] Extracción completada ({len(text)} caracteres)")
    return text


def save_text(text: str, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    print(f"[INFO] Texto guardado en: {output_path}")


def main():
    if len(sys.argv) != 2:
        print("Uso: python -m pipeline.pdf_to_text <ruta_pdf>")
        return

    pdf_path = Path(sys.argv[1])
    output_path = Path("data/raw") / (pdf_path.stem + ".txt")

    text = pdf_to_text(pdf_path)
    save_text(text, output_path)


if __name__ == "__main__":
    main()