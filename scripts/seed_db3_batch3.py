"""
Batch 3: DB3 robotics futures - underrepresented domains (arts, domestic, sensory, architecture).
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'robotics_futures.db')


def get_or_create_source(cur, title, authors, year, journal, doi=None,
                         venue_type='journal', source_type='academic_peer_reviewed',
                         peer_reviewed=1, credibility=0.85):
    row = cur.execute("SELECT id FROM sources WHERE title = ?", (title,)).fetchone()
    if row:
        return row[0]
    cur.execute("""
        INSERT INTO sources (title, authors, year, journal, doi, venue_type,
            source_type, peer_reviewed, credibility_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, authors, year, journal, doi, venue_type, source_type,
          peer_reviewed, credibility))
    return cur.lastrowid


def domain_id(cur, code):
    row = cur.execute("SELECT id FROM domains WHERE code = ?", (code,)).fetchone()
    return row[0] if row else None


def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()

    # Create all needed sources first
    src = {}
    src['dance_aesthetic'] = get_or_create_source(cur,
        "Dancing robots: aesthetic engagement shaped by stimulus and knowledge cues to human animacy",
        "Various", 2024, "PMC", None)
    src['dance_improv'] = get_or_create_source(cur,
        "A Constructed Response: Designing and Choreographing Robot Arm Movements in Collaborative Dance Improvisation",
        "Various", 2025, "arXiv", None, 'preprint', 'preprint', 0, 0.80)
    src['robot_music_sync'] = get_or_create_source(cur,
        "Integrating humanoid robots with human musicians for synchronized musical performances",
        "Various", 2025, "PMC", None)
    src['lovot_elderly'] = get_or_create_source(cur,
        "Improving the Social Well-Being of Single Older Adults Using the LOVOT Social Robot: Qualitative Study",
        "Various", 2024, "JMIR Human Factors", None)
    src['lovot_dementia'] = get_or_create_source(cur,
        "Use of a Social Robot (LOVOT) for Persons With Dementia: Exploratory Study",
        "Various", 2022, "PMC", None)
    src['moxie_child'] = get_or_create_source(cur,
        "Moxie: Social Robot for Childhood Social-Emotional Learning",
        "Various", 2024, "IEEE Spectrum", None, 'journal', 'academic_peer_reviewed', 1, 0.85)
    src['pet_compare'] = get_or_create_source(cur,
        "Real vs robotic pets comparative analysis: emotional bonding and comfort for isolated elderly",
        "Various", 2024, "Multiple journals", None)
    src['moley'] = get_or_create_source(cur,
        "Moley Robotic Kitchen: dexterous manipulation for aging in place",
        "Moley Robotics", 2024, "Industry reports", None, 'report', 'industry_report', 0, 0.75)
    src['sushi'] = get_or_create_source(cur,
        "Restaurant Robotics: sushi robots and food culture automation",
        "Aaron Allen & Associates", 2024, "Industry analysis", None,
        'report', 'industry_report', 0, 0.75)
    src['haptic_glove'] = get_or_create_source(cur,
        "Leveraging Tactile Sensing for Haptic Feedback and VR 3D Object Reconstruction in Robotic Telemanipulation",
        "Various", 2024, "arXiv", None, 'preprint', 'preprint', 0, 0.80)
    src['haptic_ring'] = get_or_create_source(cur,
        "Augmented tactile-perception and haptic-feedback rings as human-machine interfaces",
        "Various", 2022, "Nature Communications", "10.1038/s41467-022-32745-8")
    src['soft_touch'] = get_or_create_source(cur,
        "Affective touch soft robot (S-CAT) delivering CT-optimal slow-velocity strokes for stress relief",
        "Various", 2024, "Soft Robotics journals", None)
    src['sensory_blind'] = get_or_create_source(cur,
        "Wearable real-time tactile-vision substitution system: clinical validation for blind people",
        "Various", 2025, "Displays", None)
    src['ar_robot'] = get_or_create_source(cur,
        "Augmented reality and robotics integration: 460-paper review",
        "Various", 2024, "Multiple venues", None)
    src['3d_home'] = get_or_create_source(cur,
        "Toward automated construction: design-to-printing workflow for robotic in-situ 3D printed house",
        "Various", 2024, "Case Studies in Construction Materials", None)
    src['greenhouse'] = get_or_create_source(cur,
        "Robotic greenhouse systems: lettuce profit increase and worker relief",
        "Various", 2024, "Frontiers in Sustainable Food Systems", None)
    src['urban_garden'] = get_or_create_source(cur,
        "Adaptable technologies for robotic urban horticulture: review",
        "Various", 2025, "Frontiers in Sustainable Food Systems", None)
    src['vacuum_adv'] = get_or_create_source(cur,
        "Advanced robot vacuums with autonomous docking and self-maintenance: 2025 market review",
        "Various", 2025, "Consumer technology reviews", None,
        'report', 'industry_report', 0, 0.75)
    src['rammp'] = get_or_create_source(cur,
        "RAMMP: Robotic Assistive Mobility and Manipulation Platform combining wheelchair + robotic arm",
        "Northeastern University", 2025, "Northeastern News / research", None,
        'report', 'institutional_report', 0, 0.80)
    src['walkon'] = get_or_create_source(cur,
        "Soft robotic shorts (WalkON) reduce walking effort 20% in elderly",
        "Various", 2024, "Nature Machine Intelligence", "10.1038/s42256-024-00894-8")
    src['cultural_robot'] = get_or_create_source(cur,
        "Culturally adaptive robots detecting cultural communication cues for improved engagement",
        "Various", 2024, "HRI conferences", None, 'conference', 'conference_paper', 1, 0.85)
    src['smallholder'] = get_or_create_source(cur,
        "Robot-as-a-Service for smallholder farmers: accessibility and sustainability",
        "Various", 2025, "Multiple venues", None)
    src['social_catalyst'] = get_or_create_source(cur,
        "Social robots as conversational catalysts: Enhancing long-term human-human interaction at home",
        "Various", 2024, "Science Robotics", "10.1126/scirobotics.adk3307")
    src['dance_survey'] = get_or_create_source(cur,
        "Robots and Dance: A Promising Young Alchemy - survey of methods and future directions",
        "Various", 2025, "Annual Reviews / Frontiers", None)

    conn.commit()

    # Mentions
    mentions = [
        # Arts - Performance
        (src['dance_aesthetic'], 'arts_performance',
         "Robot dancers produce aesthetic engagement shaped by stimulus cues and knowledge of animacy. Audiences prefer computer-generated choreography when properly framed as intentional art",
         'creative_expression', '2024-2030', 2024, 2030, 'high',
         'aesthetic', 'positive', 4, 'mixed', 0, "Framing as art critical for acceptance", None, 'COHORT', 'STRONG'),

        (src['dance_improv'], 'arts_performance',
         "Collaborative dance improvisation between robot arms and human dancers produces novel artistic expressions through real-time motion response and embodied interaction",
         'creative_expression', '2025-2030', 2025, 2030, 'high',
         'aesthetic', 'positive', 3, 'conditional', 0, "Requires sophisticated motion planning", "Limited to structured environments", 'PROTOTYPE', 'MODERATE'),

        (src['dance_survey'], 'arts_performance',
         "Survey of robot dance research: emerging field combining robotics, choreography, and cognitive science. Robot-specific motion (non-anthropomorphic) opens new aesthetic possibilities",
         'creative_expression', '2025-2035', 2025, 2035, 'medium',
         'aesthetic', 'positive', 3, 'mixed', 0, "Non-anthropomorphic motion may be more interesting than human imitation", None, 'SURVEY', 'GROWING'),

        # Arts - Music
        (src['robot_music_sync'], 'arts_music',
         "Humanoid robots (Polaris, Oscar) achieve synchronized musical collaboration with real-time melodic generation. Head/arm gestures signal musical information to human performers",
         'creative_expression', '2025-2030', 2025, 2030, 'high',
         'aesthetic', 'positive', 4, 'conditional', 1, "Gesture-based synchronization key for musical timing", None, 'PROTOTYPE', 'MODERATE'),

        # Domestic - Companion (LOVOT)
        (src['lovot_elderly'], 'domestic_companion',
         "Single older adults using LOVOT report improved social well-being: home liveliness, forward-looking behavior, reduced loneliness through relational bonding with warm fuzzy robot",
         'emotional_companionship', '2024-2030', 2024, 2030, 'high',
         'relational', 'positive', 4, 'conditional', 0, "Requires active engagement", "Qualitative study; larger RCTs needed", 'CASE_STUDY', 'STRONG'),

        (src['lovot_dementia'], 'domestic_companion',
         "LOVOT for persons with dementia: documented improvements in communication and engagement. Warm tactile interaction particularly effective",
         'emotional_companionship', '2024-2030', 2024, 2030, 'high',
         'emotional', 'positive', 3, 'conditional', 0, "Dementia stage affects response", "Exploratory study", 'CASE_STUDY', 'MODERATE'),

        # Domestic - Companion (Moxie)
        (src['moxie_child'], 'domestic_companion',
         "Moxie robot for children shows significant RCT evidence for ASD spectrum improvements: emotion regulation, conversation skills, eye contact, social engagement (+4 magnitude)",
         'social_interaction', '2024-2030', 2024, 2030, 'high',
         'relational', 'positive', 4, 'positive', 2, "Designed specifically for childhood social-emotional learning", None, 'RCT', 'STRONG'),

        # Social - Emotion (Pet comparison)
        (src['pet_compare'], 'social_emotion',
         "Meta-analysis: real dogs superior in emotional bonding (anxiety reduction, blood pressure, survival rates). Robotic pets provide substantial comfort for isolated/disabled, inducing calmness while reducing sadness. Function as 'serious toys'",
         'emotional_companionship', '2024-2030', 2024, 2030, 'high',
         'emotional', 'positive', 3, 'mixed', 0, "Real pets superior but robots fill gap for those unable to care for animals", None, 'META_ANALYSIS', 'MODERATE'),

        # Social - Catalyst
        (src['social_catalyst'], 'social_emotion',
         "Social robots as conversational catalysts enhance long-term human-HUMAN interaction at home. Robots facilitate rather than replace human social bonds",
         'social_interaction', '2024-2030', 2024, 2030, 'high',
         'relational', 'positive', 4, 'positive', 1, "Robot catalyzes rather than substitutes human connection", None, 'RCT', 'STRONG'),

        # Domestic - Cooking
        (src['moley'], 'domestic_cooking',
         "Moley Robotic Kitchen enables aging in place through dexterous food preparation. Elderly gain cooking autonomy without caregiver dependency",
         'physical_manipulation', '2025-2035', 2025, 2035, 'medium',
         'autonomy', 'positive', 4, 'positive', 2, "High cost limits adoption", "Industry prototype, limited independent evaluation", 'PROTOTYPE', 'EMERGING'),

        (src['sushi'], 'domestic_cooking',
         "Sushi robot market exceeds $500M. CONTESTED consensus on food authenticity: efficiency vs cultural craftsmanship tension. Cultural dimension mixed",
         'physical_manipulation', '2024-2030', 2024, 2030, 'medium',
         'cultural', 'mixed', 2, 'positive', 3, "Efficiency vs authenticity tension unresolved", "Cultural acceptance varies greatly", 'SURVEY', 'CONTESTED'),

        # Domestic - Garden
        (src['greenhouse'], 'domestic_garden',
         "Robotic greenhouse systems increase lettuce profits 28%, cucumber yields 12% while relieving workers from physically demanding repetitive tasks",
         'environmental_adaptation', '2025-2030', 2025, 2030, 'high',
         'autonomy', 'positive', 3, 'positive', 3, "Commercial greenhouse context", None, 'CASE_STUDY', 'MODERATE'),

        (src['urban_garden'], 'domestic_garden',
         "Urban horticulture robots address city-dwellers' limited land and time constraints, supporting food security and bringing nature interaction to urban environments",
         'environmental_adaptation', '2025-2035', 2025, 2035, 'medium',
         'cultural', 'positive', 3, 'positive', 2, "Urban food security application", "Early stage development", 'PROTOTYPE', 'EMERGING'),

        # Domestic - Cleaning
        (src['vacuum_adv'], 'domestic_cleaning',
         "Advanced robot vacuums (2025) with autonomous docking, self-emptying, mop washing, detergent dispensing enable weeks without manual intervention. Substantially reduces burden for elderly/disabled households",
         'physical_manipulation', '2025-2030', 2025, 2030, 'high',
         'autonomy', 'positive', 3, 'positive', 2, "Mature consumer technology; high adoption rate", "QoL-specific research surprisingly thin", 'SURVEY', 'STRONG'),

        # Sensory augmentation
        (src['haptic_glove'], 'mobility_personal',
         "Haptic feedback gloves enable tactile-based teleoperation with precise 3D object reconstruction. Potential for remote sensory experience and manipulation",
         'sensory_augmentation', '2025-2032', 2025, 2032, 'high',
         'aesthetic', 'positive', 4, 'positive', 2, "Teleoperation + VR integration", None, 'PROTOTYPE', 'MODERATE'),

        (src['haptic_ring'], 'mobility_personal',
         "Wearable haptic rings provide multimodal tactile + temperature perception with vibro-haptic feedback. Nature Communications validated",
         'sensory_augmentation', '2024-2030', 2024, 2030, 'high',
         'aesthetic', 'positive', 3, 'positive', 2, "Compact wearable form factor", None, 'PROTOTYPE', 'MODERATE'),

        (src['soft_touch'], 'social_emotion',
         "Affective touch soft robot (S-CAT) delivers CT-optimal slow-velocity strokes producing measurable stress relief and pleasantness improvement in controlled studies",
         'emotional_companionship', '2025-2032', 2025, 2032, 'medium',
         'emotional', 'positive', 4, 'conditional', 0, "Slow gentle touch mimics human affective touch", "Early stage research", 'PROTOTYPE', 'EMERGING'),

        (src['sensory_blind'], 'mobility_personal',
         "Wearable tactile-vision substitution system clinically validated: significant improvement in spatial navigation and vision-related QoL for blind people",
         'sensory_augmentation', '2025-2030', 2025, 2030, 'high',
         'autonomy', 'positive', 5, 'positive', 1, "Clinical validation completed", None, 'COHORT', 'STRONG'),

        (src['ar_robot'], 'mobility_personal',
         "AR + robotics integration review (460 papers): AR headset visual augmentation significantly improves manipulation task performance through cognitive support overlay",
         'cognitive_support', '2025-2032', 2025, 2032, 'high',
         'autonomy', 'positive', 3, 'positive', 3, "Industrial and assistive applications", None, 'META_ANALYSIS', 'MODERATE'),

        # Architecture
        (src['3d_home'], 'arts_architecture',
         "3D printed homes achieve whole-house construction in <24 hours with reduced waste and mass customization. Regulatory momentum growing (Citizen Robotics Michigan 2023-2024)",
         'environmental_adaptation', '2025-2035', 2025, 2035, 'high',
         'autonomy', 'positive', 5, 'positive', 4, "Affordability and accessibility breakthrough", "Regulatory landscape still evolving", 'CASE_STUDY', 'STRONG'),

        # Mobility
        (src['rammp'], 'mobility_personal',
         "RAMMP prototype combines autonomous wheelchair with integrated robotic arm enabling activities of daily living independently. Revolutionary for severe mobility disability",
         'physical_manipulation', '2026-2032', 2026, 2032, 'high',
         'autonomy', 'positive', 5, 'positive', 2, "Combined mobility + manipulation in single platform", "12-month prototype; not yet commercialized", 'PROTOTYPE', 'EMERGING'),

        (src['walkon'], 'mobility_exo',
         "Soft robotic shorts (WalkON) reduce walking effort 20% in elderly. Only 1.6kg weight with improved wearability vs rigid exoskeletons",
         'physical_manipulation', '2024-2030', 2024, 2030, 'high',
         'autonomy', 'positive', 4, 'positive', 2, "Lightweight, practical for daily use", None, 'RCT', 'STRONG'),

        # Cultural
        (src['cultural_robot'], 'social_cultural',
         "Culturally adaptive robots detecting and responding to cultural communication cues improve engagement. Chinese users prefer implicit communication, Germans explicit",
         'social_interaction', '2025-2032', 2025, 2032, 'high',
         'cultural', 'positive', 3, 'positive', 1, "Cultural adaptation essential for global deployment", None, 'COHORT', 'STRONG'),

        # Agriculture
        (src['smallholder'], 'agriculture_sustainable',
         "Robot-as-a-Service (RaaS) model addresses smallholder farmers' high upfront cost barrier. Potential for chemical minimization, water optimization, GHG reduction",
         'environmental_adaptation', '2026-2035', 2026, 2035, 'medium',
         'cultural', 'positive', 2, 'positive', 3, "Digital infrastructure and farmer education prerequisite", "Speculative for developing countries", 'FORESIGHT', 'GROWING'),
    ]

    inserted = 0
    for m in mentions:
        qol_mag = m[10]
        econ_mag = m[12]
        quadrant = 'I' if qol_mag > 0 and econ_mag > 0 else 'II' if qol_mag > 0 else 'III' if econ_mag <= 0 else 'IV'
        cur.execute("""
            INSERT INTO mentions
            (source_id, domain_id, claim_summary, capability_type_code,
             timeline_projection, projected_year_start, projected_year_end,
             projection_confidence,
             qol_dimension, qol_impact_direction, qol_impact_magnitude,
             economic_impact_direction, economic_impact_magnitude,
             quadrant, conditions, limitations,
             evidence_type_code, consensus_level_code)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (m[0], domain_id(cur, m[1]), m[2], m[3], m[4], m[5], m[6], m[7],
              m[8], m[9], m[10], m[11], m[12],
              quadrant, m[13], m[14], m[15], m[16]))
        inserted += 1

    conn.commit()

    total = cur.execute("SELECT COUNT(*) FROM mentions").fetchone()[0]
    src_count = cur.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
    print(f"\nDB3 batch 3 complete. Inserted {inserted} mentions.")
    print(f"Total: {total} mentions, {src_count} sources")

    print("\nBy domain L2:")
    for r in cur.execute("""
        SELECT d.name, COUNT(m.id) FROM mentions m
        JOIN domains d ON m.domain_id = d.id
        GROUP BY d.name ORDER BY COUNT(m.id) DESC
    """):
        print(f"  {r[0]}: {r[1]}")

    print("\nBy QoL dimension:")
    for r in cur.execute("SELECT qol_dimension, COUNT(*) FROM mentions GROUP BY qol_dimension ORDER BY COUNT(*) DESC"):
        print(f"  {r[0]}: {r[1]}")

    conn.close()


if __name__ == '__main__':
    seed()
