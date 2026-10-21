from .models import (
    Contract,
    ExtractedClause,
    RiskFlag
)


def get_all_contracts():
    return Contract.objects.all()


def get_contract_by_id(contract_id):
    return Contract.objects.get(
        id=contract_id
    )


def get_contract_clauses(contract):
    return ExtractedClause.objects.filter(
        contract=contract
    )


def get_contract_risks(contract):
    return RiskFlag.objects.filter(
        contract=contract
    )

def get_contract_with_details(contract_id):

    return Contract.objects.prefetch_related(
        'extractedclause_set',
        'riskflag_set'
    ).get(
        id=contract_id
    )