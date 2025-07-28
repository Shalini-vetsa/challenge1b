import re
from sklearn.feature_extraction.text import TfidfVectorizer


def chunk_text(text, chunk_size=300):
    words = text.split()
    chunks, current_chunk = [], []
    current_len = 0
    for word in words:
        if current_len + len(word) + 1 > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_len = len(word)
        else:
            current_chunk.append(word)
            current_len += len(word) + 1
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks


def compute_relevance(text, query):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([query, text])
    return (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]


def extract_section_title(text):
    lines = text.strip().split("\n")
    for line in lines:
        clean = line.strip()
        if clean and (
            clean.isupper() or re.match(r"^[A-Z][A-Za-z ]+$", clean)
        ):
            return clean
    return lines[0][:60] if lines else "Untitled Section"


def rank_sections(pdf_data, persona, job):
    all_sections = []
    query = persona + " " + job
    for doc, pages in pdf_data.items():
        for page_num, page_text in enumerate(pages, start=1):
            chunks = chunk_text(page_text)
            for chunk in chunks:
                score = compute_relevance(chunk, query)
                title = extract_section_title(chunk)
                all_sections.append({
                    "document": doc,
                    "page_number": page_num,
                    "section_title": title,
                    "section_text": chunk,
                    "importance_rank": score
                })
    ranked = sorted(all_sections,
                    key=lambda x: x["importance_rank"], reverse=True)
    for idx, item in enumerate(ranked, start=1):
        item["importance_rank"] = idx
    return ranked[:5]
