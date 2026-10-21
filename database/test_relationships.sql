INSERT INTO contract
(title, file_name)
VALUES
(
'Employment Agreement',
'employment.pdf'
);

INSERT INTO extracted_clause
(contract_id, clause_type, clause_text)
VALUES
(
1,
'Termination',
'Agreement can be terminated with notice.'
);

INSERT INTO risk_flag
(contract_id, risk_type, risk_level, description)
VALUES
(
1,
'Unlimited Liability',
'High',
'Potential financial exposure.'
);