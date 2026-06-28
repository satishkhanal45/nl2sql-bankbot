-- Enable LTREE extension for hierarchical path queries
CREATE EXTENSION IF NOT EXISTS ltree;

-- Verify setup
SELECT 'LTREE extension enabled successfully' AS status;