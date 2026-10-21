# ER Diagram

## Contract

- id (Primary Key)
- title
- file_name
- uploaded_at

## ExtractedClause

- id (Primary Key)
- contract_id (Foreign Key)
- clause_type
- clause_text

## RiskFlag

- id (Primary Key)
- contract_id (Foreign Key)
- risk_type
- risk_level
- description

## Relationships

Contract (1) -> ExtractedClause (Many)

Contract (1) -> RiskFlag (Many)