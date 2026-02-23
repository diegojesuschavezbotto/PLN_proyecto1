import PyPDF2

def pdf_to_text(pdf_path):
    with open(pdf_path, "rb") as file :
        reader = PyPDF2.PdfReader(file)
        text =""
        for page in reader.pages:
            text += page.extract_text()
        return text
    

text = pdf_to_text("CELEX_32016R0679_EN_TXT.pdf")

print(text)

with open("CELEX_32016R0679_EN_TXT.txt", "w", encoding="utf-8") as f:
    f.write(text)
    print("Texto ha sido guardado en CELEX_32016R0679_EN_TXT.txt")