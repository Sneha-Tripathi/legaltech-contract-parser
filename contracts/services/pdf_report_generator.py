import json

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


class PDFReportGenerator:

    def generate(self):

        with open(
            "uploads/final_report.json",
            "r",
            encoding="utf-8"
        ) as file:

            report = json.load(file)

        pdf = SimpleDocTemplate(
            "uploads/final_report.pdf"
        )

        styles = getSampleStyleSheet()

        story = []

        story.append(

            Paragraph(

                "<b>LegalTech Contract Report</b>",

                styles["Title"]

            )

        )

        story.append(Spacer(1, 20))

        for key, value in report.items():

            story.append(

                Paragraph(

                    f"<b>{key}</b>",

                    styles["Heading2"]

                )

            )

            story.append(

                Paragraph(

                    str(value),

                    styles["BodyText"]

                )

            )

            story.append(

                Spacer(1, 12)

            )

        pdf.build(story)

        print("PDF Report Generated Successfully")


if __name__ == "__main__":

    PDFReportGenerator().generate()