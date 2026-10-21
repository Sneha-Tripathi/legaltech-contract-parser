import json
from datetime import datetime


class ReportGenerator:

    def generate(self):

        with open(
            "uploads/analytics.json",
            "r",
            encoding="utf-8"
        ) as file:

            analytics = json.load(file)

        with open(
            "uploads/entities.json",
            "r",
            encoding="utf-8"
        ) as file:

            entities = json.load(file)

        with open(
            "uploads/risk_report.json",
            "r",
            encoding="utf-8"
        ) as file:

            risks = json.load(file)

        report = {

            "Generated On":

                datetime.now().strftime(

                    "%d-%m-%Y %H:%M:%S"

                ),

            "Contract Name":

                "sample.pdf",

            "Analytics":

                analytics,

            "Entities":

                entities,

            "Risk Report":

                risks

        }

        with open(
            "uploads/final_report.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        return report


if __name__ == "__main__":

    generator = ReportGenerator()

    report = generator.generate()

    print(

        json.dumps(
            report,
            indent=4
        )

    )

    print("\nFinal Report Generated Successfully")