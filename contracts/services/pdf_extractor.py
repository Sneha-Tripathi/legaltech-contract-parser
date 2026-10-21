import fitz


def extract_pdf_text(pdf_path):
    """
    Extract text from all pages of PDF
    """

    doc = fitz.open(pdf_path)

    full_text = ""

    print("\n" + "=" * 50)
    print("TEXT EXTRACTION REPORT")
    print("=" * 50)

    print(f"Total Pages: {len(doc)}\n")

    for page_number in range(len(doc)):

        page = doc[page_number]

        text = page.get_text()

        print(f"\n--- PAGE {page_number + 1} ---\n")

        print(text[:500])

        full_text += text + "\n"

    doc.close()

    return full_text


if __name__ == "__main__":

    pdf_file = "uploads/sample.pdf"

    extracted_text = extract_pdf_text(pdf_file)

    print("\n" + "=" * 50)
    print("TOTAL CHARACTERS")
    print("=" * 50)

    print(len(extracted_text))

    # Save extracted text into file
    with open(
        "uploads/extracted_text.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(extracted_text)

    print("\n Text saved successfully!")