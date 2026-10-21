CREATE TABLE risk_flag (
    id SERIAL PRIMARY KEY,
    contract_id INTEGER,
    risk_type VARCHAR(100) NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    description TEXT
);