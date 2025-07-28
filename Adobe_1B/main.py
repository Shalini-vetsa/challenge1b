import os
import json
from utils.text_extraction import extract_text_from_pdfs
from utils.summarizer import summarize_text
from utils.persona_ranking import rank_sections


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def process_collection(collection_dir):
    input_json = os.path.join(collection_dir, "challenge1b_input.json")
    output_json = os.path.join(collection_dir, "challenge1b_output.json")
    pdf_dir = os.path.join(collection_dir, "pdfs")
    if not os.path.exists(input_json):
        return
    with open(input_json, "r", encoding="utf-8") as f:
        input_data = json.load(f)
    persona = input_data.get("persona", "")
    job = input_data.get("job_to_be_done", "")
    if not isinstance(persona, str):
        persona = " ".join(map(str, persona.values())) \
            if isinstance(persona, dict) else str(persona)
    if not isinstance(job, str):
        job = " ".join(map(str, job.values())) \
            if isinstance(job, dict) else str(job)
    pdf_text_data = extract_text_from_pdfs(pdf_dir)
    ranked_sections = rank_sections(pdf_text_data, persona, job)
    extracted_sections = []
    for sec in ranked_sections:
        extracted_sections.append({
            "document": sec["document"],
            "section_title": sec["section_title"],
            "importance_rank": sec["importance_rank"],
            "page_number": sec["page_number"]
        })
    subsection_analysis = []
    for sec in ranked_sections:
        summary = summarize_text(sec["section_text"])
        subsection_analysis.append({
            "document": sec["document"],
            "refined_text": summary,
            "page_number": sec["page_number"]
        })
    output = {
        "metadata": {
            "input_documents": list(pdf_text_data.keys()),
            "persona": persona,
            "job_to_be_done": job
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)


def main():
    for collection in os.listdir(BASE_DIR):
        path = os.path.join(BASE_DIR, collection)
        if os.path.isdir(path) and collection.lower().startswith("collection"):
            process_collection(path)


if __name__ == "__main__":
    main()
