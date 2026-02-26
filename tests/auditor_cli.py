from pipeline.auditor import audit_company_text

def main():

    print("Auditor de Cumplimiento Normativo")
    print("Pegue el texto de la empresa (escriba FIN en una línea nueva):\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "FIN":
            break
        lines.append(line)

    company_text = "\n".join(lines)
    
    audit_company_text(company_text)


if __name__ == "__main__":
    main()