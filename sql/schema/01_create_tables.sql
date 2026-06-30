
-- TABLE 1: entity

CREATE TABLE IF NOT EXISTS entity (
    id          SERIAL PRIMARY KEY,
    entity_name VARCHAR(100) NOT NULL,
    fact        VARCHAR(100) NOT NULL,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    
    CONSTRAINT uq_entity_fact UNIQUE (entity_name, fact)
);

-- Index for fast lookups by entity_name
CREATE INDEX IF NOT EXISTS idx_entity_name ON entity (entity_name);

-- Index for fast lookups by fact
CREATE INDEX IF NOT EXISTS idx_entity_fact ON entity (fact);



-- TABLE 2: attribute

CREATE TABLE IF NOT EXISTS attribute (
    id         SERIAL PRIMARY KEY,
    label      VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Each attribute label must be unique
    CONSTRAINT uq_attribute_label UNIQUE (label)
);

-- Index for fast lookups by label
CREATE INDEX IF NOT EXISTS idx_attribute_label ON attribute (label);



-- TABLE 3: entity_value
CREATE TABLE IF NOT EXISTS entity_value (
    id           SERIAL PRIMARY KEY,
    entity_id    INTEGER NOT NULL,
    attribute_id INTEGER NOT NULL,
    path_name    LTREE,
    value        TEXT NOT NULL,
    type         VARCHAR(20) NOT NULL DEFAULT 'string'
                 CHECK (type IN ('string', 'numeric', 'boolean', 'date')),
    created_at   TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Foreign key: must reference a valid entity
    CONSTRAINT fk_entity
        FOREIGN KEY (entity_id)
        REFERENCES entity (id)
        ON DELETE CASCADE,

    -- Foreign key: must reference a valid attribute
    CONSTRAINT fk_attribute
        FOREIGN KEY (attribute_id)
        REFERENCES attribute (id)
        ON DELETE CASCADE,

    -- Prevent duplicate entity+attribute combinations
    CONSTRAINT uq_entity_attribute UNIQUE (entity_id, attribute_id)
);

-- Index for fast lookups by entity_id
CREATE INDEX IF NOT EXISTS idx_ev_entity_id ON entity_value (entity_id);

-- Index for fast lookups by attribute_id
CREATE INDEX IF NOT EXISTS idx_ev_attribute_id ON entity_value (attribute_id);

-- GiST index for fast LTREE path queries (<@, @>, ~, ?)
CREATE INDEX IF NOT EXISTS idx_ev_path_name ON entity_value USING GIST (path_name);