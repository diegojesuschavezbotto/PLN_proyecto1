import re

def split_by_articles(text: str):
    """
    Detecta artículos reales del GDPR (no referencias internas)
    """
    
    pattern = r'\nArticle\s+(\d+)\s*\n'

    matches = list(re.finditer(pattern, text))

    articles = []

    for i in range(len(matches)):
        start = matches[i].start()

        if i + 1 < len(matches):
            end = matches[i+1].start()
        else:
            end = len(text)

        article_text = text[start:end].strip()
        article_number = matches[i].group(1)

        articles.append({
            "article": article_number,
            "text": article_text
        })

    return articles


