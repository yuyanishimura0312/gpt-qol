"""
DB1: QoL Sensibility Scoring Knowledge Database
Quality of Life measurement frameworks emphasizing emotional richness,
aesthetic experience, and cultural sensitivity.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'qol_sensibility.db')

SCHEMA = """
-- Sources (shared pattern across all 3 DBs)
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    journal TEXT,
    doi TEXT UNIQUE,
    source_type TEXT CHECK(source_type IN (
        'academic_peer_reviewed', 'book', 'book_chapter',
        'government_report', 'institutional_report',
        'conference_paper', 'thesis', 'grey_literature'
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
    role TEXT DEFAULT 'author',
    UNIQUE(source_id, author_name)
);

-- Academic Frameworks for QoL measurement
CREATE TABLE IF NOT EXISTS frameworks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    name_ja TEXT,
    authors TEXT NOT NULL,
    year INTEGER NOT NULL,
    source_id INTEGER REFERENCES sources(id),
    framework_type TEXT CHECK(framework_type IN (
        'capability', 'subjective_wellbeing', 'psychological_wellbeing',
        'eudaimonic', 'hedonic', 'composite', 'cultural',
        'aesthetic', 'national_index', 'technology_specific'
    )),
    dimensions_count INTEGER,
    cultural_origin TEXT,
    description TEXT,
    key_insight TEXT,
    relevance_to_tech TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimensions within each framework
CREATE TABLE IF NOT EXISTS framework_dimensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    framework_id INTEGER NOT NULL REFERENCES frameworks(id),
    dimension_name TEXT NOT NULL,
    dimension_name_ja TEXT,
    dimension_category TEXT CHECK(dimension_category IN (
        'aesthetic', 'emotional', 'meaning', 'relational',
        'autonomy', 'cultural', 'cognitive', 'physical',
        'economic', 'environmental', 'political', 'spiritual'
    )),
    measurement_method TEXT,
    scale_type TEXT,
    reliability_alpha REAL,
    validity_evidence TEXT,
    cultural_applicability TEXT,
    description TEXT,
    UNIQUE(framework_id, dimension_name)
);

-- Measurement scales and tools
CREATE TABLE IF NOT EXISTS measurement_scales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    abbreviation TEXT,
    authors TEXT NOT NULL,
    year INTEGER NOT NULL,
    source_id INTEGER REFERENCES sources(id),
    items_count INTEGER,
    scale_type TEXT CHECK(scale_type IN (
        'likert', 'semantic_differential', 'visual_analog',
        'frequency', 'composite', 'experience_sampling',
        'physiological', 'behavioral', 'narrative'
    )),
    target_population TEXT,
    languages_validated TEXT,
    reliability_score REAL,
    description TEXT,
    url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mapping scales to our 6 QoL dimensions
CREATE TABLE IF NOT EXISTS scale_dimension_mapping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scale_id INTEGER NOT NULL REFERENCES measurement_scales(id),
    qol_dimension TEXT NOT NULL CHECK(qol_dimension IN (
        'aesthetic', 'emotional', 'meaning',
        'relational', 'autonomy', 'cultural'
    )),
    coverage_score REAL CHECK(coverage_score BETWEEN 0 AND 1),
    notes TEXT,
    UNIQUE(scale_id, qol_dimension)
);

-- Technology x QoL evidence
CREATE TABLE IF NOT EXISTS tech_qol_evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL REFERENCES sources(id),
    technology_type TEXT NOT NULL,
    qol_dimension TEXT CHECK(qol_dimension IN (
        'aesthetic', 'emotional', 'meaning',
        'relational', 'autonomy', 'cultural', 'multiple'
    )),
    effect_direction TEXT CHECK(effect_direction IN (
        'positive', 'negative', 'mixed', 'null', 'conditional'
    )),
    effect_size TEXT,
    sample_size INTEGER,
    population_type TEXT,
    cultural_context TEXT,
    methodology TEXT,
    claim_summary TEXT NOT NULL,
    conditions TEXT,
    limitations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6-dimension QoL scoring model definition
