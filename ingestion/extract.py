import fitz  # PyMuPDF
import json

def extract_sections(pdf_path, book_name, heading_font_threshold=14):
    doc = fitz.open(pdf_path)
    sections = []
    current_section = None

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                text = "".join(span["text"] for span in line["spans"]).strip()
                if not text:
                    continue

                max_font_size = max(span["size"] for span in line["spans"])
                is_heading = max_font_size >= heading_font_threshold

                if is_heading and len(text) < 100:
                    if current_section:
                        sections.append(current_section)

                    current_section = {
                        "book": book_name,
                        "section_title": text,
                        "page_start": page_num + 1,
                        "text": "",
                    }
                else:
                    if current_section is None:
                        current_section = {
                            "book": book_name,
                            "section_title": "Introduction",
                            "page_start": page_num + 1,
                            "text": "",
                        }

                    current_section["text"] += text + " "
    if current_section:
        sections.append(current_section)

    return sections

if __name__ == "__main__":
    sections = extract_sections("data/Galvin_OS.pdf", "GATE_OS_Book")
    with open("data/sections.json", "w") as f:
        json.dump(sections, f, indent=2)
    print(f"Extracted {len(sections)} sections")