def detect_clauses(text):

    clauses = []

    if "termination" in text.lower():
        clauses.append("Termination")

    if "confidentiality" in text.lower():
        clauses.append("Confidentiality")

    if "payment" in text.lower():
        clauses.append("Payment")

    if "liability" in text.lower():
        clauses.append("Liability")

    return clauses


def detect_risks(text):

    risks = []

    if "unlimited liability" in text.lower():
        risks.append(
            "Unlimited Liability Clause Found"
        )

    return risks