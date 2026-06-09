-- ============================================
-- PURPOSE: Production Database Schema Definition
-- ============================================

-- PostgreSQL schema tables for metadata and relational storage
-- Database: pinterest_mcp_prod

-- Extension setup for generating UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Agents Table
CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    agent_name VARCHAR(100) NOT NULL,
    session_token VARCHAR(255) UNIQUE,
    permissions JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Boards Table
CREATE TABLE IF NOT EXISTS boards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    vector_centroid FLOAT[], -- 768 dimensions representing board's average style (SigLIP)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Pins Table
CREATE TABLE IF NOT EXISTS pins (
    id VARCHAR(100) PRIMARY KEY, -- Pinterest Pin ID or internal UUID
    title VARCHAR(255),
    description TEXT,
    image_url TEXT NOT NULL,
    source_url TEXT,
    aesthetic_score NUMERIC(4, 3) DEFAULT 0.500,
    colors VARCHAR(7)[] DEFAULT '{}', -- Array of HEX codes
    metadata JSONB DEFAULT '{}', -- OCR text, tags, font associations
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Collections (Groups of Boards)
CREATE TABLE IF NOT EXISTS collections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS collection_boards (
    collection_id UUID REFERENCES collections(id) ON DELETE CASCADE,
    board_id UUID REFERENCES boards(id) ON DELETE CASCADE,
    PRIMARY KEY (collection_id, board_id)
);

-- 6. Board Pins Junction Table
CREATE TABLE IF NOT EXISTS board_pins (
    board_id UUID REFERENCES boards(id) ON DELETE CASCADE,
    pin_id VARCHAR(100) REFERENCES pins(id) ON DELETE CASCADE,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (board_id, pin_id)
);

-- 7. Searches Table
CREATE TABLE IF NOT EXISTS searches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    search_query TEXT,
    parsed_filters JSONB DEFAULT '{}',
    results_returned_count INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. Trends Table
CREATE TABLE IF NOT EXISTS trends (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trend_name VARCHAR(255) UNIQUE NOT NULL,
    vertical VARCHAR(100) NOT NULL, -- UI/UX, Fashion, Interior, etc.
    growth_score NUMERIC(6, 2) NOT NULL, -- Percentage growth
    signature_colors VARCHAR(7)[] DEFAULT '{}',
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. Recommendations Table
CREATE TABLE IF NOT EXISTS recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    pin_id VARCHAR(100) REFERENCES pins(id) ON DELETE CASCADE,
    score NUMERIC(4, 3) NOT NULL, -- Confidence level
    seen BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 10. Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    action_type VARCHAR(100) NOT NULL, -- e.g. CALL_TOOL_SEARCH, DELETE_PIN
    target_resource VARCHAR(255) NOT NULL,
    payload JSONB DEFAULT '{}',
    ip_address VARCHAR(45),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indices for performance optimization
CREATE INDEX IF NOT EXISTS idx_pins_metadata ON pins USING gin (metadata);
CREATE INDEX IF NOT EXISTS idx_audit_agent ON audit_logs(agent_id);
CREATE INDEX IF NOT EXISTS idx_board_pins_board ON board_pins(board_id);

-- ============================================
-- FUTURE IMPROVEMENTS
-- ============================================
--
-- 1. Multi-user collaboration with table board_members
-- 2. Temporal database architecture to track historical state
-- 3. Partitioning of audit_logs for tables exceeding 100M rows
--
-- ============================================
