CREATE TABLE contract (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    file_name VARCHAR(255),
    uploaded_at TIMESTAMP
);

CREATE TABLE extracted_clause (
    id SERIAL PRIMARY KEY,
    contract_id INTEGER,
    clause_type VARCHAR(100),
    clause_text TEXT
);

CREATE TABLE risk_flag (
    id SERIAL PRIMARY KEY,
    contract_id INTEGER,
    risk_type VARCHAR(100),
    risk_level VARCHAR(50),
    description TEXT
);

