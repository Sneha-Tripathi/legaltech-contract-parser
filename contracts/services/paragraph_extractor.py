import fitz
import json


def extract_paragraphs(pdf_path):

    doc = fitz.open(pdf_path)

    all_paragraphs = []

    paragraph_id = 1

    for page_number in range(len(doc)):

        page = doc[page_number]

        text = page.get_text()

        paragraphs = text.split("\n\n")

        for para in paragraphs:

            para = para.strip()

            if len(para) > 20:

                all_paragraphs.append(
                    {
                        "paragraph_id": paragraph_id,
                        "page": page_number + 1,
                        "content": para
                    }
                )

                paragraph_id += 1

    doc.close()

    return all_paragraphs


if __name__ == "__main__":

    pdf_file = "uploads/sample.pdf"

    paragraphs = extract_paragraphs(pdf_file)

    print("\n" + "=" * 50)
    print("PARAGRAPH EXTRACTION REPORT")
    print("=" * 50)

    print(f"Total Paragraphs: {len(paragraphs)}")

    with open(
        "uploads/paragraphs.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            paragraphs,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n Paragraph JSON Created")