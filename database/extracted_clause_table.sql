CREATE TABLE extracted_clause (
    id SERIAL PRIMARY KEY,
    contract_id INTEGER,
    clause_type VARCHAR(100) NOT NULL,
    clause_text TEXT NOT NULL
);