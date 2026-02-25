from pathlib import Path
import re


def normalize_text(text: str) -> str:
    print("[INFO] Normalizando texto...")

    # unir palabras con guion de salto de línea
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)

    # reemplazar saltos múltiples
    text = re.sub(r'\n{2,}', '\n\n', text)

    # eliminar espacios duplicados
    text = re.sub(r'[ \t]+', ' ', text)

    return text


def remove_headers_footers(text: str) -> str:
    print("[INFO] Eliminando encabezados de página...")

    text = re.sub(r'Official Journal of the European Union.*', '', text)
    text = re.sub(r'\d+\.\d+\.\d+\sL\s\d+/\d+', '', text)

    return text


def remove_recitals(text: str) -> str:
    print("[INFO] Eliminando recitals...")

    match = re.search(r'CHAPTER\s+I', text)
    if not match:
        print("[WARN] No se encontró CHAPTER I")
        return text

    return text[match.start():]


def process_file(input_path: Path, output_path: Path):
    if not input_path.exists():
        raise FileNotFoundError(f"No existe: {input_path}")

    print(f"[INFO] Procesando archivo: {input_path}")

    raw = input_path.read_text(encoding="utf-8")

    clean = normalize_text(raw)
    clean = remove_headers_footers(clean)
    clean = remove_recitals(clean)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(clean, encoding="utf-8")

    print(f"[INFO] Texto limpio guardado en: {output_path}")
    print(f"[INFO] Caracteres finales: {len(clean)}")


def main():
    input_path = Path("data/raw/CELEX_32016R0679_EN_TXT.txt")
    output_path = Path("data/processed/gdpr_clean.txt")

    process_file(input_path, output_path)


if __name__ == "__main__":
    main()