from pathlib import Path
import re


def clean_gdpr_text(text: str) -> str:
    """
    Normaliza artefactos del PDF:
    - Une palabras cortadas por salto de línea
    - Normaliza saltos
    - Limpia espacios
    """

    print("[INFO] Normalizando texto...")

    # unir palabras cortadas
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)

    # normalizar saltos
    text = re.sub(r'\n+', '\n', text)

    # limpiar espacios
    text = re.sub(r'[ \t]+', ' ', text)

    print("[INFO] Normalización completada")
    return text


def remove_recitals(text: str) -> str:
    """
    Elimina considerandos y deja solo el articulado del GDPR
    """

    print("[INFO] Eliminando recitals...")

    match = re.search(r'CHAPTER\s+I', text)

    if not match:
        print("[WARN] No se encontró CHAPTER I — se devuelve texto original")
        return text

    cleaned = text[match.start():]

    print("[INFO] Recitals eliminados correctamente")
    return cleaned


def process_file(input_path: Path, output_path: Path):
    """Pipeline completo de limpieza"""

    if not input_path.exists():
        raise FileNotFoundError(f"No existe: {input_path}")

    print(f"[INFO] Procesando archivo: {input_path}")

    raw = input_path.read_text(encoding="utf-8")

    clean = clean_gdpr_text(raw)
    clean = remove_recitals(clean)

    print(f"[INFO] Caracteres finales: {len(clean)}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(clean, encoding="utf-8")

    print(f"[INFO] Texto limpio guardado en: {output_path}")


def main():
    input_path = Path("data/raw/CELEX_32016R0679_EN_TXT.txt")
    output_path = Path("data/processed/gdpr_clean.txt")

    process_file(input_path, output_path)


if __name__ == "__main__":
    main()