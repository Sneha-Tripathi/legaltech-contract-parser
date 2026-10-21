ALTER TABLE extracted_clause
ADD CONSTRAINT fk_contract_clause
FOREIGN KEY (contract_id)
REFERENCES contract(id);

ALTER TABLE risk_flag
ADD CONSTRAINT fk_contract_risk
FOREIGN KEY (contract_id)
REFERENCES contract(id);