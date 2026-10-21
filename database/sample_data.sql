-- Contract Records

INSERT INTO contract
(title, file_name, status)
VALUES
('NDA Agreement', 'nda.pdf', 'Processed'),
('Employment Agreement', 'employment.pdf', 'Processed'),
('Vendor Contract', 'vendor.pdf', 'Pending');


-- Clause Records

INSERT INTO extracted_clause
(contract_id, clause_type, clause_text)
VALUES
(
1,
'Confidentiality',
'All confidential information must remain protected.'
),
(
2,
'Termination',
'Agreement can be terminated with 30 days notice.'
),
(
3,
'Payment',
'Payment must be completed within 15 days.'
);


-- Risk Records

INSERT INTO risk_flag
(contract_id, risk_type, risk_level, description)
VALUES
(
1,
'Data Leakage',
'High',
'Risk of confidential information exposure.'
),
(
2,
'Unlimited Liability',
'High',
'Potential unlimited financial liability.'
),
(
3,
'Late Payment',
'Medium',
'Delayed payment may impact operations.'
);