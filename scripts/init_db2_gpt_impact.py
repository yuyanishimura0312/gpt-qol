"""
DB2: GPT Impact Genealogy Database
Historical general-purpose technology usage and its quality-of-life impact genealogy.
Focus: Automobile, Telephone, Printing Press (+ Electricity, Steam Engine as auxiliary).
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'gpt_impact_genealogy.db')

SCHEMA = """
-- Sources
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
        'conference_paper', 'thesis', 'grey_literature',
        'historical_primary', 'archive'
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
    UNIQUE(source_id, author_name)
);

-- GPT Technologies master
CREATE TABLE IF NOT EXISTS gpt_technologies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    name_ja TEXT NOT NULL,
    year_invention INTEGER,
    year_mass_adoption INTEGER,
    year_maturity INTEGER,
    inventor TEXT,
    region_origin TEXT,
    gpt_criteria_pervasiveness TEXT,
    gpt_criteria_improvement TEXT,
    gpt_criteria_complementarity TEXT,
    is_primary INTEGER DEFAULT 1,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Usage events (nodes in the genealogy)
CREATE TABLE IF NOT EXISTS usage_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gpt_id INTEGER NOT NULL REFERENCES gpt_technologies(id),
    name TEXT NOT NULL,
    name_ja TEXT,
    year_start INTEGER,
    year_end INTEGER,
    year_confidence TEXT CHECK(year_confidence IN (
        'exact', 'decade', 'quarter_century', 'century', 'estimated'
    )) DEFAULT 'decade',
    region TEXT,
    domain TEXT CHECK(domain IN (
        'transportation', 'communication', 'culture', 'education',
        'leisure', 'domestic', 'commerce', 'social', 'spiritual',
        'artistic', 'political', 'healthcare', 'labor', 'urban',
        'rural', 'military', 'scientific', 'other'
    )),
    event_type TEXT CHECK(event_type IN (
        'economic', 'cultural', 'social', 'aesthetic',
        'spiritual', 'political', 'technological', 'mixed'
    )),
    description TEXT,
    trigger_pattern TEXT,
    -- 6-dimension QoL scores (-5 to +5)
    score_aesthetic INTEGER CHECK(score_aesthetic BETWEEN -5 AND 5),
    score_emotional INTEGER CHECK(score_emotional BETWEEN -5 AND 5),
    score_meaning INTEGER CHECK(score_meaning BETWEEN -5 AND 5),
    score_relational INTEGER CHECK(score_relational BETWEEN -5 AND 5),
    score_autonomy INTEGER CHECK(score_autonomy BETWEEN -5 AND 5),
    score_cultural INTEGER CHECK(score_cultural BETWEEN -5 AND 5),
    -- Economic impact axis
    score_economic_macro INTEGER CHECK(score_economic_macro BETWEEN -5 AND 5),
    -- Computed: QoL composite (average of 6 dimensions)
    qol_composite REAL,
    -- Metadata
    intended_by_inventor INTEGER DEFAULT 0,
    adoption_path_type TEXT CHECK(adoption_path_type IN (
        'linear', 'serendipitous', 'repurposed', 'grassroots',
        'resistance', 'appropriation', 'hybridization'
    )),
    quadrant TEXT CHECK(quadrant IN ('I', 'II', 'III', 'IV')),
    evidence_strength TEXT CHECK(evidence_strength IN (
        'strong', 'moderate', 'suggestive', 'anecdotal'
    )),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Triggers to auto-compute qol_composite and quadrant
CREATE TRIGGER IF NOT EXISTS compute_qol_composite_insert
AFTER INSERT ON usage_events
BEGIN
    UPDATE usage_events SET
        qol_composite = (
            COALESCE(NEW.score_aesthetic, 0) +
            COALESCE(NEW.score_emotional, 0) +
            COALESCE(NEW.score_meaning, 0) +
            COALESCE(NEW.score_relational, 0) +
            COALESCE(NEW.score_autonomy, 0) +
            COALESCE(NEW.score_cultural, 0)
        ) / 6.0,
        quadrant = CASE
            WHEN (COALESCE(NEW.score_aesthetic, 0) + COALESCE(NEW.score_emotional, 0) +
                  COALESCE(NEW.score_meaning, 0) + COALESCE(NEW.score_relational, 0) +
                  COALESCE(NEW.score_autonomy, 0) + COALESCE(NEW.score_cultural, 0)) > 0
                 AND COALESCE(NEW.score_economic_macro, 0) > 0 THEN 'I'
            WHEN (COALESCE(NEW.score_aesthetic, 0) + COALESCE(NEW.score_emotional, 0) +
                  COALESCE(NEW.score_meaning, 0) + COALESCE(NEW.score_relational, 0) +
                  COALESCE(NEW.score_autonomy, 0) + COALESCE(NEW.score_cultural, 0)) > 0
                 AND COALESCE(NEW.score_economic_macro, 0) <= 0 THEN 'II'
            WHEN (COALESCE(NEW.score_aesthetic, 0) + COALESCE(NEW.score_emotional, 0) +
                  COALESCE(NEW.score_meaning, 0) + COALESCE(NEW.score_relational, 0) +
                  COALESCE(NEW.score_autonomy, 0) + COALESCE(NEW.score_cultural, 0)) <= 0
                 AND COALESCE(NEW.score_economic_macro, 0) <= 0 THEN 'III'
            ELSE 'IV'
        END
    WHERE id = NEW.id;
