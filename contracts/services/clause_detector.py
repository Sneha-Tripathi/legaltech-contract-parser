import json


CLAUSES = {

"Confidentiality":[

"confidential",

"non-disclosure",

"proprietary"

],

"Payment Terms":[

"payment",

"invoice",

"fee",

"amount due"

],

"Termination":[

"terminate",

"termination",

"expiry"

],

"Liability":[

"liability",

"damages"

],

"Indemnity":[

"indemnify",

"indemnification"

],

"Governing Law":[

"governing law",

"jurisdiction"

],

"Arbitration":[

"arbitration",

"dispute resolution"

]

}



class ClauseDetector:


    def __init__(self,text):


        self.text=text.lower()



    def detect(self):



        results=[]



        for clause,keywords in CLAUSES.items():



            found=False



            for keyword in keywords:



                if keyword in self.text:


                    found=True


                    break



            if found:



                results.append(clause)



        return results




if __name__=="__main__":



    with open(

            "uploads/day11_output.txt",

            encoding="utf-8"

    ) as f:



        text=f.read()




    detector=ClauseDetector(text)



    clauses=detector.detect()



    print("\nDetected Clauses\n")



    print(clauses)




    with open(

            "uploads/detected_clauses.json",

            "w"

    ) as file:



        json.dump(

            clauses,

            file,

            indent=4

        )



    print("\nSaved")