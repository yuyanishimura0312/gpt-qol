"""
Seed DB1 with QoL frameworks, measurement scales, and tech-QoL evidence
from research team findings.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'qol_sensibility.db')


def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()

    # ============================================================
    # SOURCES
    # ============================================================
    sources = [
        # Capability Approach
        ("Development as Freedom", "Amartya Sen", 1999, "Oxford University Press", None,
         "book", 0, 0.95, None, "Foundational text on capability approach to human development"),
        ("Women and Human Development: The Capabilities Approach", "Martha Nussbaum", 2000,
         "Cambridge University Press", None, "book", 0, 0.95, None,
         "Defines 10 Central Human Capabilities including senses/imagination/thought and emotions"),
        ("Creating Capabilities: The Human Development Approach", "Martha Nussbaum", 2011,
         "Harvard University Press", None, "book", 0, 0.95, None,
         "Updated capabilities framework with policy applications"),
        # Subjective Well-being
        ("The Satisfaction with Life Scale", "Ed Diener; Robert A. Emmons; Randy J. Larsen; Sharon Griffin",
         1985, "Journal of Personality Assessment", "10.1207/s15327752jpa4901_13",
         "academic_peer_reviewed", 1, 0.95, None,
         "5-item scale measuring global cognitive life satisfaction. Cronbach alpha=0.87"),
        ("Development and validation of brief measures of positive and negative affect: The PANAS scales",
         "David Watson; Lee Anna Clark; Auke Tellegen", 1988,
         "Journal of Personality and Social Psychology", "10.1037/0022-3514.54.6.1063",
         "academic_peer_reviewed", 1, 0.95, None,
         "20-item Positive and Negative Affect Schedule"),
        # Psychological Well-being
        ("Happiness Is Everything, or Is It? Explorations on the Meaning of Psychological Well-Being",
         "Carol D. Ryff", 1989, "Journal of Personality and Social Psychology",
         "10.1037/0022-3514.57.6.1069", "academic_peer_reviewed", 1, 0.95, None,
         "6-dimension model: self-acceptance, positive relations, autonomy, environmental mastery, purpose, growth"),
        # Flow
        ("Flow: The Psychology of Optimal Experience", "Mihaly Csikszentmihalyi", 1990,
         "Harper & Row", None, "book", 0, 0.95, None,
         "Foundational theory of flow states and optimal experience"),
        ("Beyond Boredom and Anxiety: Experiencing Flow in Work and Play",
         "Mihaly Csikszentmihalyi", 1975, "Jossey-Bass", None, "book", 0, 0.90, None,
         "Early formulation of flow theory with Experience Sampling Method"),
        # PERMA
        ("Flourish: A Visionary New Understanding of Happiness and Well-being",
         "Martin E.P. Seligman", 2011, "Free Press", None, "book", 0, 0.95, None,
         "PERMA model: Positive Emotion, Engagement, Relationships, Meaning, Accomplishment"),
        # Kama Muta
        ("It Is Not Just a Feeling, but a Social Emotion: Kama Muta",
         "Thomas Fessler; Alan Page Fiske; et al.", 2019,
         "Cognition and Emotion", "10.1080/02699931.2019.1576664",
         "academic_peer_reviewed", 1, 0.90, None,
         "Kama Muta Multiplex Scale validated across 19 countries, 15 languages, 3542 participants"),
        # Awe
        ("The Awe Experience: A Meta-Analysis",
         "Dacher Keltner; Jonathan Haidt", 2003,
         "Cognition and Emotion", "10.1080/02699930302297",
         "academic_peer_reviewed", 1, 0.90, None,
         "Foundational theory of awe as self-transcendent emotion"),
        ("Development and Validation of the Awe Experience Scale (AWE-S)",
         "David B. Yaden; Scott Barry Kaufman; et al.", 2018,
         "The Journal of Positive Psychology", "10.1080/17439760.2018.1484940",
         "academic_peer_reviewed", 1, 0.90, None,
         "6-factor scale: vastness, time dilation, self-diminishment, connectedness, physical sensations, need for accommodation"),
        # Ikigai
        ("Ikigai and mortality in older Japanese adults",
         "Toshimasa Sone; Naoki Nakaya; et al.", 2008,
         "Psychosomatic Medicine", "10.1097/PSY.0b013e31817e7e64",
         "academic_peer_reviewed", 1, 0.90, None,
         "7-year cohort study: ikigai associated with reduced mortality. Functional disability -31%, dementia -36%"),
        # GNH
        ("A Short Guide to Gross National Happiness Index",
         "Centre for Bhutan Studies", 2012,
         "Centre for Bhutan Studies", None,
         "institutional_report", 0, 0.85, None,
         "GNH Index methodology: 9 domains, 33 indicators, Alkire-Foster sufficiency approach"),
        # OECD
        ("How's Life? Measuring Well-being",
         "OECD", 2011, "OECD Publishing", "10.1787/9789264121164-en",
         "institutional_report", 0, 0.90, None,
         "Better Life Index: 11 dimensions with user-adjustable weights"),
        # Hedonic Adaptation
        ("Lottery Winners and Accident Victims: Is Happiness Relative?",
         "Philip Brickman; Dan Coates; Ronnie Janoff-Bulman", 1978,
         "Journal of Personality and Social Psychology", "10.1037/0022-3514.36.8.917",
         "academic_peer_reviewed", 1, 0.90, None,
         "Foundational hedonic adaptation study"),
        # Aesthetic Experience
        ("Aesthetic Experience Questionnaire: A Scale for Measuring Aesthetic Engagement with Art",
         "Aaron Kozbelt; et al.", 2014, "Psychology of Aesthetics, Creativity, and the Arts",
         None, "academic_peer_reviewed", 1, 0.85, None,
         "Measures flow-like states during visual art appreciation"),
        # Music aesthetics
        ("Thrills, chills, frissons, and skin orgasms: toward an integrative model of transcendent psychophysiological experiences in music",
         "Luke Harrison; Psyche Loui", 2014,
         "Frontiers in Psychology", "10.3389/fpsyg.2014.00790",
         "academic_peer_reviewed", 1, 0.85, None,
         "Chills/thrills as physiological markers of aesthetic emotion in music"),
        # Digital Well-being
        ("How's Life in the Digital Age?",
         "OECD", 2024, "OECD Publishing", None,
         "institutional_report", 0, 0.85, None,
         "Framework for digital technology impact on QoL: affective, cognitive, social dimensions"),
        # Social Connection
        ("Social Connectedness in Physical, Online, and Hybrid Social Contexts",
         "Various", 2023, "Foundation for Social Connection", None,
         "institutional_report", 0, 0.80, None,
         "CDCS: 14-item Connection During Conversations Scale"),
        # Japanese Aesthetics
        ("Japanese Aesthetics", "Graham Parkes; Adam Loughnane", 2023,
         "Stanford Encyclopedia of Philosophy", None,
         "book_chapter", 0, 0.90, None,
         "Comprehensive treatment of mono no aware, wabi-sabi, ma, ikigai in philosophical context"),
        # MCDA
        ("Multi-Criteria Decision-Making for Quality of Life Assessment",
         "Various", 2021, "Sustainability (MDPI)", None,
         "academic_peer_reviewed", 1, 0.80, None,
         "TOPSIS, VIKOR, SAW, ELECTRE algorithms for composite QoL scoring"),
    ]

    source_ids = {}
    for s in sources:
        cur.execute("""
            INSERT OR IGNORE INTO sources (title, authors, year, journal, doi,
                source_type, peer_reviewed, credibility_score, url, abstract)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, s)
        if cur.lastrowid:
            source_ids[s[0]] = cur.lastrowid
        else:
            row = cur.execute("SELECT id FROM sources WHERE title = ?", (s[0],)).fetchone()
            if row:
                source_ids[s[0]] = row[0]

    # ============================================================
    # FRAMEWORKS
    # ============================================================
    frameworks = [
        ("Capability Approach", "ケイパビリティ・アプローチ", "Amartya Sen", 1999,
         "Development as Freedom", "capability", 5, "India/Global",
         "Freedom to achieve valued functionings, not just resources",
         "Choice and freedom as core of well-being, not material possession",
         "Technology should expand capabilities (freedoms), not just efficiency"),
        ("Central Human Capabilities", "中心的人間能力", "Martha Nussbaum", 2000,
         "Women and Human Development: The Capabilities Approach", "capability", 10, "USA/Global",
         "10 capabilities essential for human dignity and flourishing",
         "Senses/Imagination/Thought and Emotions as distinct capabilities",
         "Technology must support aesthetic and emotional capabilities, not just functional ones"),
        ("Satisfaction with Life Scale (SWLS)", "人生満足度尺度", "Ed Diener", 1985,
         "The Satisfaction with Life Scale", "subjective_wellbeing", 1, "USA",
         "Global cognitive assessment of life satisfaction on 7-point Likert scale",
         "Cognitive evaluation distinct from emotional well-being. Alpha=0.87",
         "Measures overall satisfaction but misses aesthetic/emotional richness"),
        ("PANAS", "ポジティブ・ネガティブ感情尺度", "David Watson; Lee Anna Clark; Auke Tellegen", 1988,
         "Development and validation of brief measures of positive and negative affect: The PANAS scales",
         "hedonic", 2, "USA",
         "20-item scale measuring positive and negative affect independently",
         "PA and NA are independent dimensions, not opposites. Correlation with SWLS ~0.44",
         "Captures emotional valence but not complexity or depth of aesthetic experience"),
        ("Psychological Well-being Scales", "心理的幸福感尺度", "Carol D. Ryff", 1989,
         "Happiness Is Everything, or Is It? Explorations on the Meaning of Psychological Well-Being",
         "psychological_wellbeing", 6, "USA",
         "6 dimensions: self-acceptance, positive relations, autonomy, environmental mastery, purpose, growth",
         "Eudaimonic approach grounded in Aristotelian philosophy of optimal human functioning",
         "Autonomy and Personal Growth dimensions directly relevant to technology-mediated QoL"),
        ("Flow Theory", "フロー理論", "Mihaly Csikszentmihalyi", 1990,
         "Flow: The Psychology of Optimal Experience", "aesthetic", 8, "USA/Hungary",
         "Optimal experience when challenge matches skill: action-awareness merging, loss of self-consciousness",
         "Experience Sampling Method (ESM) for real-time measurement in daily life",
         "Technology can create or destroy flow states; key to aesthetic QoL dimension"),
        ("PERMA Model", "PERMAモデル", "Martin E.P. Seligman", 2011,
         "Flourish: A Visionary New Understanding of Happiness and Well-being",
         "composite", 5, "USA",
         "5 pillars: Positive Emotion, Engagement (flow), Relationships, Meaning, Accomplishment",
         "Integrates hedonic and eudaimonic approaches. Engagement=flow theory connection",
         "Comprehensive but may underweight aesthetic and cultural sensitivity dimensions"),
        ("Kama Muta Scale", "カマムタ尺度", "Alan Page Fiske; Thomas Fessler", 2019,
         "It Is Not Just a Feeling, but a Social Emotion: Kama Muta",
         "aesthetic", 4, "Cross-cultural (19 countries)",
         "Measures being moved/touched: tears, chills, warmth. Social emotion of communal sharing intensification",
         "Validated across 19 countries, 15 languages, 3542 participants. Cross-cultural robustness",
         "Captures deep social-emotional experiences that technology may enhance or diminish"),
        ("Awe Experience Scale (AWE-S)", "畏敬体験尺度", "David B. Yaden; Scott Barry Kaufman", 2018,
         "Development and Validation of the Awe Experience Scale (AWE-S)",
         "aesthetic", 6, "USA",
         "6 factors: vastness, time dilation, self-diminishment, connectedness, physical sensations, accommodation need",
         "Self-transcendent emotion linked to meaning and prosocial behavior",
         "Awe experiences may be enhanced or reduced by technology; VR awe is emerging research area"),
        ("Ikigai Scale (Ikigai-9)", "生きがい尺度", "Various (based on Kamiya 1966)", 2008,
         "Ikigai and mortality in older Japanese adults",
         "eudaimonic", 1, "Japan",
         "Sense of life worth living. 9-item scale validated in English, French, German",
         "Not just happiness but existential fulfillment. 7-year mortality reduction. Functional disability -31%",
         "Distinct from SWB; closer to meaning/purpose. Technology should support ikigai, not replace it"),
        ("Gross National Happiness (GNH)", "国民総幸福量", "Centre for Bhutan Studies", 2012,
         "A Short Guide to Gross National Happiness Index",
         "national_index", 9, "Bhutan",
         "9 domains, 33 indicators. Alkire-Foster sufficiency approach. 66% threshold for happiness",
         "Buddhist values: interdependence, spiritual fulfillment. Cultural diversity as domain",
         "Alternative paradigm to GDP. Policy screening tool, not just measurement"),
        ("OECD Better Life Index", "OECD より良い暮らし指標", "OECD", 2011,
         "How's Life? Measuring Well-being",
         "national_index", 11, "Global (OECD countries)",
         "11 dimensions with user-adjustable weights. Acknowledges value pluralism",
         "User sets own weights: no single definition of good life. Life satisfaction included",
         "Most comprehensive international framework but may underweight aesthetic/cultural dimensions"),
        ("Hedonic Adaptation Level Theory", "快楽適応水準理論",
         "Philip Brickman; Dan Coates", 1978,
         "Lottery Winners and Accident Victims: Is Happiness Relative?",
         "hedonic", 1, "USA",
         "People return to baseline happiness after major life events",
         "Set-point is not immutable; modifiable by temperament and multiple well-being components",
         "Technology novelty fades but may shift baseline through new aesthetic/social opportunities"),
        ("Aesthetic Experience Questionnaire (AEQ)", "美的経験質問票",
         "Aaron Kozbelt", 2014,
         "Aesthetic Experience Questionnaire: A Scale for Measuring Aesthetic Engagement with Art",
         "aesthetic", 4, "USA",
         "Flow-like states during visual art appreciation",
         "Measures aesthetic engagement specifically, not general well-being",
         "Direct measure of aesthetic QoL dimension; applicable to technology-mediated art experiences"),
    ]

    for f in frameworks:
        src_id = source_ids.get(f[4])
        cur.execute("""
            INSERT OR IGNORE INTO frameworks
            (name, name_ja, authors, year, source_id, framework_type,
             dimensions_count, cultural_origin, description, key_insight, relevance_to_tech)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (f[0], f[1], f[2], f[3], src_id, f[5], f[6], f[7], f[8], f[9], f[10]))

    # ============================================================
    # MEASUREMENT SCALES
    # ============================================================
    scales = [
        ("Satisfaction with Life Scale", "SWLS", "Ed Diener et al.", 1985,
         "The Satisfaction with Life Scale", 5, "likert", "Adults",
         "40+ languages", 0.87, "5 items, 7-point Likert. Cognitive life satisfaction"),
        ("Positive and Negative Affect Schedule", "PANAS", "Watson, Clark & Tellegen", 1988,
         "Development and validation of brief measures of positive and negative affect: The PANAS scales",
         20, "likert", "Adults", "30+ languages", 0.88,
         "10 PA + 10 NA items. Independent dimensions"),
        ("Ryff Psychological Well-being Scales", "Ryff PWB", "Carol D. Ryff", 1989,
         "Happiness Is Everything, or Is It? Explorations on the Meaning of Psychological Well-Being",
         84, "likert", "Adults", "20+ languages", 0.86,
         "84/42/18-item versions. 6 eudaimonic dimensions"),
        ("Flow State Scale", "FSS", "Susan Jackson & Mihaly Csikszentmihalyi", 1996,
         None, 36, "likert", "Adults", "10+ languages", 0.85,
         "9 dimensions of flow experience. Also short form FSS-2 (9 items)"),
        ("Experience Sampling Method", "ESM", "Mihaly Csikszentmihalyi", 1975,
         "Beyond Boredom and Anxiety: Experiencing Flow in Work and Play",
         0, "experience_sampling", "All ages", "Multiple", None,
         "Real-time daily life measurement via random prompts. Minimizes recall bias"),
        ("PERMA-Profiler", "PERMA", "Martin Seligman et al.", 2016,
         None, 23, "likert", "Adults", "15+ languages", 0.89,
         "23 items across 5 PERMA domains + 3 filler items"),
        ("Kama Muta Multiplex Scale", "KAMMUS", "Alan Page Fiske et al.", 2019,
         "It Is Not Just a Feeling, but a Social Emotion: Kama Muta",
         0, "composite", "Adults", "15 languages", 0.88,
         "Multi-component: emotion labels, sensations, appraisals, motivation"),
        ("Awe Experience Scale", "AWE-S", "Yaden & Kaufman et al.", 2018,
         "Development and Validation of the Awe Experience Scale (AWE-S)",
         30, "likert", "Adults", "5+ languages", 0.90,
         "6-factor structure capturing self-transcendent awe"),
        ("Ikigai-9 Scale", "Ikigai-9", "Various", 2008,
         "Ikigai and mortality in older Japanese adults",
         9, "likert", "Older adults", "Japanese, English, French, German", 0.83,
         "9 items measuring sense of life worth living"),
        ("Meaning in Life Questionnaire", "MLQ", "Michael F. Steger et al.", 2006,
         None, 10, "likert", "Adults", "30+ languages", 0.86,
         "Two subscales: Presence of Meaning + Search for Meaning"),
        ("Social Connectedness Scale-Revised", "SCS-R", "Richard M. Lee et al.", 2001,
         None, 20, "likert", "Adults", "10+ languages", 0.92,
         "Measures sense of interpersonal closeness with the social world"),
        ("Gross National Happiness Index", "GNH", "Centre for Bhutan Studies", 2012,
         "A Short Guide to Gross National Happiness Index",
         33, "composite", "National population", "Dzongkha, English", None,
         "9 domains, 33 indicators. Sufficiency threshold approach"),
    ]

    for s in scales:
        src_id = source_ids.get(s[4]) if s[4] else None
        cur.execute("""
            INSERT OR IGNORE INTO measurement_scales
            (name, abbreviation, authors, year, source_id, items_count,
             scale_type, target_population, languages_validated,
             reliability_score, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (s[0], s[1], s[2], s[3], src_id, s[5], s[6], s[7], s[8], s[9], s[10]))

    # ============================================================
    # SCALE-DIMENSION MAPPINGS
    # ============================================================
    # Map each scale to our 6 QoL dimensions
    mappings = [
        ("SWLS", [("meaning", 0.6), ("emotional", 0.4)]),
        ("PANAS", [("emotional", 0.9), ("aesthetic", 0.3)]),
        ("Ryff PWB", [("autonomy", 0.9), ("relational", 0.8), ("meaning", 0.8),
                      ("emotional", 0.6), ("cultural", 0.3)]),
        ("FSS", [("aesthetic", 0.9), ("emotional", 0.7), ("autonomy", 0.5)]),
        ("ESM", [("aesthetic", 0.8), ("emotional", 0.8), ("relational", 0.6),
                 ("meaning", 0.5), ("autonomy", 0.4), ("cultural", 0.3)]),
        ("PERMA", [("emotional", 0.8), ("relational", 0.8), ("meaning", 0.8),
                   ("aesthetic", 0.6), ("autonomy", 0.5)]),
        ("KAMMUS", [("emotional", 0.9), ("relational", 0.8), ("cultural", 0.5)]),
        ("AWE-S", [("aesthetic", 0.9), ("emotional", 0.8), ("meaning", 0.7),
                   ("cultural", 0.6)]),
        ("Ikigai-9", [("meaning", 0.95), ("emotional", 0.6), ("cultural", 0.7)]),
        ("MLQ", [("meaning", 0.95), ("autonomy", 0.5)]),
        ("SCS-R", [("relational", 0.95), ("emotional", 0.5)]),
        ("GNH", [("cultural", 0.9), ("meaning", 0.8), ("relational", 0.7),
                 ("emotional", 0.6), ("autonomy", 0.6), ("aesthetic", 0.4)]),
    ]

    for abbr, dims in mappings:
        scale_row = cur.execute(
            "SELECT id FROM measurement_scales WHERE abbreviation = ?", (abbr,)
        ).fetchone()
        if scale_row:
            for dim, score in dims:
                cur.execute("""
                    INSERT OR IGNORE INTO scale_dimension_mapping
                    (scale_id, qol_dimension, coverage_score)
                    VALUES (?, ?, ?)
                """, (scale_row[0], dim, score))

    conn.commit()

    # Report
    tables = ["sources", "frameworks", "measurement_scales", "scale_dimension_mapping"]
    print("DB1 seeded:")
    for t in tables:
        count = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {count} rows")

    conn.close()


if __name__ == '__main__':
    seed()
