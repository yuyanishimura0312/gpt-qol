"""
Batch 2: DB1 tech×QoL empirical evidence from research agent.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'qol_sensibility.db')


def get_or_create_source(cur, title, authors, year, journal, doi=None,
                         source_type='academic_peer_reviewed', peer_reviewed=1, credibility=0.85):
    row = cur.execute("SELECT id FROM sources WHERE title = ?", (title,)).fetchone()
    if row:
        return row[0]
    cur.execute("""
        INSERT INTO sources (title, authors, year, journal, doi,
            source_type, peer_reviewed, credibility_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, authors, year, journal, doi, source_type, peer_reviewed, credibility))
    return cur.lastrowid


def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()

    # Evidence items: (source_title, authors, year, journal, doi,
    #                  technology, qol_dimension, effect_direction, claim,
    #                  methodology, sample_size, cultural_context, conditions, limitations)
    evidence = [
        # Social media
        ("Effects of social media restriction: Meta-analytic evidence from RCTs",
         "Haidt et al.", 2024, "Nature Human Behaviour", None,
         "Social Media", "emotional", "positive",
         "Restricting social media to 10 min/day significantly improves subjective well-being (g=0.17). Meta-analysis of 32 RCTs, 5544 individuals",
         "Meta-analysis of 32 RCTs", 5544, "Western, 70% female, avg age 23",
         "10-min restriction protocol", "Primarily college students"),

        ("Social media detox and well-being: Meta-analysis of RCTs",
         "Stevic & Liu", 2025, "MDPI Behavioral Sciences", None,
         "Social Media", "emotional", "positive",
         "Social media detox produces positive effects on life satisfaction, positive affect, and reduces depression and anxiety",
         "Meta-analysis of RCTs", None, "Global",
         "Detox interventions", None),

        ("Active and passive social media use and mental health: Meta-analysis of 141 studies",
         "Valkenburg & van Driel", 2024, "Journal of Computer-Mediated Communication", None,
         "Social Media", "relational", "conditional",
         "Active social media use correlates with greater well-being; passive use shows mixed associations varying by context",
         "Meta-analysis of 141 studies", 145000, "Multiple countries",
         "Active vs passive use distinction critical", None),

        ("Social media use and well-being: Systematic review",
         "Ansari et al.", 2024, "Cyberpsychology, Behavior, and Social Networking", None,
         "Social Media", "emotional", "negative",
         "Problematic social media use negatively correlates with subjective and psychological well-being (51 studies, 680K individuals)",
         "Systematic review and meta-analysis", 680506, "Global",
         "Problematic vs normal use distinction", None),

        # Smartphone
        ("Mere presence of smartphone reduces attentional performance",
         "Various", 2023, "Scientific Reports", None,
         "Smartphone", "autonomy", "negative",
         "Mere presence of smartphone reduces basal attentional performance and diverts cognitive resources even when silent",
         "Experimental", None, "University samples",
         None, None),

        ("Smartphone use and anxiety/depression in adolescents",
         "Various", 2023, "Multiple longitudinal studies", None,
         "Smartphone", "emotional", "negative",
         "Higher smartphone use associated with more frequent anxiety, depression symptoms, and sleep complaints in adolescents",
         "Longitudinal", None, "Adolescents, Western countries",
         None, None),

        # Television
        ("Bowling Alone: The Collapse and Revival of American Community",
         "Robert Putnam", 2000, "Simon & Schuster", None,
         "Television", "relational", "negative",
         "Television accounts for 25% of post-1965 decline in civic participation and social capital",
         "Time-use analysis and social capital surveys", None, "United States",
         None, "Causal attribution debated"),

        ("Television use and sleep in early childhood",
         "Various", 2019, "Sleep Health Journal", None,
         "Television", "emotional", "negative",
         "Children watching more TV display significantly shorter sleep duration; TV in bedrooms substantially reduces nighttime sleep. 76% of 42 studies found adverse outcomes",
         "Meta-analysis of 42 studies", 470, "Preschool-age children, Western",
         "TV in bedrooms worst effect", None),

        # Music technology
        ("Music streaming and emotion regulation",
         "Various", 2024, "Frontiers in Music & Psychology", None,
         "Music Streaming", "emotional", "positive",
         "Music listening through streaming platforms evokes positive emotions, changes affective state, and enhances emotional well-being through purposeful engagement",
         "Longitudinal, experience sampling", None, "International",
         "Purposeful engagement key", None),

        ("Live vs recorded music emotional response",
         "Various", 2024, "Scientific Reports", None,
         "Recorded Music", "aesthetic", "conditional",
         "Live music elicits significantly higher amygdala activation than recorded. Recorded music participants report less appreciation, lower arousal and valence",
         "fMRI neuroimaging + behavioral", 100, "Concert audiences, Western",
         "Live > recorded for emotional impact", None),

        # Video games
        ("A motivational model of video game engagement",
         "Przybylski et al.", 2010, "Review of General Psychology", None,
         "Video Games", "meaning", "positive",
         "Flow experiences in video games enhance engagement, well-being, and social interaction. Challenging educational games create flow linked with improved learning",
         "Experimental and cross-sectional", None, "Students and adult gamers",
         "Flow state requires skill-challenge balance", None),

        ("Exergaming physical activity and social well-being",
         "Various", 2024, "Systematic reviews", None,
         "Exergames", "relational", "positive",
         "Exergames increase physical activity 300% above resting. Promising effects for reduced loneliness, increased social connection, positive attitudes, subjective happiness",
         "Meta-analysis and RCTs (27 studies, 10 RCTs)", None, "Older adults",
         None, None),

        ("Esports stress and mental health",
         "Various", 2024, "Review of Sport and Exercise Psychology", None,
         "Competitive Gaming", "emotional", "negative",
         "Esports players report anxiety (38-82%) and depression (25-37%). High playtime correlates with poor psychological well-being",
         "Systematic review", None, "Global esports communities",
         "Professional/competitive context", None),

        # VR
        ("VR for awe and well-being",
         "Various", 2025, "Frontiers in Psychology", None,
         "Virtual Reality", "aesthetic", "positive",
         "VR experiences successfully elicit awe producing social interconnectivity, increased life satisfaction, improved mental and physical well-being even after brief exposure",
         "Experimental", 100, "Western countries",
         None, None),

        ("Immersive VR and quality of life in older adults",
         "Various", 2026, "JMIR Aging", None,
         "Virtual Reality", "meaning", "positive",
         "IVR interventions of 4+ weeks moderately improve quality of life in older adults, particularly those with clinical vulnerabilities or in institutional settings",
         "Systematic review and meta-analysis", None, "Older adults 65+",
         "4+ weeks duration needed", None),

        # Lighting
        ("Electric lighting and circadian rhythm disruption",
         "Various", 2024, "PMC reviews", None,
         "Electric Lighting", "emotional", "negative",
         "Evening artificial light suppresses melatonin by up to 50% in nearly half of homes, altering circadian rhythms. Morning light exposure improves sleep and reduces depression",
         "Actigraphy, longitudinal, RCTs", None, "Global",
         "Evening negative / morning positive", None),

        ("Outdoor light exposure and depression: UK Biobank",
         "Various", 2022, "PMC", None,
         "Natural Lighting", "emotional", "positive",
         "Greater daytime outdoor light associated with fewer depressive symptoms, lower antidepressant use, easier waking, less tiredness. N=400,000+",
         "Large longitudinal cohort", 400000, "United Kingdom",
         None, None),

        # Mindfulness apps
        ("Meditation apps effects: Meta-analysis of 34 RCTs",
         "Various", 2025, "Multiple journals", None,
         "Meditation Apps", "emotional", "positive",
         "Meditation apps show significant effects on stress (g=0.46), anxiety (g=0.28), depression (g=0.33). 68% of RCTs reported significant well-being improvements",
         "Meta-analysis of 34 RCTs", 7566, "Global",
         None, None),

        # Dating apps
        ("Dating apps and psychological well-being: Systematic review",
         "Various", 2025, "Cyberpsychology", None,
         "Dating Apps", "relational", "negative",
         "Dating app users report significantly worse psychological health (depression, anxiety, loneliness, distress) vs non-users. 85% of studies found negative body image impact",
         "Meta-analysis and systematic review", None, "Western countries",
         "Motivation-dependent effects", None),

        # AI chatbots
        ("AI chatbots for mental health: Meta-analysis",
         "Various", 2023, "npj Digital Medicine", None,
         "AI Chatbot", "emotional", "positive",
         "AI conversational agents significantly reduce depression (g=0.64) and distress (g=0.7). Effects commence at 4 weeks and intensify at 8 weeks. 15 RCTs",
         "Meta-analysis of 15 RCTs", 7834, "Multiple countries",
         "4-8 weeks for therapeutic effect", None),

        ("Therabot RCT: Depression reduction",
         "Dartmouth researchers", 2025, "Dartmouth / peer-reviewed", None,
         "AI Therapy Chatbot", "emotional", "positive",
         "People with diagnosed depression using Therabot experienced 51% average reduction in symptoms after 8 weeks",
         "RCT", None, "USA, adults with depression",
         None, "First large therapy chatbot trial"),

        # Audiobooks
        ("Audiobooks emotional response vs TV/film",
         "UCL researchers", 2024, "University College London", None,
         "Audiobooks", "aesthetic", "positive",
         "Audiobooks produce stronger emotional and physiological responses (heart rate, body temperature) than TV or film with 99% certainty",
         "Experimental comparison", 100, "General population, Western",
         None, None),

        # Email/workplace
        ("Email overload and workplace well-being",
         "Various", 2024, "Frontiers in Psychology", None,
         "Email", "autonomy", "negative",
         "High email load impairs well-being. 76% of workers report information overload contributes to daily stress. Email disrupts workflow and goal regulation",
         "Cross-sectional and longitudinal", None, "Global workforce",
         None, None),

        # Bicycle
        ("Bicycles and women's liberation",
         "Historical scholarship / National Women's History Museum", 1890, "Historical analysis", None,
         "Bicycle", "autonomy", "positive",
         "Bicycles revolutionized women's liberation enabling independent movement. Susan B. Anthony: 'It has done more to emancipate women than anything else in the world'",
         "Historical documentation", None, "USA/Europe, 1890s-1920s",
         None, "Historical, not controlled study"),

        # Community radio
        ("Community radio and social capital",
         "Van Vuuren, K.", 2002, "Media International Australia", None,
         "Community Radio", "relational", "positive",
         "Community radio stations build social capital. More successful stations have heterogeneous volunteers diverse in background, age, gender",
         "Case study", None, "Non-metropolitan Australia",
         None, None),

        # Video conferencing
        ("Video calling and loneliness during pandemic",
         "Various", 2023, "Multiple studies", None,
         "Video Conferencing", "relational", "conditional",
         "Voice calls and text more effective at reducing loneliness than video calls in general. But video calls reduce loneliness in hearing-impaired elderly with dose-dependent effects",
         "Cross-sectional and longitudinal", None, "General population and older adults",
         "Modality-dependent", "Pandemic context"),

        # Air conditioning
        ("Personal comfort systems and thermal well-being",
         "Various", 2024, "Building and Environment", None,
         "Air Conditioning", "autonomy", "positive",
         "Personal comfort systems allowing occupant thermal regulation substantially decrease heat-related discomfort and enhance well-being, boosting pleasure and arousal",
         "Experimental", None, "Office environments, multiple climates",
         None, None),

        # Phonograph
        ("Phonograph and music democratization",
         "Historical analyses", 1900, "Smithsonian / music history", None,
         "Phonograph", "aesthetic", "positive",
         "Phonograph enabled on-demand music access, democratizing consumption. Shifted music from group to solitary experience. Created new forms of personal leisure",
         "Historical analysis", None, "USA, early 1900s-1950s",
         None, "Historical, not empirical"),

        # Binge-watching
        ("Binge-watching and sleep/quality of life",
         "Various", 2023, "Journal of Clinical Sleep Medicine", None,
         "Streaming Video", "emotional", "negative",
         "88% of US adults lose sleep to binge-watching. Linked with poorer sleep, more fatigue, insomnia symptoms, and pre-sleep cognitive arousal",
         "Survey (national) and longitudinal", None, "USA, young adults",
         "Problematic use vs normal viewing", None),

        # News
        ("Television news and anxiety",
         "Various", 2024, "JMIR Mental Health", None,
         "Television News", "emotional", "negative",
         "Increased news viewing frequency associated with anxiety, uncontrolled fear, hyperarousal, sleeping difficulties. Brief exposure increases state anxiety and negative mood",
         "Experimental and longitudinal", None, "News consumers globally",
         None, "Returns to baseline with relaxation"),

        # Fitness trackers
        ("Wearable activity trackers and motivation",
         "Various", 2023, "JMIR", None,
         "Fitness Tracker", "autonomy", "positive",
         "Wearable fitness trackers serve as behavioral nudges increasing self-awareness and motivation. Effective for those not meeting activity guidelines",
         "RCTs with 12-month follow-up", None, "Older adults, community samples",
         "Moderated by mindset about activity adequacy", None),

        # Podcasts
        ("Narrative podcasts and empathy",
         "Various", 2023, "PMC medical education", None,
         "Podcasts", "emotional", "positive",
         "96.2% of medical students agreed narrative podcasts increased empathy and reduced stigma. Audio storytelling uniquely impacts memory and emotions",
         "Qualitative and quantitative", None, "Medical students",
         None, None),

        # Digital tech meta
        ("Psychological effects of digital technology: Meta-analysis",
         "Various", 2025, "Frontiers in Psychology", None,
         "Digital Technology (general)", "emotional", "mixed",
         "Psychological well-being strongest positive association with AI, remote work, smart tourism (r=0.435). Burnout strongest negative (r=-0.478). 47 papers, 36100 adults",
         "Meta-analysis of 47 papers", 36100, "Global adults",
         "Technology type matters more than overall digital exposure", None),
    ]

    inserted = 0
    for e in evidence:
        src_id = get_or_create_source(cur, e[0], e[1], e[2], e[3], e[4])
        cur.execute("""
            INSERT OR IGNORE INTO tech_qol_evidence
            (source_id, technology_type, qol_dimension, effect_direction,
             claim_summary, methodology, sample_size, cultural_context,
             conditions, limitations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (src_id, e[5], e[6], e[7], e[8], e[9], e[10], e[11], e[12], e[13]))
        inserted += 1

    conn.commit()

    # Report
    total_evidence = cur.execute("SELECT COUNT(*) FROM tech_qol_evidence").fetchone()[0]
    total_sources = cur.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
    print(f"\nDB1 evidence batch complete. Inserted {inserted} items.")
    print(f"Total: {total_evidence} evidence items, {total_sources} sources")

    print("\nBy technology:")
    for r in cur.execute("""
        SELECT technology_type, COUNT(*) FROM tech_qol_evidence
        GROUP BY technology_type ORDER BY COUNT(*) DESC
    """):
        print(f"  {r[0]}: {r[1]}")

    print("\nBy QoL dimension:")
    for r in cur.execute("""
        SELECT qol_dimension, COUNT(*) FROM tech_qol_evidence
        GROUP BY qol_dimension ORDER BY COUNT(*) DESC
    """):
        print(f"  {r[0]}: {r[1]}")

    print("\nBy effect direction:")
    for r in cur.execute("""
        SELECT effect_direction, COUNT(*) FROM tech_qol_evidence
        GROUP BY effect_direction ORDER BY COUNT(*) DESC
    """):
        print(f"  {r[0]}: {r[1]}")

    conn.close()


if __name__ == '__main__':
    seed()
