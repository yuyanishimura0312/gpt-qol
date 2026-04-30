"""
DB3: Robotics Futures Evidence Database
Academic mentions of future robotics possibilities and their QoL impact potential.
Architecture follows AI Acceleration Evidence DB 4-layer pattern.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'robotics_futures.db')

SCHEMA = """
-- ============================================================
-- TAXONOMY LAYER
-- ============================================================

-- Domain taxonomy (3-level hierarchy)
CREATE TABLE IF NOT EXISTS domains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    name_ja TEXT NOT NULL,
    level INTEGER NOT NULL CHECK(level IN (1, 2, 3)),
    parent_id INTEGER REFERENCES domains(id),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Robotics capability types
CREATE TABLE IF NOT EXISTS capability_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    name_ja TEXT NOT NULL,
    description TEXT
);

-- QoL impact dimension types (linked to 6-dimension model)
CREATE TABLE IF NOT EXISTS qol_impact_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    name_ja TEXT NOT NULL,
    description TEXT
);

-- Consensus levels
CREATE TABLE IF NOT EXISTS consensus_levels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    rank INTEGER
);

-- Evidence types
CREATE TABLE IF NOT EXISTS evidence_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT
);

-- ============================================================
-- SOURCE LAYER
-- ============================================================

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    journal TEXT,
    doi TEXT UNIQUE,
    venue_type TEXT CHECK(venue_type IN (
        'journal', 'conference', 'workshop', 'preprint',
        'book', 'report', 'thesis', 'white_paper'
    )),
    source_type TEXT CHECK(source_type IN (
        'academic_peer_reviewed', 'government_report',
        'industry_report', 'institutional_report',
        'conference_paper', 'preprint', 'book', 'thesis',
        'foresight_report', 'roadmap'
    )),
    peer_reviewed INTEGER DEFAULT 0,
    credibility_score REAL CHECK(credibility_score BETWEEN 0 AND 1),
    url TEXT,
    abstract TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL REFERENCES sources(id),
    author_name TEXT NOT NULL,
    affiliation TEXT,
    h_index INTEGER,
    UNIQUE(source_id, author_name)
);

-- ============================================================
-- EVIDENCE LAYER
-- ============================================================

-- Main evidence mentions
CREATE TABLE IF NOT EXISTS mentions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL REFERENCES sources(id),
    domain_id INTEGER REFERENCES domains(id),
    claim_summary TEXT NOT NULL,
    capability_type_code TEXT REFERENCES capability_types(code),
    -- Timeline projection
    timeline_projection TEXT,
    projected_year_start INTEGER,
    projected_year_end INTEGER,
    projection_confidence TEXT CHECK(projection_confidence IN (
        'high', 'medium', 'low', 'speculative'
    )),
    -- QoL impact assessment
    qol_dimension TEXT CHECK(qol_dimension IN (
        'aesthetic', 'emotional', 'meaning',
        'relational', 'autonomy', 'cultural', 'multiple'
    )),
    qol_impact_direction TEXT CHECK(qol_impact_direction IN (
        'positive', 'negative', 'mixed', 'conditional', 'unknown'
    )),
    qol_impact_magnitude INTEGER CHECK(qol_impact_magnitude BETWEEN -5 AND 5),
    -- Economic assessment
    economic_impact_direction TEXT CHECK(economic_impact_direction IN (
        'positive', 'negative', 'mixed', 'conditional', 'unknown'
    )),
    economic_impact_magnitude INTEGER CHECK(economic_impact_magnitude BETWEEN -5 AND 5),
    -- Quadrant assignment
    quadrant TEXT CHECK(quadrant IN ('I', 'II', 'III', 'IV')),
    -- Conditions and constraints
    conditions TEXT,
    limitations TEXT,
    ethical_concerns TEXT,
    -- Metadata
    evidence_type_code TEXT REFERENCES evidence_types(code),
    consensus_level_code TEXT REFERENCES consensus_levels(code),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Supporting evidence items for each mention
CREATE TABLE IF NOT EXISTS mention_evidence_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mention_id INTEGER NOT NULL REFERENCES mentions(id),
    evidence_description TEXT NOT NULL,
    evidence_type TEXT,
    quantitative_value TEXT,
    unit TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mention conditions and caveats
CREATE TABLE IF NOT EXISTS mention_caveats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mention_id INTEGER NOT NULL REFERENCES mentions(id),
    caveat_type TEXT CHECK(caveat_type IN (
        'technical_barrier', 'ethical_concern', 'cost_barrier',
        'regulatory', 'cultural_resistance', 'safety',
        'privacy', 'equity', 'environmental', 'other'
    )),
    description TEXT NOT NULL,
    severity TEXT CHECK(severity IN ('critical', 'major', 'moderate', 'minor'))
);

-- ============================================================
-- AGGREGATE LAYER
-- ============================================================

