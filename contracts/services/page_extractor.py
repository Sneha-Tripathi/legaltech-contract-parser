import fitz
import json


def extract_pages(pdf_path):

    doc = fitz.open(pdf_path)

    pages_data = []

    print("\n" + "=" * 50)
    print("PAGE STRUCTURE REPORT")
    print("=" * 50)

    for page_number in range(len(doc)):

        page = doc[page_number]

        text = page.get_text()

        page_info = {
            "page": page_number + 1,
            "characters": len(text),
            "text": text
        }

        pages_data.append(page_info)

        print(
            f"Page {page_number + 1} => {len(text)} characters"
        )

    doc.close()

    return pages_data


if __name__ == "__main__":

    pdf_file = "uploads/sample.pdf"

    pages = extract_pages(pdf_file)

    with open(
        "uploads/page_data.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            pages,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n JSON file created successfully!")