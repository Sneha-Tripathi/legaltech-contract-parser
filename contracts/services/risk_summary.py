import json



with open(

        "uploads/risk_report.json"

) as f:



    report = json.load(f)




summary = {


"High":

len(report["High Risk"]),


"Medium":

len(report["Medium Risk"]),


"Low":

len(report["Low Risk"])

}




with open(

        "uploads/final_summary.json",

        "w"

) as file:



    json.dump(

        summary,

        file,

        indent=4

    )



print(summary)