-- Domain-level assessments
CREATE TABLE IF NOT EXISTS domain_assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER NOT NULL REFERENCES domains(id),
    mention_count INTEGER DEFAULT 0,
    consensus_level TEXT,
    confidence_tier TEXT CHECK(confidence_tier IN (
        'insufficient', 'tentative', 'moderate', 'strong', 'definitive'
    )),
    earliest_projection INTEGER,
    latest_projection INTEGER,
    qol_potential_score REAL,
    economic_potential_score REAL,
    quadrant_tendency TEXT,
    assessment_summary TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(domain_id)
);

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_domains_level ON domains(level);
CREATE INDEX IF NOT EXISTS idx_domains_parent ON domains(parent_id);
CREATE INDEX IF NOT EXISTS idx_mentions_domain ON mentions(domain_id);
CREATE INDEX IF NOT EXISTS idx_mentions_source ON mentions(source_id);
CREATE INDEX IF NOT EXISTS idx_mentions_qol ON mentions(qol_dimension);
CREATE INDEX IF NOT EXISTS idx_mentions_quadrant ON mentions(quadrant);
CREATE INDEX IF NOT EXISTS idx_mentions_year ON mentions(projected_year_start);
CREATE INDEX IF NOT EXISTS idx_evidence_mention ON mention_evidence_items(mention_id);
CREATE INDEX IF NOT EXISTS idx_caveats_mention ON mention_caveats(mention_id);
"""

# Seed data: Domain taxonomy
SEED_DOMAINS_L1 = [
    ('healthcare', 'Healthcare & Care', '医療・介護'),
    ('education', 'Education', '教育'),
    ('arts', 'Arts & Creation', '芸術・創作'),
    ('domestic', 'Domestic Life', '家庭生活'),
    ('agriculture', 'Agriculture & Food', '農業・食文化'),
    ('industry', 'Industry & Manufacturing', '産業・製造'),
    ('mobility', 'Mobility & Transport', '移動・交通'),
    ('social', 'Social Relations', '社会関係'),
]

SEED_DOMAINS_L2 = {
    'healthcare': [
        ('healthcare_rehab', 'Rehabilitation', 'リハビリテーション'),
        ('healthcare_elderly', 'Elderly Care', '高齢者ケア'),
        ('healthcare_mental', 'Mental Health', 'メンタルヘルス'),
        ('healthcare_surgery', 'Surgical Robots', '手術ロボット'),
        ('healthcare_companion', 'Therapeutic Companions', '治療用コンパニオン'),
    ],
    'education': [
        ('education_stem', 'STEM Education', 'STEM教育'),
        ('education_language', 'Language Learning', '言語学習'),
        ('education_special', 'Special Needs', '特別支援'),
        ('education_lifelong', 'Lifelong Learning', '生涯学習'),
    ],
    'arts': [
        ('arts_performance', 'Performance Art', 'パフォーマンスアート'),
        ('arts_music', 'Music Creation', '音楽創作'),
        ('arts_visual', 'Visual Arts', 'ビジュアルアート'),
        ('arts_architecture', 'Architecture & Space', '建築・空間'),
    ],
    'domestic': [
        ('domestic_cleaning', 'Cleaning & Maintenance', '清掃・メンテナンス'),
        ('domestic_cooking', 'Cooking & Food Prep', '調理'),
        ('domestic_companion', 'Home Companions', '家庭用コンパニオン'),
        ('domestic_garden', 'Gardening', '園芸'),
    ],
    'agriculture': [
        ('agriculture_harvest', 'Harvesting', '収穫'),
        ('agriculture_precision', 'Precision Farming', '精密農業'),
        ('agriculture_sustainable', 'Sustainability', '持続可能性'),
    ],
    'industry': [
        ('industry_cobots', 'Collaborative Robots', '協働ロボット'),
        ('industry_logistics', 'Logistics', '物流'),
        ('industry_construction', 'Construction', '建設'),
    ],
    'mobility': [
        ('mobility_autonomous', 'Autonomous Vehicles', '自動運転'),
        ('mobility_exo', 'Exoskeletons', '外骨格'),
        ('mobility_personal', 'Personal Mobility', 'パーソナルモビリティ'),
    ],
    'social': [
        ('social_hri', 'Human-Robot Interaction', 'ヒューマンロボットインタラクション'),
        ('social_emotion', 'Emotional Bonding', '感情的結びつき'),
        ('social_cultural', 'Cultural Attitudes', '文化的態度'),
        ('social_ethics', 'Ethics & Society', '倫理・社会'),
    ],
}

SEED_CAPABILITIES = [
    ('physical_manipulation', 'Physical Manipulation', '物理的操作',
     'Grasping, moving, assembling physical objects'),
    ('social_interaction', 'Social Interaction', '社会的インタラクション',
     'Conversation, emotional response, social cues'),
    ('creative_expression', 'Creative Expression', '創造的表現',
     'Art, music, dance, performance'),
    ('sensory_augmentation', 'Sensory Augmentation', '感覚拡張',
     'Enhancing human sensory capabilities'),
    ('cognitive_support', 'Cognitive Support', '認知的支援',
     'Decision support, memory aid, learning facilitation'),
    ('emotional_companionship', 'Emotional Companionship', '感情的コンパニオンシップ',
     'Providing emotional support, comfort, companionship'),
    ('environmental_adaptation', 'Environmental Adaptation', '環境適応',
     'Operating in diverse, unstructured environments'),
    ('collaborative_task', 'Collaborative Task', '協働タスク',
     'Working alongside humans on shared goals'),
]

SEED_QOL_TYPES = [
    ('aesthetic', 'Aesthetic Experience', '感覚・美的経験', 'Impact on sensory and aesthetic experience'),
    ('emotional', 'Emotional Richness', '感情的豊かさ', 'Impact on emotional depth and diversity'),
    ('meaning', 'Meaning & Purpose', '意味・目的', 'Impact on sense of purpose and meaning'),
    ('relational', 'Relational Belonging', '関係性・帰属', 'Impact on social connections'),
    ('autonomy', 'Autonomy & Growth', '自律・成長', 'Impact on personal autonomy and growth'),
    ('cultural', 'Cultural Sensitivity', '文化的感受性', 'Impact on cultural depth and diversity'),
]

SEED_CONSENSUS = [
    ('DEFINITIVE', 'Definitive', 'Strong academic consensus with meta-analyses', 6),
    ('STRONG', 'Strong', 'Multiple high-quality studies in agreement', 5),
    ('MODERATE', 'Moderate', 'Several studies with consistent findings', 4),
    ('GROWING', 'Growing', 'Emerging body of supportive evidence', 3),
    ('EMERGING', 'Emerging', 'Initial studies, limited replication', 2),
    ('CONTESTED', 'Contested', 'Conflicting evidence or active debate', 1),
]

SEED_EVIDENCE_TYPES = [
    ('META_ANALYSIS', 'Meta-analysis', 'Systematic review with quantitative synthesis'),
    ('RCT', 'Randomized Controlled Trial', 'Experimental study with random assignment'),
    ('COHORT', 'Cohort Study', 'Observational longitudinal study'),
    ('CASE_STUDY', 'Case Study', 'In-depth analysis of specific instances'),
    ('SURVEY', 'Survey Research', 'Cross-sectional survey data'),
    ('EXPERT_OPINION', 'Expert Opinion', 'Expert consensus or roadmap projection'),
    ('FORESIGHT', 'Foresight Report', 'Structured futures analysis'),
    ('PROTOTYPE', 'Prototype Demonstration', 'Working prototype with measured outcomes'),
    ('SIMULATION', 'Simulation Study', 'Computational modeling and simulation'),
    ('THEORETICAL', 'Theoretical Framework', 'Conceptual or theoretical analysis'),
]


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)

    # Seed L1 domains
    for code, name, name_ja in SEED_DOMAINS_L1:
        conn.execute("""
            INSERT OR IGNORE INTO domains (code, name, name_ja, level, description)
            VALUES (?, ?, ?, 1, ?)
        """, (code, name, name_ja, f'L1 domain: {name}'))

    # Seed L2 domains
    for parent_code, children in SEED_DOMAINS_L2.items():
        parent_id = conn.execute(
            "SELECT id FROM domains WHERE code = ?", (parent_code,)
        ).fetchone()
        if parent_id:
            for code, name, name_ja in children:
                conn.execute("""
                    INSERT OR IGNORE INTO domains (code, name, name_ja, level, parent_id, description)
                    VALUES (?, ?, ?, 2, ?, ?)
                """, (code, name, name_ja, parent_id[0], f'L2 domain under {parent_code}'))

    # Seed capability types
    for code, name, name_ja, desc in SEED_CAPABILITIES:
        conn.execute("""
            INSERT OR IGNORE INTO capability_types (code, name, name_ja, description)
            VALUES (?, ?, ?, ?)
        """, (code, name, name_ja, desc))

    # Seed QoL impact types
    for code, name, name_ja, desc in SEED_QOL_TYPES:
        conn.execute("""
            INSERT OR IGNORE INTO qol_impact_types (code, name, name_ja, description)
            VALUES (?, ?, ?, ?)
        """, (code, name, name_ja, desc))

    # Seed consensus levels
    for code, name, desc, rank in SEED_CONSENSUS:
        conn.execute("""
            INSERT OR IGNORE INTO consensus_levels (code, name, description, rank)
            VALUES (?, ?, ?, ?)
        """, (code, name, desc, rank))

    # Seed evidence types
    for code, name, desc in SEED_EVIDENCE_TYPES:
        conn.execute("""
            INSERT OR IGNORE INTO evidence_types (code, name, description)
            VALUES (?, ?, ?)
        """, (code, name, desc))

    conn.commit()

    # Report
    cursor = conn.cursor()
    tables = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    print(f"DB3 initialized: {DB_PATH}")
    print(f"Tables ({len(tables)}):")
    for t in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM [{t[0]}]").fetchone()[0]
        print(f"  {t[0]}: {count} rows")

    conn.close()


if __name__ == '__main__':
    init_db()
