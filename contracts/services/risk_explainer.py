import json



EXPLANATIONS = {


"Termination":

"Contract may end unexpectedly.",


"Liability":

"Potential financial exposure.",


"Indemnity":

"Party may bear third-party losses.",


"Payment Terms":

"Delayed payment obligations.",


"Confidentiality":

"Sensitive data protection clause."

}



with open(

        "uploads/risk_report.json"

) as f:



    report = json.load(f)




explanations = {}



for level in report:



    for clause in report[level]:



        explanations[clause] = EXPLANATIONS.get(

            clause,

            "No explanation available."

        )



with open(

        "uploads/risk_explanations.json",

        "w"

) as file:



    json.dump(

        explanations,

        file,

        indent=4

    )



print(

    "Risk Explanations Saved"

)