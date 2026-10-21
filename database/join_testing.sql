SELECT
    c.id,
    c.title,
    ec.clause_type,
    rf.risk_type,
    rf.risk_level
FROM contract c
LEFT JOIN extracted_clause ec
ON c.id = ec.contract_id
LEFT JOIN risk_flag rf
ON c.id = rf.contract_id;