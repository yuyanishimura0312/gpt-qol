"""
Seed DB3 with initial robotics futures evidence from research team findings.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'robotics_futures.db')


def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()

    # ============================================================
    # SOURCES
    # ============================================================
    sources = [
        ("Foundation models in robotics: Applications, challenges, and the future",
         "Roya Firoozi et al.", 2025, "International Journal of Robotics Research",
         "10.1177/02783649241281508", "journal", "academic_peer_reviewed", 1, 0.95),
        ("RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control",
         "Anthony Brohan et al.", 2023, "arXiv", "10.48550/arXiv.2307.15818",
         "preprint", "preprint", 0, 0.85),
        ("The effectiveness of PARO on behavioural and psychological symptoms in dementia: systematic review and meta-analysis",
         "Various", 2023, "International Journal of Nursing Studies", "10.1016/j.ijnurstu.2023.104503",
         "journal", "academic_peer_reviewed", 1, 0.90),
        ("Socially Assistive Robots for People Living with Dementia: A Systematic Review and Meta-Analysis of RCTs",
         "Various", 2024, "Gerontology (Karger)", None,
         "journal", "academic_peer_reviewed", 1, 0.90),
        ("Social robots for education: A review",
         "Tony Belpaeme et al.", 2018, "Science Robotics", "10.1126/scirobotics.aat5954",
         "journal", "academic_peer_reviewed", 1, 0.95),
        ("Social Robots: A Promising Tool to Support People with Autism",
         "Various", 2024, "Review Journal of Autism and Developmental Disorders",
         "10.1007/s40489-024-00434-5", "journal", "academic_peer_reviewed", 1, 0.90),
        ("Shaping high-performance wearable robots for human motor and sensory reconstruction and enhancement",
         "Various", 2024, "Nature Communications", "10.1038/s41467-024-46249-0",
         "journal", "academic_peer_reviewed", 1, 0.95),
        ("Food's future: sustainability and agricultural robotics",
         "Stavros Vougioukas et al.", 2025, "Frontiers in Robotics and AI",
         "10.3389/frobt.2025.1696483", "journal", "academic_peer_reviewed", 1, 0.85),
        ("Kantianism for the Ethics of Human-Robot Interaction",
         "Various", 2025, "Philosophy & Technology", "10.1007/s13347-025-00941-1",
         "journal", "academic_peer_reviewed", 1, 0.85),
        ("Animism, Rinri, Modernization; the Base of Japanese Robotics",
         "Various", 2023, "Montreal AI Ethics Institute", None,
         "report", "institutional_report", 0, 0.80),
        ("A Survey of Robotic Systems for Nursing Care",
         "Various", 2022, "Frontiers in Robotics and AI", None,
         "journal", "academic_peer_reviewed", 1, 0.85),
        ("Designing Sociable Robots",
         "Cynthia Breazeal", 2002, "MIT Press", None,
         "book", "book", 0, 0.90),
        ("Physical Human-Robot Interaction Safety Constraints",
         "Various", 2025, "arXiv", None,
         "preprint", "preprint", 0, 0.80),
        ("Functional Fibers and Fabrics for Soft Robotics, Wearables, and Human-Robot Interface",
         "Various", 2021, "Advanced Materials", "10.1002/adma.202002640",
         "journal", "academic_peer_reviewed", 1, 0.90),
    ]

    source_ids = {}
    for s in sources:
        cur.execute("""
            INSERT OR IGNORE INTO sources
            (title, authors, year, journal, doi, venue_type, source_type,
             peer_reviewed, credibility_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, s)
        row = cur.execute("SELECT id FROM sources WHERE title = ?", (s[0],)).fetchone()
        if row:
            source_ids[s[0]] = row[0]

    # Add placeholder sources for items without specific publications
    cur.execute("""
        INSERT OR IGNORE INTO sources (title, authors, year, journal, venue_type, source_type, peer_reviewed, credibility_score)
        VALUES ('Various conference and journal publications on creative robotics', 'Laviers, Cuan, Donnarumma, Gemeinboeck', 2023, 'Frontiers in Robotics and AI', 'journal', 'academic_peer_reviewed', 1, 0.80)
    """)
    source_ids["creative_robotics_placeholder"] = cur.lastrowid or cur.execute("SELECT id FROM sources WHERE title LIKE 'Various conference%'").fetchone()[0]

    cur.execute("""
        INSERT OR IGNORE INTO sources (title, authors, year, journal, venue_type, source_type, peer_reviewed, credibility_score)
        VALUES ('Uncanny Valley and LLM Integration Studies', 'Various', 2024, 'Multiple venues', 'journal', 'academic_peer_reviewed', 1, 0.80)
    """)
    source_ids["uncanny_valley_placeholder"] = cur.lastrowid or cur.execute("SELECT id FROM sources WHERE title LIKE 'Uncanny Valley%'").fetchone()[0]

    cur.execute("""
        INSERT OR IGNORE INTO sources (title, authors, year, journal, venue_type, source_type, peer_reviewed, credibility_score)
        VALUES ('Household chore automation predictions', 'Oxford University researchers', 2024, 'Various', 'report', 'institutional_report', 0, 0.75)
    """)
    source_ids["domestic_placeholder"] = cur.lastrowid or cur.execute("SELECT id FROM sources WHERE title LIKE 'Household chore%'").fetchone()[0]

    cur.execute("""
        INSERT OR IGNORE INTO sources (title, authors, year, journal, venue_type, source_type, peer_reviewed, credibility_score)
        VALUES ('OriHime Avatar Robot: Disability Inclusion through Telepresence', 'Ory Laboratory', 2021, 'Various', 'report', 'institutional_report', 0, 0.80)
    """)
    source_ids["orihime_placeholder"] = cur.lastrowid or cur.execute("SELECT id FROM sources WHERE title LIKE 'OriHime%'").fetchone()[0]

    cur.execute("""
        INSERT OR IGNORE INTO sources (title, authors, year, journal, venue_type, source_type, peer_reviewed, credibility_score)
        VALUES ('Woebot RCT and CBT Chatbot Meta-analysis', 'Various', 2023, 'JMIR Mental Health', 'journal', 'academic_peer_reviewed', 1, 0.85)
    """)
    source_ids["woebot_placeholder"] = cur.lastrowid or cur.execute("SELECT id FROM sources WHERE title LIKE 'Woebot%'").fetchone()[0]

    conn.commit()

    # ============================================================
    # MENTIONS (Evidence items)
    # ============================================================
    # Helper to get domain_id
    def domain_id(code):
        row = cur.execute("SELECT id FROM domains WHERE code = ?", (code,)).fetchone()
        return row[0] if row else None

    mentions = [
        # PARO therapeutic robot
        (source_ids.get("The effectiveness of PARO on behavioural and psychological symptoms in dementia: systematic review and meta-analysis"),
         domain_id("healthcare_companion"),
         "PARO intervention reduces antipsychotic medication use and improves anxiety, agitation, and depression in dementia patients with small-to-moderate effect sizes",
         "emotional_companionship", None, None, None, "medium",
         "emotional", "positive", 3, "positive", 1, None,
         "Small sample sizes and wide confidence intervals limit generalizability. Active user interest required for effectiveness",
         "Methodological limitations noted: need for larger RCTs",
         "META_ANALYSIS", "MODERATE"),

        # Social robots for dementia (SAR)
        (source_ids.get("Socially Assistive Robots for People Living with Dementia: A Systematic Review and Meta-Analysis of RCTs"),
         domain_id("healthcare_elderly"),
         "Socially assistive robots improve depression, anxiety, and social interaction in dementia patients but overall QoL improvement not yet statistically significant",
         "social_interaction", None, None, None, "medium",
         "relational", "positive", 2, "positive", 1, None,
         "Improvements in social interaction and positive emotional experience. Caregiver burden reduction",
         "Overall QoL improvement not statistically significant. Implementation barriers: weight, noise, cost",
         "META_ANALYSIS", "MODERATE"),

        # Education robots
        (source_ids.get("Social robots for education: A review"),
         domain_id("education_stem"),
         "Physical robot presence provides learning advantages over screen-based digital agents in STEM education, with NAO robot dominating education research",
         "social_interaction", None, None, None, "medium",
         "meaning", "positive", 3, "positive", 2, None,
         "Physical embodiment advantage strongest for STEM/coding. NAO and Pepper robots most studied",
         "Most studies focused on curriculum learning. Effect sizes small-to-moderate. Long-term effects unclear",
         "META_ANALYSIS", "STRONG"),

        # ASD therapy robots
        (source_ids.get("Social Robots: A Promising Tool to Support People with Autism"),
         domain_id("education_special"),
         "Children with ASD prefer interacting with robots over human therapists due to reduced sensory processing load. Statistically significant improvements in social communication and emotion recognition",
         "social_interaction", None, None, None, "medium",
         "relational", "positive", 4, "positive", 1, None,
         "KASPAR, QTrobot, NAO effective for joint attention, turn-taking, emotion recognition",
         "Long-term effect studies lacking. Skill generalization to daily life uncertain",
         "META_ANALYSIS", "STRONG"),

        # Foundation models in robotics
        (source_ids.get("Foundation models in robotics: Applications, challenges, and the future"),
         domain_id("healthcare_rehab"),
         "Foundation models (LLM, VLM, VLA) enable transfer learning across multiple robot application domains, potentially making robotics a true GPT. RT-2 doubled performance on unseen scenarios vs RT-1",
         "cognitive_support", "2025-2035", 2025, 2035, "medium",
         "multiple", "positive", 3, "positive", 4, None,
         "Data scarcity for robot training remains key bottleneck. Safety guarantees and uncertainty quantification needed",
         None,
         "META_ANALYSIS", "GROWING"),

        # Soft exosuits
        (source_ids.get("Shaping high-performance wearable robots for human motor and sensory reconstruction and enhancement"),
         domain_id("mobility_exo"),
         "Soft exosuits achieve 96.2% accuracy in predicting upper limb joint movements from EMG signals, enabling natural body-extension perception and rehabilitation for stroke, SCI, MS patients",
         "sensory_augmentation", "2024-2030", 2024, 2030, "high",
         "autonomy", "positive", 4, "positive", 3, None,
         "Textile-based actuators allow natural movement unlike rigid exoskeletons. Clinical applications for neurological conditions",
         None,
         "PROTOTYPE", "GROWING"),

        # Agricultural robotics
        (source_ids.get("Food's future: sustainability and agricultural robotics"),
         domain_id("agriculture_precision"),
         "Agricultural robots achieve 80% reduction in chemical use through precision application. SwarmFarm deployed 135+ robots across 6M+ acres for planting, spraying, weeding, mowing",
         "environmental_adaptation", "2025-2035", 2025, 2035, "medium",
         "cultural", "positive", 2, "positive", 3, None,
         "Harvest robots may replace up to 50% of labor force. Occlusion (30% fruit not visible) remains technical bottleneck",
         "High deployment costs. Labor displacement concerns",
         "CASE_STUDY", "MODERATE"),

        # Japanese cultural attitudes toward robots
        (source_ids.get("Animism, Rinri, Modernization; the Base of Japanese Robotics"),
         domain_id("social_cultural"),
         "Japanese Shinto animism (all objects possess anima/spirit) and ethics of relational harmony (rinri) provide cultural foundation for higher robot acceptance compared to Western 'robot threat' narratives. Tsukumogami tradition enables robot monks and care companions",
         "social_interaction", None, None, None, "medium",
         "cultural", "positive", 3, "conditional", 0, None,
         "Cultural attitudes significantly mediate robot acceptance. Western deployment must account for cultural resistance",
         "Anthropological analysis, not empirical measurement",
         "THEORETICAL", "MODERATE"),

        # Nursing care robots
        (source_ids.get("A Survey of Robotic Systems for Nursing Care"),
         domain_id("healthcare_elderly"),
         "Nursing care robots provide patient monitoring, personalized rehabilitation, and daily living support. Key to maintaining mobility and object manipulation independence in elderly",
         "physical_manipulation", "2025-2035", 2025, 2035, "medium",
         "autonomy", "positive", 3, "positive", 2, None,
         "Robots learn user preferences and routines for individualized care. Reduces caregiver burden while maintaining care recipient autonomy",
         "Field deployment challenges: one robot ('Hug') abandoned after days due to operational burden of moving between rooms",
         "SURVEY", "MODERATE"),

        # Creative robotics
        (source_ids.get("creative_robotics_placeholder"), domain_id("arts_performance"),
         "Robot dancers, musicians, and performers redefine creativity as collaborative practice between humans and machines, not individual human capacity. Researchers: Laviers, Cuan, Donnarumma, Gemeinboeck",
         "creative_expression", "2020-2030", 2020, 2030, "low",
         "aesthetic", "positive", 4, "positive", 1, None,
         "Creativity exists 'in the interaction between' human and robot, not in either alone",
         "Early-stage research. Artistic quality assessment subjective",
         "CASE_STUDY", "EMERGING"),

        # Textile/fiber soft robotics
        (source_ids.get("Functional Fibers and Fabrics for Soft Robotics, Wearables, and Human-Robot Interface"),
         domain_id("mobility_exo"),
         "Fiber/yarn actuators can be sewn and woven using mature textile engineering, enabling rehabilitation, human motion assist, and power amplification through clothing-like interfaces with high skin affinity",
         "sensory_augmentation", "2025-2035", 2025, 2035, "medium",
         "autonomy", "positive", 3, "positive", 2, None,
         "Knitted strain sensors for stroke patient limb motion monitoring. Safe interaction platform with high skin compatibility",
         None,
         "PROTOTYPE", "EMERGING"),

        # Robot ethics - Kantian framework
        (source_ids.get("Kantianism for the Ethics of Human-Robot Interaction"),
         domain_id("social_ethics"),
         "Kantian ethics for HRI proposes duties not to the robot itself but to maintain human moral character and protect human-robot relationships. Current robots lack clear moral status but future strong AI may change this",
         "social_interaction", None, None, None, "low",
         "meaning", "conditional", 0, "conditional", 0, None,
         "Ethical frameworks still developing. Current robots have no moral status",
         "Philosophical analysis without empirical validation",
         "THEORETICAL", "EMERGING"),

        # MIT sociable robots
        (source_ids.get("Designing Sociable Robots"),
         domain_id("social_emotion"),
         "Richer social embodiment strengthens trust, emotional bonding, and companionship perception toward AI personas. Huggable for pediatric patients, Tega for child language development",
         "emotional_companionship", "2020-2030", 2020, 2030, "medium",
         "emotional", "positive", 3, "positive", 1, None,
         "Long-term human interaction supports growth. Physical presence more effective than screen-based agents",
         "Lab-based studies; real-world longitudinal data limited",
         "PROTOTYPE", "MODERATE"),

        # Uncanny valley and LLM integration
        (source_ids.get("uncanny_valley_placeholder"), domain_id("social_hri"),
         "LLM integration reduces uncanny valley effect by enabling more natural conversation. Repeated friendly interaction produces affective habituation that reduces perceived eeriness. Neural basis: amygdala and prefrontal cortex activation during uncanny valley perception",
         "social_interaction", "2024-2030", 2024, 2030, "medium",
         "emotional", "positive", 2, "positive", 1, None,
         "EEG and eye-tracking evidence for neural mechanisms. Conversational ability key factor in acceptance",
         "Cross-cultural variation in uncanny valley perception not fully mapped",
         "RCT", "GROWING"),

        # Domestic service robots - Oxford prediction
        (source_ids.get("domestic_placeholder"), domain_id("domestic_cleaning"),
         "Oxford University predicts 40% of household chores (cleaning, cooking, laundry) automatable within 10 years. Current: vacuum robots, lawn mowers, smart speakers. Next generation: multi-function adaptive home robots",
         "physical_manipulation", "2025-2035", 2025, 2035, "low",
         "autonomy", "positive", 2, "positive", 2, None,
         "Progressive automation of household tasks",
         "Prediction, not demonstrated. Cost and reliability barriers remain",
         "EXPERT_OPINION", "EMERGING"),

        # OriHime avatar robot for disability inclusion
        (source_ids.get("orihime_placeholder"), domain_id("social_hri"),
         "OriHime avatar robot enables people with severe physical disabilities (ALS, MS) to work as cafe servers remotely via smartphone. Tokyo cafe employs 60+ disabled workers. Customers report authentic human connection through robot intermediary",
         "social_interaction", "2021-2030", 2021, 2030, "medium",
         "relational", "positive", 4, "positive", 2, None,
         "Robot as 'facilitator of inclusion and genuine beautiful connection'. Meaningful employment for severely disabled",
         "Single implementation case. Scalability unclear",
         "CASE_STUDY", "EMERGING"),

        # Mental health chatbots (Woebot)
        (source_ids.get("woebot_placeholder"), domain_id("healthcare_mental"),
         "CBT-based chatbot (Woebot) shows statistically significant reduction in depression and anxiety symptoms vs WHO self-help materials in 2-week RCT. Meta-analysis (18 RCTs, n~3500): effect size g=-0.25 to -0.33",
         "cognitive_support", "2023-2030", 2023, 2030, "high",
         "emotional", "positive", 3, "positive", 2, None,
         "Accessible, scalable mental health support",
         "Chatbot, not physical robot. Long-term efficacy data limited",
         "META_ANALYSIS", "MODERATE"),
    ]

    for i, m in enumerate(mentions):
        try:
            cur.execute("""
                INSERT INTO mentions
            (source_id, domain_id, claim_summary, capability_type_code,
             timeline_projection, projected_year_start, projected_year_end,
             projection_confidence,
             qol_dimension, qol_impact_direction, qol_impact_magnitude,
             economic_impact_direction, economic_impact_magnitude,
             quadrant,
             conditions, limitations,
             evidence_type_code, consensus_level_code)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7],
              m[8], m[9], m[10], m[11], m[12],
              # Compute quadrant
              'I' if m[10] and m[10] > 0 and m[12] and m[12] > 0 else
              'II' if m[10] and m[10] > 0 and (m[12] is None or m[12] <= 0) else
              'III' if (m[10] is None or m[10] <= 0) and (m[12] is None or m[12] <= 0) else 'IV',
              m[14], m[15], m[16], m[17]))
        except Exception as e:
            print(f"Failed on mention {i}: {e}")
            print(f"  source_id={m[0]}, domain_id={m[1]}, capability={m[3]}")
            print(f"  evidence_type={m[15]}, consensus={m[16]}")
            raise

    conn.commit()

    # Report
    print("DB3 seeded:")
    for t in ["sources", "mentions"]:
        count = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {count} rows")

    print("\nBy domain L1:")
    for row in cur.execute("""
        SELECT d.name, COUNT(m.id) FROM mentions m
        JOIN domains d ON m.domain_id = d.id OR m.domain_id IN
            (SELECT id FROM domains WHERE parent_id = d.id)
        WHERE d.level = 1
        GROUP BY d.name ORDER BY COUNT(m.id) DESC
    """):
        print(f"  {row[0]}: {row[1]}")

    print("\nBy QoL dimension:")
    for row in cur.execute("""
        SELECT qol_dimension, COUNT(*) FROM mentions
        GROUP BY qol_dimension ORDER BY COUNT(*) DESC
    """):
        print(f"  {row[0]}: {row[1]}")

    print("\nBy consensus level:")
    for row in cur.execute("""
        SELECT consensus_level_code, COUNT(*) FROM mentions
        GROUP BY consensus_level_code ORDER BY COUNT(*) DESC
    """):
        print(f"  {row[0]}: {row[1]}")

    conn.close()


if __name__ == '__main__':
    seed()
