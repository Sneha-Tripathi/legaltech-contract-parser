import json
from datetime import datetime


class Analytics:

    def __init__(self, report):
        self.report = report

    def calculate(self):

        high = len(self.report["High Risk"])
        medium = len(self.report["Medium Risk"])
        low = len(self.report["Low Risk"])

        total = high + medium + low

        if total == 0:
            total = 1

        risk_percent = round((high / total) * 100, 2)

        health_score = 100 - (high * 20) - (medium * 10)

        if health_score < 0:
            health_score = 0

        if health_score >= 80:
            status = "Safe"

        elif health_score >= 50:
            status = "Moderate Risk"

        else:
            status = "High Risk"

        if status == "Safe":

            recommendation = (
                "Contract appears safe. Proceed after standard legal review."
            )

        elif status == "Moderate Risk":

            recommendation = (
                "Review payment and arbitration clauses before approval."
            )

        else:

            recommendation = (
                "Legal team review required before signing the contract."
            )

        analytics = {

            "Generated On": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

            "Total Clauses": total,

            "High Risk": high,

            "Medium Risk": medium,

            "Low Risk": low,

            "Risk Percentage": risk_percent,

            "Health Score": health_score,

            "Contract Status": status,

            "Recommendation": recommendation

        }

        return analytics


if __name__ == "__main__":

    with open(
        "uploads/risk_report.json",
        "r",
        encoding="utf-8"
    ) as f:

        report = json.load(f)

    analyzer = Analytics(report)

    data = analyzer.calculate()

    print("\n" + "=" * 50)
    print("CONTRACT ANALYTICS")
    print("=" * 50)

    for key, value in data.items():

        print(f"{key}: {value}")

    with open(
        "uploads/analytics.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )

    print("\n Analytics saved successfully!")