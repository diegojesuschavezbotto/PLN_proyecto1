from pathlib import Path
import sys
import PyPDF2


def pdf_to_text(pdf_path: Path) -> str:
    """Extrae texto de un PDF."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {pdf_path}")

    print(f"[INFO] Leyendo PDF: {pdf_path}")

    text = ""
    with pdf_path.open("rb") as file:
        reader = PyPDF2.PdfReader(file)

        print(f"[INFO] Páginas detectadas: {len(reader.pages)}")

        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            text += page_text
            print(f"[DEBUG] Página {i+1} procesada")

    print(f"[INFO] Extracción completada ({len(text)} caracteres)")
    return text


def save_text(text: str, output_path: Path):
    """Guarda el texto en archivo."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        f.write(text)

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