# GDPR Compliance Auditor (Mini Proyecto PLN)

---

## Funcionamiento

El sistema realiza los siguientes pasos:

1. Extrae texto del reglamento en PDF.
2. Limpia el documento jurídico (elimina recitals y normaliza texto).
3. Divide el documento en fragmentos semánticos (chunking).
4. Genera embeddings usando Ollama.
5. Construye una base vectorial persistente con ChromaDB.
6. Permite realizar búsqueda semántica sobre la normativa.

---

## Requisitos

- Python 3.10 o superior
- Ollama instalado  
  https://ollama.com/

Descargar los modelos necesarios:

```bash
ollama pull nomic-embed-text
ollama pull mistral
```

---

## Instalación de dependencias

Dentro del proyecto ejecutar:

```bash
pip install chromadb langchain langchain-ollama langchain-text-splitters pypdf2
```

---

## Ejecución paso a paso

### 1️⃣ Convertir PDF a texto

```bash
python -m pipeline.pdf_to_text data/raw/CELEX_32016R0679_EN_TXT.pdf
```

Genera:

```
data/raw/CELEX_32016R0679_EN_TXT.txt
```

---

### 2️⃣ Limpiar documento

```bash
python -m pipeline.clean_text
```

Genera:

```
data/processed/gdpr_clean.txt
```

---

### 3️⃣ Verificar fragmentación (chunking)

```bash
python -m pipeline.chunking
```

Debe mostrar aproximadamente:

```
Chunks creados: 200-300
```

---

### 4️⃣ Construir base vectorial

```bash
python -m pipeline.build_vector_db
```

Esto creará:

```
data/chroma_db/
```

---

### 5️⃣ Probar búsqueda semántica

```bash
python -m tests.teste_search
```

El sistema devolverá artículos del GDPR relacionados con la consulta realizada.

---

## Autor

Mini proyecto – Procesamiento de Lenguaje Natural
By Diego Botto & Hailton Amaya
