import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_sections(sections_path="data/sections.json", output_path="data/chunks.jsonl"):
    with open(sections_path) as f:
        sections = json.load(f)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=75,
        separators=["\n\n", "\n", ". ", " "]
    )

    all_chunks = []
    for section in sections:
        text = section["text"].strip()
        if len(text) < 20:
            continue
        pieces = splitter.split_text(text)
        for i, piece in enumerate(pieces):
            all_chunks.append({
                "chunk_id": f"{section['book']}_{section['page_start']}_{i}",
                "text": piece,
                "book": section["book"],
                "section": section["section_title"],
                "page": section["page_start"],
                "source_type": "textbook"
            })

    with open(output_path, "w") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk) + "\n")

    print(f"Created {len(all_chunks)} chunks")
    return all_chunks

if __name__ == "__main__":
    chunk_sections()