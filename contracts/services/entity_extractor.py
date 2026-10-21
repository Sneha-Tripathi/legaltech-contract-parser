import json
import re


class EntityExtractor:

    def __init__(self, text):

        self.text = text

    def extract(self):

        entities = {}

        entities["Dates"] = re.findall(
            r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
            self.text
        )

        entities["Payment Amounts"] = re.findall(
            r"(₹\s?\d[\d,]*|\$\s?\d[\d,]*)",
            self.text
        )

        entities["Organizations"] = re.findall(
            r"\b[A-Z][A-Za-z ]+(?:Ltd|Limited|LLP|Pvt\. Ltd\.|Inc)\b",
            self.text
        )

        return entities


if __name__ == "__main__":

    with open(
        "uploads/day11_output.txt",
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    extractor = EntityExtractor(text)

    entities = extractor.extract()

    print(json.dumps(entities, indent=4))

    with open(
        "uploads/entities.json",
        "w",
        encoding="utf-8"
    ) as output:

        json.dump(
            entities,
            output,
            indent=4
        )

    print("\n entities.json created successfully!")