CREATE TABLE IF NOT EXISTS qol_dimensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    name_ja TEXT NOT NULL,
    description TEXT,
    academic_foundations TEXT,
    scoring_criteria_plus5 TEXT,
    scoring_criteria_plus3 TEXT,
    scoring_criteria_zero TEXT,
    scoring_criteria_minus3 TEXT,
    scoring_criteria_minus5 TEXT,
    key_scales TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_sources_year ON sources(year);
CREATE INDEX IF NOT EXISTS idx_sources_doi ON sources(doi);
CREATE INDEX IF NOT EXISTS idx_frameworks_type ON frameworks(framework_type);
CREATE INDEX IF NOT EXISTS idx_scales_dimension ON scale_dimension_mapping(qol_dimension);
CREATE INDEX IF NOT EXISTS idx_evidence_dimension ON tech_qol_evidence(qol_dimension);
CREATE INDEX IF NOT EXISTS idx_evidence_tech ON tech_qol_evidence(technology_type);
"""

# Seed data: 6 QoL dimensions
SEED_DIMENSIONS = [
    ('aesthetic', 'Aesthetic Experience', '感覚・美的経験',
     'New aesthetic experience categories, access to beauty, sensory richness',
     'Nussbaum Capability #4 (Senses/Imagination/Thought), AEQ, Csikszentmihalyi Flow, AWE-S',
     'Creation of entirely new aesthetic experience categories',
     'Expanded access to existing aesthetic experiences',
     'No change in aesthetic experience',
     'Homogenization of aesthetic experience',
     'Dulling of aesthetic sensitivity'),
    ('emotional', 'Emotional Richness', '感情的豊かさ',
     'Diversity of complex emotional experiences, emotional depth',
     'Kama Muta Scale, PANAS, Ryff PWB, PERMA-E',
     'Opening of entirely new emotional experience domains',
     'Deepening of existing emotional experiences',
     'No change in emotional landscape',
     'Shallowing of emotional contact',
     'Severe emotional isolation'),
    ('meaning', 'Meaning & Purpose', '意味・目的',
     'Sense of purpose, existential fulfillment, ikigai',
     'Ikigai-9, PERMA-M, Ryff Purpose in Life, Steger MLQ',
     'Fundamental expansion of life meaning',
     'Creation of new purpose and direction',
     'No change',
     'Weakening of existing meaning systems',
     'Promotion of existential emptiness'),
    ('relational', 'Relational Belonging', '関係性・帰属',
     'Quality and depth of social connections, community bonds',
     'PERMA-R, Ryff Positive Relations, Social Connectedness Scale',
     'Creation of entirely new modes of social bonding',
     'Strengthening of existing relationships',
     'No change',
     'Superficialization of relationships',
     'Structural promotion of social isolation'),
    ('autonomy', 'Autonomy & Growth', '自律・成長',
     'Freedom of choice, personal growth opportunities',
     'Sen Capability Approach, Ryff Autonomy, Ryff Personal Growth',
     'Fundamental expansion of personal autonomy',
     'Expansion of growth opportunities',
     'No change',
     'Creation of new dependencies',
     'Structural deprivation of autonomy'),
    ('cultural', 'Cultural Sensitivity', '文化的感受性',
     'Cultural diversity, depth of cultural expression, receptivity to impermanence',
     'GNH Cultural Dimension, Mono no Aware, Wabi-Sabi, Cultural Intelligence Scale',
     'Increase in cultural diversity and depth',
     'New forms of cultural expression',
     'No change',
     'Cultural homogenization',
     'Loss of traditional cultural capital'),
]


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)

    # Seed 6 QoL dimensions
    for dim in SEED_DIMENSIONS:
        conn.execute("""
            INSERT OR IGNORE INTO qol_dimensions
            (code, name, name_ja, description, academic_foundations,
             scoring_criteria_plus5, scoring_criteria_plus3,
             scoring_criteria_zero, scoring_criteria_minus3, scoring_criteria_minus5)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, dim)

    conn.commit()

    # Report
    cursor = conn.cursor()
    tables = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    print(f"DB1 initialized: {DB_PATH}")
    print(f"Tables ({len(tables)}):")
    for t in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM [{t[0]}]").fetchone()[0]
        print(f"  {t[0]}: {count} rows")

    conn.close()


if __name__ == '__main__':
    init_db()
