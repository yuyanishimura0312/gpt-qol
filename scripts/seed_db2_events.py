"""
Seed DB2 with historical GPT usage events and their QoL impact scores.
Data from GPT theory research team findings.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'gpt_impact_genealogy.db')


def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()

    # Get GPT IDs
    gpt_ids = {}
    for row in cur.execute("SELECT id, name FROM gpt_technologies"):
        gpt_ids[row[1]] = row[0]

    auto_id = gpt_ids["Automobile"]
    tel_id = gpt_ids["Telephone"]
    print_id = gpt_ids["Printing Press"]
    elec_id = gpt_ids["Electricity"]
    steam_id = gpt_ids["Steam Engine"]

    # ============================================================
    # USAGE EVENTS — Automobile
    # ============================================================
    auto_events = [
        # (name, name_ja, year_start, year_end, year_conf, region, domain, event_type,
        #  description, trigger,
        #  aesthetic, emotional, meaning, relational, autonomy, cultural, economic,
        #  intended, path_type, evidence)
        ("Mass Production (Ford Model T)", "大量生産（フォードT型）",
         1908, 1927, "exact", "USA", "commerce", "economic",
         "Henry Ford's assembly line made automobiles affordable for middle class",
         "Industrial innovation + consumer demand",
         0, 0, 1, 0, 3, 0, 5, 1, "linear", "strong"),
        ("Suburbanization", "郊外化",
         1920, 1970, "decade", "USA", "urban", "social",
         "Automobile enabled low-density suburban living with long-distance commuting. Federal highway subsidies amplified effect",
         "Automobile + federal road construction subsidies",
         -1, -2, 0, -3, 3, -2, 4, 0, "serendipitous", "strong"),
        ("Road Trip Culture", "ロードトリップ文化",
         1930, None, "decade", "USA", "leisure", "cultural",
         "Family road trips to remote destinations became major leisure activity. New emotional experiences of adventure and freedom",
         "Affordable cars + highway system",
         3, 4, 2, 2, 4, 3, 2, 0, "grassroots", "strong"),
        ("Drive-in Cinema", "ドライブインシネマ",
         1933, 1980, "exact", "USA", "leisure", "aesthetic",
         "Outdoor movie theaters combining automobile comfort with cinema. Peak in 1950s-60s",
         "Automobile culture + cinema technology",
         4, 3, 1, 3, 2, 3, 2, 0, "serendipitous", "moderate"),
        ("Dating Culture Transformation", "デーティング文化の変容",
         1950, 1970, "decade", "USA", "social", "social",
         "Car as 'second living room' freed teens from parental supervision. Dating shifted from home visits to driving",
         "Youth automobile ownership + desire for autonomy",
         1, 3, 1, 3, 4, 2, 0, 0, "grassroots", "moderate"),
        ("Drive-in Restaurants", "ドライブイン飲食店",
         1940, 1970, "decade", "USA", "leisure", "cultural",
         "Carhop service, car-centered dining. New social interaction patterns",
         "Automobile culture + food service innovation",
         2, 2, 0, 3, 2, 2, 2, 0, "serendipitous", "moderate"),
        ("Personal Freedom Symbol", "個人的自由の象徴",
         1920, None, "decade", "USA/Global", "social", "cultural",
         "Automobile became cultural icon of individual freedom, mobility, independence. Especially powerful in American culture",
         "Mass ownership + cultural narratives",
         2, 3, 3, 0, 5, 3, 1, 0, "grassroots", "strong"),
        ("Social Isolation via Car-Centric Design", "自動車中心設計による社会的孤立",
         1950, None, "decade", "USA", "urban", "social",
         "Car-optimized cities reduced spontaneous social encounters. Vance Packard: geographic mobility causes isolation",
         "Suburban sprawl + zoning laws",
         -2, -3, -1, -4, 1, -3, 2, 0, "serendipitous", "strong"),
        ("Automobile as Art Form", "芸術としての自動車",
         1930, None, "decade", "Global", "artistic", "aesthetic",
         "Car design as industrial art. Streamlining, chrome aesthetics, concept cars. Museums dedicated to automotive design",
         "Mass production + design competition",
         4, 2, 1, 0, 0, 3, 3, 0, "serendipitous", "moderate"),
        ("Environmental Pollution", "環境汚染",
         1950, None, "decade", "Global", "other", "mixed",
         "Air pollution, noise pollution, CO2 emissions. Loss of quiet urban spaces",
         "Mass automobile use",
         -3, -1, -1, 0, 0, -2, -1, 0, "serendipitous", "strong"),
        ("Women's Mobility", "女性の移動の自由",
         1920, 1960, "decade", "USA/Europe", "social", "social",
         "Automobile gave women independent mobility beyond walking/transit range",
         "Women's suffrage movement + automobile affordability",
         0, 2, 2, 1, 4, 1, 1, 0, "appropriation", "moderate"),
    ]

    # ============================================================
    # USAGE EVENTS — Telephone
    # ============================================================
    tel_events = [
        ("Business Communication Tool", "ビジネス通信ツール",
         1876, 1920, "decade", "USA/UK", "communication", "economic",
         "Bell's original vision: business dictation and communication. Initial adoption by businesses",
         "Invention + business efficiency demand",
         0, 0, 0, 0, 1, 0, 4, 1, "linear", "strong"),
        ("Social Chatting Culture", "おしゃべり文化",
         1900, None, "decade", "USA", "social", "social",
         "Telephone repurposed for personal conversations. Bell company initially discouraged non-business use. Users created 'chatting' as new social practice",
         "Users discovering social utility despite company resistance",
         0, 3, 1, 4, 2, 2, 0, 0, "repurpose", "strong"),
        ("Party Line Communities", "パーティーライン共同体",
         1890, 1960, "decade", "Rural USA", "social", "social",
         "Shared telephone lines in rural areas created new community bonds. Eavesdropping became social glue",
         "Rural telephone infrastructure limitations",
         0, 2, 1, 4, 0, 2, 0, 0, "serendipitous", "moderate"),
        ("Long-Distance Family Bonds", "遠距離家族の絆",
         1920, None, "decade", "Global", "social", "social",
         "Voice communication maintained family relationships across distances impossible by letter",
         "Long-distance telephone service + migration patterns",
         0, 4, 2, 5, 1, 1, 1, 0, "repurpose", "strong"),
        ("Telephone Operators as Women's Employment", "電話交換手と女性雇用",
         1880, 1960, "decade", "USA/Europe", "labor", "social",
         "Telephone operating became major women's profession. Young women gained economic independence",
         "Need for operators + gender norms about voice quality",
         0, 1, 2, 2, 3, 1, 3, 0, "serendipitous", "moderate"),
        ("Emergency Services (911)", "緊急通報サービス",
         1968, None, "exact", "USA", "healthcare", "social",
         "Universal emergency number enabled rapid response. Fundamental sense of safety and security",
         "Government policy + telephone ubiquity",
         0, 3, 1, 2, 2, 0, 2, 0, "linear", "strong"),
        ("Teen Phone Culture", "十代の電話文化",
         1950, 1990, "decade", "USA", "social", "cultural",
         "Teenagers claimed telephone as social lifeline. Hours-long calls, phone in bedroom as private space",
         "Youth culture + household telephone penetration",
         0, 3, 1, 4, 3, 2, 0, 0, "grassroots", "moderate"),
        ("Emotional Intimacy via Voice", "声による感情的親密さ",
         1900, None, "decade", "Global", "social", "aesthetic",
         "Voice carries emotional nuance that letters cannot. Laughter, tone, silence became part of relationship",
         "Inherent qualities of voice communication",
         2, 4, 2, 4, 0, 1, 0, 0, "serendipitous", "moderate"),
        ("Telephone Anxiety", "電話不安",
         1920, None, "decade", "Global", "social", "mixed",
         "Some people developed anxiety about telephone calls. Loss of visual cues, performance pressure",
         "Asymmetric communication medium",
         0, -2, 0, -1, -1, 0, 0, 0, "serendipitous", "suggestive"),
        ("Radio Broadcasting via Telephone Lines", "電話線によるラジオ放送",
         1920, 1950, "decade", "Europe", "culture", "aesthetic",
         "In some European countries, telephone networks used to distribute radio-like content before radio receivers were common",
         "Telephone infrastructure repurposed for entertainment",
         3, 2, 0, 1, 0, 2, 1, 0, "repurpose", "moderate"),
    ]

    # ============================================================
    # USAGE EVENTS — Printing Press
    # ============================================================
    print_events = [
        ("Bible Mass Production", "聖書の大量印刷",
         1455, 1520, "decade", "Europe", "spiritual", "spiritual",
         "Gutenberg Bible first mass-produced book. Made personal Bible ownership possible for first time",
         "Gutenberg invention + religious demand",
         2, 3, 5, 1, 4, 3, 3, 1, "linear", "strong"),
        ("Protestant Reformation", "プロテスタント改革",
         1517, 1648, "exact", "Europe", "spiritual", "spiritual",
         "Sola Scriptura enabled by printing: individuals could read and interpret Bible directly. Destroyed clerical monopoly on religious authority",
         "Printed Bible + Luther's theological challenge",
         1, 3, 5, 2, 5, 4, 1, 0, "serendipitous", "strong"),
        ("Republic of Letters", "文人共和国",
         1500, 1800, "quarter_century", "Europe", "education", "cultural",
         "Informal scholarly network across nations. Scientists and thinkers exchanged printed works and correspondence. First 'virtual community'",
         "Printed books + postal systems + scholarly curiosity",
         2, 2, 4, 4, 3, 4, 1, 0, "serendipitous", "strong"),
        ("Literacy Democratization", "識字の民主化",
         1450, 1800, "century", "Europe", "education", "social",
         "Literate population roughly doubled each century after printing. Foundation for universal education, free press, democratic governance",
         "Affordable printed materials + growing education demand",
         1, 1, 3, 2, 4, 3, 2, 0, "grassroots", "strong"),
        ("Scientific Revolution", "科学革命",
         1543, 1700, "decade", "Europe", "scientific", "cultural",
         "Printing enabled replication, verification, and cumulative development of scientific discoveries. Copernicus, Galileo, Newton disseminated via print",
         "Printed scientific texts + scholarly networks",
         2, 1, 4, 3, 3, 4, 2, 0, "serendipitous", "strong"),
        ("Vernacular Literature Flourishing", "各国語文学の隆盛",
         1500, 1700, "quarter_century", "Europe", "artistic", "aesthetic",
         "Printing in local languages (not just Latin) enabled national literary traditions. Shakespeare, Cervantes, Rabelais reached wide audiences",
         "Printing in vernacular + growing literate middle class",
         5, 4, 3, 2, 2, 5, 2, 0, "serendipitous", "strong"),
        ("Newspaper and Public Sphere", "新聞と公共圏",
         1600, 1800, "quarter_century", "Europe", "political", "political",
         "Printed newspapers created Habermasian public sphere. Citizens could form opinions on public affairs",
         "Printing technology + urban coffee house culture",
         1, 1, 2, 3, 3, 3, 3, 0, "serendipitous", "strong"),
        ("Pamphlet Wars and Propaganda", "パンフレット戦争とプロパガンダ",
         1517, 1800, "quarter_century", "Europe", "political", "political",
         "Cheap printed pamphlets as weapons of ideological warfare. Martin Luther's 95 Theses spread rapidly",
         "Low-cost printing + political/religious conflict",
         0, -1, 1, -1, 2, -1, 1, 0, "serendipitous", "strong"),
        ("Personal Reading as Private Experience", "個人的読書体験",
         1500, None, "quarter_century", "Europe", "leisure", "aesthetic",
         "Silent individual reading became new form of private aesthetic experience. Interior life enriched by imagined worlds",
         "Affordable books + literacy",
         5, 4, 4, -1, 4, 4, 0, 0, "serendipitous", "strong"),
        ("Music Score Printing", "楽譜の印刷",
         1501, 1700, "exact", "Europe", "artistic", "aesthetic",
         "Ottaviano Petrucci's music printing (1501) democratized musical knowledge. Amateur music-making flourished",
         "Movable type adapted for musical notation",
         4, 3, 2, 3, 3, 4, 2, 0, "serendipitous", "moderate"),
    ]

    # ============================================================
    # USAGE EVENTS — Electricity (auxiliary)
    # ============================================================
    elec_events = [
        ("Night-time Activity Expansion", "夜間活動の拡張",
         1890, 1930, "decade", "USA/Europe", "leisure", "cultural",
         "Electric lighting extended productive and leisure hours into night. Fundamentally restructured daily time",
         "Electric grid expansion + light bulb affordability",
         3, 2, 1, 2, 3, 2, 3, 0, "serendipitous", "strong"),
        ("Radio and Shared National Culture", "ラジオと共有国民文化",
         1920, 1950, "decade", "USA", "culture", "cultural",
         "Radio broadcast same content nationwide simultaneously. Kansas family and Manhattan family heard same comedy, baseball, presidential speeches",
         "Electric power + radio technology",
         3, 3, 1, 3, 0, 4, 3, 0, "serendipitous", "strong"),
        ("Domestic Electrification", "家庭の電化",
         1920, 1960, "decade", "USA/Europe", "domestic", "social",
         "Electric appliances (iron, washing machine, vacuum) changed domestic labor. Paradox: efficiency led to higher standards, not less work",
         "Electric grid + consumer appliance industry",
         1, 0, 0, 0, 1, 0, 4, 1, "linear", "strong"),
        ("Great White Way (Theater District)", "グレート・ホワイト・ウェイ（劇場街）",
         1895, 1930, "decade", "USA", "artistic", "aesthetic",
         "Electric illumination transformed urban entertainment districts. Amusement parks, nightlife, spectacle culture",
         "Electric lighting + urban entertainment culture",
         4, 3, 1, 2, 1, 3, 3, 0, "serendipitous", "moderate"),
    ]

    # ============================================================
    # USAGE EVENTS — Steam Engine (auxiliary)
    # ============================================================
    steam_events = [
        ("Birth of Tourism", "観光の誕生",
         1830, 1900, "decade", "UK/Europe", "leisure", "cultural",
         "Steam railways enabled mass tourism. Thomas Cook organized first package tours (1841). Leisure travel became middle-class activity",
         "Railway expansion + rising incomes",
         3, 3, 2, 2, 3, 3, 3, 0, "serendipitous", "strong"),
        ("Urbanization and Anonymous City", "都市化と匿名の都市",
         1800, 1900, "decade", "UK/Europe", "urban", "social",
         "London grew from 1.17M (1801) to 2.68M+ (1851). Small cohesive communities transformed into anonymous diverse urban spaces",
         "Steam-powered factories + railway networks",
         1, -1, 0, -2, 2, 1, 4, 0, "serendipitous", "strong"),
    ]

    # Insert all events
    all_events = [
        (auto_id, auto_events),
        (tel_id, tel_events),
        (print_id, print_events),
        (elec_id, elec_events),
        (steam_id, steam_events),
    ]

    for gpt_id, events in all_events:
        for e in events:
            cur.execute("""
                INSERT OR IGNORE INTO usage_events
                (gpt_id, name, name_ja, year_start, year_end, year_confidence,
                 region, domain, event_type, description, trigger_pattern,
                 score_aesthetic, score_emotional, score_meaning,
                 score_relational, score_autonomy, score_cultural,
                 score_economic_macro,
                 intended_by_inventor, adoption_path_type, evidence_strength)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (gpt_id, e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7],
                  e[8], e[9], e[10], e[11], e[12], e[13], e[14], e[15], e[16],
                  e[17], e[18], e[19]))

    # ============================================================
    # ADOPTION PATHS
    # ============================================================
    paths = [
        (auto_id, "Automobile Road Trip Detour", "自動車ロードトリップ迂回路",
         "Commercial transport tool becomes leisure and self-discovery vehicle",
         "Efficient long-distance transportation", "Family leisure, adventure, emotional freedom",
         1930, "Highway system + middle-class car ownership",
         "Quadrant shift from IV (economic efficiency) to II (emotional/aesthetic enrichment without direct economic value)",
         "grassroots"),
        (tel_id, "Telephone Social Chat Pivot", "電話おしゃべり転換",
         "Business communication device becomes social bonding tool",
         "Office dictation and business communication", "Personal chatting, relationship maintenance, emotional intimacy",
         1900, "Users defied Bell company's intended use",
         "Classic repurpose: from Quadrant IV to Quadrant I/II. Voice carries emotional nuance letters cannot",
         "repurpose"),
        (print_id, "Printing Press Spiritual Liberation", "印刷術による精神的解放",
         "Mass text reproduction enables individual spiritual interpretation",
         "Efficient copying of religious and scholarly texts", "Personal Bible reading, individual spiritual autonomy, Protestant Reformation",
         1517, "Luther's 95 Theses + affordable printed Bibles",
         "From Quadrant I (economic + cultural) to Quadrant II (deep meaning/purpose without economic motive)",
         "democratization"),
        (tel_id, "Party Line Community", "パーティーライン共同体",
         "Infrastructure limitation creates unexpected social bonds",
         "Shared line as cost-saving measure", "Community bonding through shared conversations and eavesdropping",
         1890, "Rural telephone infrastructure constraints",
         "Infrastructure limitation paradoxically created stronger social bonds than private lines",
         "serendipity"),
        (auto_id, "Women's Automobile Liberation", "女性の自動車解放",
         "Male-designed technology appropriated for women's mobility",
         "Male-oriented transportation tool", "Independent female mobility, expanded social and economic participation",
         1920, "Women's suffrage movement + automobile affordability",
         "Appropriation: marginalized group found empowerment through technology not designed for them",
         "appropriation"),
    ]

    for p in paths:
        cur.execute("""
            INSERT OR IGNORE INTO adoption_paths
            (gpt_id, path_name, path_name_ja, path_description,
             intended_use, actual_use, pivot_year, pivot_trigger,
             qol_impact_summary, path_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    # ============================================================
    # EVENT RELATIONS
    # ============================================================
    # Get event IDs by name
    event_ids = {}
    for row in cur.execute("SELECT id, name FROM usage_events"):
        event_ids[row[1]] = row[0]

    relations = [
        ("Mass Production (Ford Model T)", "Suburbanization", "enabled", 0.9, 12),
        ("Mass Production (Ford Model T)", "Road Trip Culture", "enabled", 0.8, 22),
        ("Mass Production (Ford Model T)", "Personal Freedom Symbol", "inspired", 0.7, 12),
        ("Suburbanization", "Social Isolation via Car-Centric Design", "enabled", 0.9, 30),
        ("Road Trip Culture", "Drive-in Cinema", "inspired", 0.6, 3),
        ("Road Trip Culture", "Drive-in Restaurants", "inspired", 0.6, 10),
        ("Personal Freedom Symbol", "Dating Culture Transformation", "inspired", 0.7, 30),
        ("Personal Freedom Symbol", "Women's Mobility", "inspired", 0.5, 0),
        ("Business Communication Tool", "Social Chatting Culture", "evolved_from", 0.9, 24),
        ("Social Chatting Culture", "Long-Distance Family Bonds", "enabled", 0.8, 20),
        ("Social Chatting Culture", "Teen Phone Culture", "enabled", 0.7, 50),
        ("Social Chatting Culture", "Emotional Intimacy via Voice", "enabled", 0.8, 0),
        ("Business Communication Tool", "Telephone Operators as Women's Employment", "enabled", 0.8, 4),
        ("Bible Mass Production", "Protestant Reformation", "enabled", 0.95, 62),
        ("Protestant Reformation", "Literacy Democratization", "amplified", 0.7, 0),
        ("Bible Mass Production", "Republic of Letters", "enabled", 0.6, 45),
        ("Literacy Democratization", "Vernacular Literature Flourishing", "enabled", 0.8, 50),
        ("Literacy Democratization", "Scientific Revolution", "enabled", 0.7, 93),
        ("Vernacular Literature Flourishing", "Personal Reading as Private Experience", "enabled", 0.8, 0),
        ("Scientific Revolution", "Newspaper and Public Sphere", "enabled", 0.5, 57),
        ("Night-time Activity Expansion", "Radio and Shared National Culture", "enabled", 0.7, 30),
        ("Night-time Activity Expansion", "Great White Way (Theater District)", "enabled", 0.8, 5),
        ("Birth of Tourism", "Road Trip Culture", "preceded", 0.6, 100),
    ]

    for r in relations:
        from_id = event_ids.get(r[0])
        to_id = event_ids.get(r[1])
        if from_id and to_id:
            cur.execute("""
                INSERT OR IGNORE INTO event_relations
                (from_event_id, to_event_id, relation_type, strength, time_lag_years)
                VALUES (?, ?, ?, ?, ?)
            """, (from_id, to_id, r[2], r[3], r[4]))

    conn.commit()

    # Report
    tables = ["usage_events", "adoption_paths", "event_relations"]
    print("\nDB2 seeded:")
    for t in tables:
        count = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {count} rows")

    # Quadrant distribution
    print("\nQuadrant distribution:")
    for row in cur.execute("""
        SELECT quadrant, COUNT(*) FROM usage_events GROUP BY quadrant ORDER BY quadrant
    """):
        print(f"  Quadrant {row[0]}: {row[1]} events")

    # Path type distribution
    print("\nAdoption path types:")
    for row in cur.execute("""
        SELECT adoption_path_type, COUNT(*) FROM usage_events
        WHERE adoption_path_type IS NOT NULL GROUP BY adoption_path_type
    """):
        print(f"  {row[0]}: {row[1]} events")

    conn.close()


if __name__ == '__main__':
    seed()
