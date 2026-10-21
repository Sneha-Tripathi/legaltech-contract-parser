import json


HIGH_RISK = [

    "Termination",

    "Liability",

    "Indemnity"

]


MEDIUM_RISK = [

    "Payment Terms",

    "Arbitration"

]


LOW_RISK = [

    "Confidentiality",

    "Governing Law"

]



class RiskScorer:



    def __init__(self, clauses):


        self.clauses = clauses




    def calculate(self):



        report = {

            "High Risk": [],

            "Medium Risk": [],

            "Low Risk": []

        }




        for clause in self.clauses:



            if clause in HIGH_RISK:


                report["High Risk"].append(

                    clause

                )



            elif clause in MEDIUM_RISK:



                report["Medium Risk"].append(

                    clause

                )




            elif clause in LOW_RISK:



                report["Low Risk"].append(

                    clause

                )



        return report




if __name__=="__main__":



    with open(

            "uploads/detected_clauses.json"

    ) as f:



        clauses = json.load(f)




    scorer = RiskScorer(

        clauses

    )




    result = scorer.calculate()




    print(result)




    with open(

            "uploads/risk_report.json",

            "w"

    ) as file:



        json.dump(

            result,

            file,

            indent=4

        )




    print(

        "\nRisk Report Saved"

    )