END;

-- Event relations (genealogy network)
CREATE TABLE IF NOT EXISTS event_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_event_id INTEGER NOT NULL REFERENCES usage_events(id),
    to_event_id INTEGER NOT NULL REFERENCES usage_events(id),
    relation_type TEXT NOT NULL CHECK(relation_type IN (
        'enabled', 'inspired', 'opposed', 'evolved_from',
        'parallel', 'prerequisite', 'amplified', 'constrained'
    )),
    strength REAL CHECK(strength BETWEEN 0 AND 1),
    time_lag_years INTEGER,
    description TEXT,
    UNIQUE(from_event_id, to_event_id, relation_type)
);

-- Non-linear adoption paths
CREATE TABLE IF NOT EXISTS adoption_paths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gpt_id INTEGER NOT NULL REFERENCES gpt_technologies(id),
    path_name TEXT NOT NULL,
    path_name_ja TEXT,
    path_description TEXT,
    intended_use TEXT,
    actual_use TEXT,
    pivot_year INTEGER,
    pivot_trigger TEXT,
    qol_impact_summary TEXT,
    path_type TEXT CHECK(path_type IN (
        'serendipity', 'repurpose', 'grassroots', 'resistance',
        'appropriation', 'creative_misuse', 'democratization'
    )),
    -- Link to related events
    source_id INTEGER REFERENCES sources(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Event-evidence linkage
CREATE TABLE IF NOT EXISTS event_evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL REFERENCES usage_events(id),
    source_id INTEGER NOT NULL REFERENCES sources(id),
    claim_summary TEXT,
    evidence_type TEXT CHECK(evidence_type IN (
        'quantitative', 'qualitative', 'historical_analysis',
        'case_study', 'survey', 'ethnography', 'archival',
        'statistical', 'theoretical'
    )),
    confidence_level TEXT CHECK(confidence_level IN (
        'high', 'medium', 'low', 'speculative'
    )),
    UNIQUE(event_id, source_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_events_gpt ON usage_events(gpt_id);
CREATE INDEX IF NOT EXISTS idx_events_quadrant ON usage_events(quadrant);
CREATE INDEX IF NOT EXISTS idx_events_year ON usage_events(year_start);
CREATE INDEX IF NOT EXISTS idx_events_path_type ON usage_events(adoption_path_type);
CREATE INDEX IF NOT EXISTS idx_relations_from ON event_relations(from_event_id);
CREATE INDEX IF NOT EXISTS idx_relations_to ON event_relations(to_event_id);
CREATE INDEX IF NOT EXISTS idx_paths_gpt ON adoption_paths(gpt_id);
"""

# Seed data: 5 GPT technologies
SEED_GPTS = [
    ('Automobile', '自動車', 1886, 1920, 1960,
     'Karl Benz / Henry Ford', 'Germany/USA',
     'Transportation, logistics, urban planning, culture, leisure',
     'Continuous improvement in speed, safety, fuel efficiency, autonomous driving',
     'Enabled suburban development, tourism industry, drive-in culture, road infrastructure',
     1, 'Internal combustion engine vehicle enabling personal mobility'),
    ('Telephone', '電話', 1876, 1920, 1960,
     'Alexander Graham Bell', 'USA/UK',
     'Communication, business, social relations, emergency services',
     'From wired to wireless, analog to digital, voice to multimedia',
     'Enabled real-time remote communication, transformed social relations and business',
     1, 'Voice communication technology enabling real-time remote interaction'),
    ('Printing Press', '印刷術', 1440, 1500, 1600,
     'Johannes Gutenberg', 'Germany',
     'Education, religion, science, governance, literature, journalism',
     'From movable type to lithography to offset to digital',
     'Enabled mass literacy, scientific revolution, Protestant reformation',
     1, 'Movable type printing enabling mass reproduction of written works'),
    ('Electricity', '電気', 1879, 1920, 1950,
     'Thomas Edison / Nikola Tesla', 'USA',
     'Domestic life, industry, entertainment, urban infrastructure',
     'From DC to AC, centralized to distributed generation',
     'Enabled electric appliances, nightlife, radio, industrial automation',
     0, 'Electrical power distribution enabling domestic and industrial transformation'),
    ('Steam Engine', '蒸気機関', 1712, 1830, 1900,
     'Thomas Newcomen / James Watt', 'UK',
     'Transportation, manufacturing, mining, agriculture',
     'From atmospheric to high-pressure to compound engines',
     'Enabled railways, factories, steamships, urbanization',
     0, 'Steam-powered mechanical engine enabling industrial revolution'),
]


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)

    # Seed GPT technologies
    for gpt in SEED_GPTS:
        conn.execute("""
            INSERT OR IGNORE INTO gpt_technologies
            (name, name_ja, year_invention, year_mass_adoption, year_maturity,
             inventor, region_origin, gpt_criteria_pervasiveness,
             gpt_criteria_improvement, gpt_criteria_complementarity,
             is_primary, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, gpt)

    conn.commit()

    # Report
    cursor = conn.cursor()
    tables = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    print(f"DB2 initialized: {DB_PATH}")
    print(f"Tables ({len(tables)}):")
    for t in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM [{t[0]}]").fetchone()[0]
        print(f"  {t[0]}: {count} rows")

    conn.close()


if __name__ == '__main__':
    init_db()
