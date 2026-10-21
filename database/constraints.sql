ALTER TABLE risk_flag
ADD CONSTRAINT chk_risk_level
CHECK (
    risk_level IN ('Low', 'Medium', 'High')
);