"""
Batch 2: Additional DB3 robotics futures evidence from research agent.
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


def compute_quadrant(qol_mag, econ_mag):
    qol = qol_mag or 0
    econ = econ_mag or 0
    if qol > 0 and econ > 0:
        return 'I'
    elif qol > 0 and econ <= 0:
        return 'II'
    elif qol <= 0 and econ <= 0:
        return 'III'
    else:
        return 'IV'


def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()

    # Create sources for new evidence
    sources = {
        'paro_cognitive': get_or_create_source(cur,
            "PARO intervention for cognitive function improvement in elderly with cognitive decline",
            "Multiple RCT authors", 2023, "Various geriatrics journals", None,
            'journal', 'academic_peer_reviewed', 1, 0.90),
        'pepper_caresses': get_or_create_source(cur,
            "CARESSES: Culture-Aware Robots and Environmental Sensor Systems for Elderly Support",
            "CARESSES project consortium", 2023, "EU/Japan collaborative research", None,
            'report', 'institutional_report', 0, 0.85),
        'toyota_hsr': get_or_create_source(cur,
            "Toyota Human Support Robot: Compact Mobile Robot for Independent Living",
            "Toyota Motor Corporation", 2024, "Toyota Research Reports", None,
            'report', 'industry_report', 0, 0.80),
        'ragt_meta': get_or_create_source(cur,
            "Robot-assisted gait training combined with conventional rehabilitation for stroke: systematic review and meta-analysis",
            "Various", 2024, "Journal of NeuroEngineering and Rehabilitation",
            "10.1186/s12984-025-01649-1", 'journal', 'academic_peer_reviewed', 1, 0.90),
        'exo_sci': get_or_create_source(cur,
            "Exoskeleton training for spinal cord injury: RCT and meta-analysis of 12 studies",
            "Various", 2023, "Journal of NeuroEngineering and Rehabilitation",
            "10.1186/s12984-023-01158-z", 'journal', 'academic_peer_reviewed', 1, 0.90),
        'asd_efficacy': get_or_create_source(cur,
            "Robot-assisted therapy for autism: efficacy trial with 69 children",
            "Various", 2024, "Science Robotics", "10.1126/scirobotics.adl2266",
            'journal', 'academic_peer_reviewed', 1, 0.95),
        'asd_gaze': get_or_create_source(cur,
            "Eye-gaze analysis and joint attention in robot-assisted autism therapy",
            "Various", 2025, "AI intervention reviews", None,
            'journal', 'academic_peer_reviewed', 1, 0.85),
        'music_therapy_robot': get_or_create_source(cur,
            "Music-therapy robotic platform for children with autism: pilot study",
            "Various", 2024, "Frontiers in Robotics and AI", None,
            'journal', 'academic_peer_reviewed', 1, 0.80),
        'language_robot': get_or_create_source(cur,
            "ASR-equipped robot language learning: systematic review comparing robot vs human tutors",
            "Various", 2025, "Systematic literature review", None,
            'journal', 'academic_peer_reviewed', 1, 0.80),
        'surgery_qol': get_or_create_source(cur,
            "Robot-assisted surgery patient satisfaction and recovery quality",
            "Various", 2024, "Surgical outcomes journals", None,
            'journal', 'academic_peer_reviewed', 1, 0.85),
        'exo_accept': get_or_create_source(cur,
            "Acceptability of robotic exoskeletons by spinal cord injury patients: multicenter qualitative study",
            "Various", 2024, "Rehabilitation journals", None,
            'journal', 'academic_peer_reviewed', 1, 0.85),
        'phantom_pain': get_or_create_source(cur,
            "Peripheral nerve stimulation for phantom limb pain relief and prosthetic sensory feedback",
            "Various", 2024, "Neurorehabilitation journals", None,
            'journal', 'academic_peer_reviewed', 1, 0.85),
        'haptic_grasp': get_or_create_source(cur,
            "Vibrotactile haptic feedback for prosthetic grasping: experimental evaluation",
            "Various", 2024, "IEEE sensors and robotics", None,
            'journal', 'academic_peer_reviewed', 1, 0.85),
        'supernumerary': get_or_create_source(cur,
            "Robogami third arm for daily task assistance",
            "MIT d'Arbeloff Lab", 2024, "Science Robotics",
            "10.1126/scirobotics.adh1438", 'journal', 'academic_peer_reviewed', 1, 0.90),
        'elderly_loneliness': get_or_create_source(cur,
            "Digital social robot BOCCO emo for loneliness reduction in elderly: RCT",
            "Various", 2025, "JMIR Aging", "10.2196/74422",
            'journal', 'academic_peer_reviewed', 1, 0.90),
        'shimon_music': get_or_create_source(cur,
            "Shimon robot musician: deep learning for human-robot musical performance",
            "Gil Weinberg et al.", 2021, "Nature Communications / GTCMT", None,
            'journal', 'academic_peer_reviewed', 1, 0.85),
        'ethics_dependency': get_or_create_source(cur,
            "Ethical implications of companion robots: dependency, social isolation, and emotional attachment",
            "Various", 2025, "Frontiers in Robotics and AI",
            "10.3389/frobt.2025.1560214", 'journal', 'academic_peer_reviewed', 1, 0.85),
        'staff_burden': get_or_create_source(cur,
            "Care robot implementation: staff perspective on burden increase",
            "Various", 2024, "Nursing home staff systematic review", None,
            'journal', 'academic_peer_reviewed', 1, 0.80),
        'microsurgery': get_or_create_source(cur,
            "Robot-assisted microsurgery: tremor correction and precision with deep learning",
            "Various", 2024, "Science Robotics", "10.1126/scirobotics.adt0187",
            'journal', 'academic_peer_reviewed', 1, 0.90),
        'education_meta': get_or_create_source(cur,
            "Global effects of robot-based education: systematic review and meta-analysis",
            "Various", 2025, "Nature Communications",
            "10.1038/s41599-025-05546-9", 'journal', 'academic_peer_reviewed', 1, 0.95),
        'inclusion_edu': get_or_create_source(cur,
            "Educational robotics for social inclusion of vulnerable youth",
            "Various", 2025, "Frontiers in Robotics and AI",
            "10.3389/frobt.2025.1662945", 'journal', 'academic_peer_reviewed', 1, 0.85),
        'agri_precision': get_or_create_source(cur,
            "Precision farming robotics: water reduction and chemical-free weeding",
            "Various", 2025, "Agricultural robotics journals", None,
            'journal', 'academic_peer_reviewed', 1, 0.85),
        'kismet': get_or_create_source(cur,
            "Emotion and sociable humanoid robots",
            "Cynthia Breazeal", 2003, "International Journal of Human-Computer Studies", None,
            'journal', 'academic_peer_reviewed', 1, 0.90),
        'visual_nav': get_or_create_source(cur,
            "Visual Impairment Spatial Awareness system for indoor navigation",
            "Various", 2025, "PMC / CHI conference", None,
            'conference', 'conference_paper', 1, 0.85),
        'elderly_care_review': get_or_create_source(cur,
            "Care robots for vulnerable elderly: effectiveness and usability systematic review",
            "Various", 2025, "Sage Journals",
            "10.1177/20552076251370058", 'journal', 'academic_peer_reviewed', 1, 0.90),
        'taiwan_paro': get_or_create_source(cur,
            "Robot intervention for depression, loneliness and QoL in Taiwanese elderly care",
            "Various", 2024, "International Psychogeriatrics", None,
            'journal', 'academic_peer_reviewed', 1, 0.85),
        'japan_culture': get_or_create_source(cur,
            "Engineering robots with heart in Japan: cultural analysis",
            "Various", 2023, "Oxford Academic",
            "10.1093/oso/9780197631577.003.0034", 'book', 'book', 0, 0.85),
        'indigenous': get_or_create_source(cur,
            "Indigenous knowledge and pattern thinking in robotics workshops",
            "Various", 2024, "FCJ-209 / Academia.edu", None,
            'journal', 'academic_peer_reviewed', 1, 0.75),
        'haria': get_or_create_source(cur,
            "HARIA: Neurorobotic platform for supernumerary limb control",
            "HORIZON CORDIS", 2024, "Cyborg and Bionic Systems",
            "10.34133/cbsystems.0105", 'journal', 'academic_peer_reviewed', 1, 0.85),
        'soft_stroke': get_or_create_source(cur,
            "Soft robotic exosuit for stroke gait training: pilot RCT",
            "Various", 2023, "Frontiers in Neurology",
            "10.3389/fneur.2023.1296102", 'journal', 'academic_peer_reviewed', 1, 0.85),
        'care_framework': get_or_create_source(cur,
            "CARE: Customized Assistive Robot-based Education framework",
            "Various", 2025, "Frontiers in Robotics and AI",
            "10.3389/frobt.2025.1474741", 'journal', 'academic_peer_reviewed', 1, 0.80),
    }

    conn.commit()

    # ============================================================
    # MENTIONS
    # ============================================================
    mentions = [
        # (source_key, domain_code, claim, capability, timeline, ys, ye, conf,
        #  qol_dim, qol_dir, qol_mag, econ_dir, econ_mag,
        #  conditions, limitations, evidence_type, consensus)

        ('paro_cognitive', 'healthcare_elderly',
         "PARO intervention improves cognitive function in elderly with cognitive decline: 3.9 point improvement over 12 weeks in cognitive scores",
         'emotional_companionship', '2024-2030', 2024, 2030, 'high',
         'emotional', 'positive', 4, 'positive', 2,
         "Most effective in long-term care with staff support", "More rigorous larger RCTs needed",
         'RCT', 'STRONG'),

        ('pepper_caresses', 'healthcare_elderly',
         "Pepper robot with 18 hours interaction over 2 weeks significantly improves elderly mental health. Non-verbal communication ability positively affects satisfaction",
         'social_interaction', '2023-2030', 2023, 2030, 'high',
         'relational', 'positive', 3, 'conditional', 1,
         "Culturally-competent design essential; integration into care routines required", "Benefits depend on engagement level",
         'CASE_STUDY', 'MODERATE'),

        ('toyota_hsr', 'domestic_companion',
         "Toyota HSR compact mobile robot assists elderly/disabled with object retrieval, manipulation. Enables independent home living",
         'physical_manipulation', '2025-2035', 2025, 2035, 'high',
         'autonomy', 'positive', 4, 'positive', 3,
         "Requires robotic literacy; remote operation adds social dimension", "Cost barriers for broad adoption",
         'PROTOTYPE', 'STRONG'),

        ('ragt_meta', 'healthcare_rehab',
         "Meta-analysis (23 RCTs, n=907): robot-assisted gait training + conventional rehab significantly improves walking function, speed, balance, ADL performance in stroke patients",
         'collaborative_task', '2024-2030', 2024, 2030, 'high',
         'autonomy', 'positive', 4, 'conditional', 2,
         "Most beneficial in first 3 months post-stroke; end-effector > exoskeleton for subacute", "Adjunct to conventional therapy; high equipment costs",
         'META_ANALYSIS', 'STRONG'),

        ('exo_sci', 'mobility_exo',
         "Exoskeleton training for SCI patients: RCT evidence shows improved lower extremity motor scores, functional independence, and walking speed",
         'physical_manipulation', '2024-2032', 2024, 2032, 'high',
         'autonomy', 'positive', 4, 'mixed', 0,
         "ReWalk/Ekso/Indego systems. Functional gains despite modest speed improvement", "High device cost; donning/doffing burden; limited community adoption",
         'RCT', 'STRONG'),

        ('asd_efficacy', 'education_special',
         "Efficacy trial with 69 ASD children (avg age 4.4): biweekly 12-session robot therapy matches standard treatment outcomes while significantly increasing patient engagement",
         'social_interaction', '2024-2030', 2024, 2030, 'high',
         'relational', 'positive', 4, 'conditional', 2,
         "Robot effectiveness depends on predictability; personalization essential", "Clinical validation lags technical development",
         'RCT', 'STRONG'),

        ('asd_gaze', 'education_special',
         "Robot therapy improves eye contact, joint attention, imitation, communication, turn-taking in ASD children. 1-month deployment improves joint attention with adults",
         'social_interaction', '2024-2030', 2024, 2030, 'high',
         'relational', 'positive', 3, 'conditional', 1,
         "Embodied interaction sustains attention; transfers to human contexts", "Individual variation significant",
         'COHORT', 'MODERATE'),

        ('music_therapy_robot', 'arts_music',
         "Music therapy robot platform for ASD children improves social communication and increases creative expression through visual-audio-haptic environment",
         'creative_expression', '2024-2030', 2024, 2030, 'medium',
         'aesthetic', 'positive', 3, 'conditional', 1,
         "Visual-audio-haptic environment promotes creativity and motivation", "Limited pilot study base",
         'CASE_STUDY', 'EMERGING'),

        ('language_robot', 'education_language',
         "ASR-equipped robot language tutors reduce vocabulary/grammar errors and improve fluency compared to human tutors. Instant feedback technology effective",
         'cognitive_support', '2024-2030', 2024, 2030, 'medium',
         'autonomy', 'positive', 2, 'positive', 2,
         "No significant difference in pronunciation; grammar/fluency advantages", "Limited to structured language learning contexts",
         'COHORT', 'EMERGING'),

        ('surgery_qol', 'healthcare_surgery',
         "85% of robot-assisted surgery patients report high satisfaction. Pain reduction, faster physical recovery, improved mental well-being. Return in 33 vs 54 days",
         'physical_manipulation', '2024-2030', 2024, 2030, 'high',
         'autonomy', 'positive', 3, 'positive', 3,
         "Minimally invasive approach reduces complications", "Expectation management important",
         'SURVEY', 'STRONG'),

        ('exo_accept', 'mobility_exo',
         "Multicenter qualitative study: SCI patients accept robotic exoskeletons but request shorter donning time and improved operability for community use",
         'physical_manipulation', '2025-2035', 2025, 2035, 'medium',
         'autonomy', 'conditional', 2, 'negative', -2,
         "User acceptance depends on complexity, weight, social stigma", "Community integration needs improvement",
         'CASE_STUDY', 'MODERATE'),

        ('phantom_pain', 'healthcare_rehab',
         "Peripheral nerve stimulation suppresses phantom limb pain and provides prosthetic somatosensory feedback. 2-week study: significant pain reduction across multiple stimulation patterns",
         'sensory_augmentation', '2025-2030', 2025, 2030, 'high',
         'emotional', 'positive', 4, 'conditional', 0,
         "Touch awakening and closed-loop control integration effective", "Invasive neural implant; long-term safety data needed",
         'CASE_STUDY', 'MODERATE'),

        ('haptic_grasp', 'healthcare_rehab',
         "Vibrotactile haptic feedback prosthetics achieve 85.4% object property discrimination accuracy without visual inspection",
         'sensory_augmentation', '2024-2030', 2024, 2030, 'high',
         'autonomy', 'positive', 3, 'conditional', 1,
         "Multi-modal vibrotactile feedback optimal in dynamic environments", "Invasiveness level varies by approach",
         'PROTOTYPE', 'MODERATE'),

        ('supernumerary', 'domestic_companion',
         "Robogami third arm assists daily tasks (cup stabilization, object retrieval, cooking). Supernumerary robotic limbs expand human workspace and add new capabilities",
         'physical_manipulation', '2026-2035', 2026, 2035, 'medium',
         'autonomy', 'positive', 3, 'conditional', 2,
         "Reconfigurable design improves versatility", "Unstructured environment adaptation limited; control interface complexity",
         'PROTOTYPE', 'EMERGING'),

        ('elderly_loneliness', 'healthcare_mental',
         "RCT: Digital social robot BOCCO emo 4-week intervention significantly reduces loneliness, improves psychological well-being, depression, and self-rated health in elderly",
         'emotional_companionship', '2024-2030', 2024, 2030, 'high',
         'emotional', 'positive', 3, 'positive', 1,
         "Non-Western (Japanese) context. Growing RCT evidence base (8 studies)", "Long-term effects unverified",
         'RCT', 'MODERATE'),

        ('shimon_music', 'arts_music',
         "Shimon robot (deep learning) performs marimba with human musicians. Evolution toward human-like musical expressiveness demonstrates robot-human creative collaboration",
         'creative_expression', None, None, None, 'high',
         'aesthetic', 'positive', 3, 'mixed', 0,
         "Artistic significance in human-robot creative fusion", "Practical QoL application limited",
         'PROTOTYPE', 'EMERGING'),

        ('ethics_dependency', 'social_ethics',
         "Companion robots risk dependency and psychological maladaptation. Distress upon removal. Concern about reduced human interaction. Elderly-only robot design may increase isolation",
         'emotional_companionship', None, None, None, 'high',
         'relational', 'negative', -3, 'mixed', 0,
         "Especially dangerous during staff shortages; consent, autonomy, emotional dependency are ethical issues", "Human interaction displacement risk",
         'SURVEY', 'STRONG'),

        ('staff_burden', 'healthcare_elderly',
         "Care robot implementation increases staff operational burden despite reducing physical/mental load. Mixed positive/negative effects on workflow complexity",
         'collaborative_task', None, None, None, 'medium',
         'meaning', 'conditional', -2, 'negative', -1,
         "Implementation planning and training determine success", "Robots only effective in supplementary role",
         'SURVEY', 'MODERATE'),

        ('microsurgery', 'healthcare_surgery',
         "Robot-assisted microsurgery enables tremor correction and high-precision manipulation. 3D reconstruction and deep learning enable real-time precision enhancement",
         'physical_manipulation', '2024-2030', 2024, 2030, 'high',
         'autonomy', 'positive', 4, 'positive', 3,
         "Reduces surgeon fatigue; AI-assisted decision support", "Training costs; ethical responsibility for AI-assisted decisions",
         'COHORT', 'STRONG'),

        ('education_meta', 'education_stem',
         "Global meta-analysis (Nature): robot-based education improves academic achievement, computation, motivation, and performance compared to traditional methods",
         'cognitive_support', '2025-2030', 2025, 2030, 'high',
         'meaning', 'positive', 3, 'positive', 2,
         "Task-based learning with knowledge creation most effective", "Implementation and maintenance costs; teacher training required",
         'META_ANALYSIS', 'STRONG'),

        ('inclusion_edu', 'education_special',
         "Educational robotics promotes social inclusion for vulnerable youth through cognitive and socio-emotional skill stimulation",
         'cognitive_support', '2025-2030', 2025, 2030, 'medium',
         'relational', 'positive', 3, 'positive', 1,
         "Focus on vulnerable community implementation; dual skill/integration effect", "Limited programs; scalability challenges",
         'CASE_STUDY', 'EMERGING'),

        ('agri_precision', 'agriculture_precision',
         "Precision farming robots reduce water use 40%, eliminate pesticides. Strawberry picking robot handles 25 acres in 3 days (=30 workers). Automated greenhouses cut water 90-95%",
         'environmental_adaptation', '2025-2032', 2025, 2032, 'high',
         'cultural', 'positive', 2, 'positive', 4,
         "GPS + field monitoring sensors integration", "Labor force shift as social challenge; high initial investment",
         'CASE_STUDY', 'STRONG'),

        ('kismet', 'social_emotion',
         "Kismet (MIT, 1990s) expressed 9 emotion states via face/voice/movement. Caregiver-infant dyad model established foundation for social robot emotional interaction",
         'social_interaction', None, None, None, 'high',
         'emotional', 'positive', 2, 'mixed', 0,
         "Foundational pioneering research", "Limited practical application; theoretical contribution primary",
         'THEORETICAL', 'DEFINITIVE'),

        ('visual_nav', 'mobility_personal',
         "VISA system for visually impaired: indoor navigation + object detection + text recognition. Quadruped robot guide (RDog) reduces collisions and cognitive load",
         'sensory_augmentation', '2025-2032', 2025, 2032, 'high',
         'autonomy', 'positive', 4, 'conditional', 1,
         "SLAM technology critical for spatial awareness; force + audio guidance integration", "Scalability challenges",
         'PROTOTYPE', 'MODERATE'),

        ('elderly_care_review', 'healthcare_elderly',
         "Systematic review (2025): 4 types of care robots (humanoid/animal/cartoon/mechanical) provide daily assistance, cognitive enhancement, and emotional well-being for vulnerable elderly",
         'emotional_companionship', '2025-2035', 2025, 2035, 'high',
         'autonomy', 'positive', 3, 'conditional', 2,
         "Diverse robot forms address individual needs", "Implementation challenges and long-term effects are research focus",
         'META_ANALYSIS', 'MODERATE'),

        ('taiwan_paro', 'healthcare_mental',
         "Taiwan RCT: PARO intervention for long-term care elderly shows significant improvement in depression, loneliness, and QoL vs control group",
         'emotional_companionship', '2024-2030', 2024, 2030, 'high',
         'emotional', 'positive', 3, 'positive', 1,
         "Asian context effectiveness confirmed", "Long-term follow-up data needed; individual variation large",
         'RCT', 'MODERATE'),

        ('japan_culture', 'social_cultural',
         "Japanese animism and Shinto provide cultural foundation for robot acceptance vs Western preventive ethics. Ethics guidelines Western-centric, undervaluing Japanese vision of human-robot coexistence",
         'social_interaction', None, None, None, 'high',
         'cultural', 'positive', 3, 'mixed', 0,
         "Cultural relativism perspective essential", "Non-Western ethical frameworks need integration",
         'THEORETICAL', 'STRONG'),

        ('indigenous', 'social_cultural',
         "Indigenous youth robotics workshops inspire cultural pride and traditional knowledge respect through Pattern Thinking ethical framework emphasizing interrelationality",
         'creative_expression', None, None, None, 'medium',
         'cultural', 'positive', 4, 'conditional', 1,
         "Limited programs; continuous engagement needed", "Scalability challenges",
         'CASE_STUDY', 'EMERGING'),

        ('haria', 'healthcare_rehab',
         "HARIA neurorobotic platform enables independent/coordinated control of virtual and physical robot arms alongside biological arms via multimodal motor HMI",
         'sensory_augmentation', '2026-2032', 2026, 2032, 'high',
         'autonomy', 'positive', 4, 'conditional', 2,
         "Neural interface invasiveness; brain-machine interface training load", "Long-term implant safety data needed",
         'PROTOTYPE', 'MODERATE'),

        ('soft_stroke', 'healthcare_rehab',
         "Soft robotic exosuit pilot RCT: stroke patient gait training shows significant biomechanical and clinical parameter improvements",
         'physical_manipulation', '2024-2030', 2024, 2030, 'medium',
         'autonomy', 'positive', 3, 'conditional', 1,
         "Soft exosuit more comfortable than rigid types", "Small sample; larger RCT needed",
         'RCT', 'MODERATE'),

        ('care_framework', 'education_special',
         "CARE framework enables customized assistive robot-based education adapting to individual needs of vulnerable populations",
         'cognitive_support', '2025-2030', 2025, 2030, 'medium',
         'meaning', 'positive', 3, 'positive', 1,
         "Customization complexity; educator training required", "Scalability and sustainable operation model challenges",
         'PROTOTYPE', 'EMERGING'),
    ]

    inserted = 0
    for m in mentions:
        src_id = sources[m[0]]
        dom_id = domain_id(cur, m[1])
        quadrant = compute_quadrant(m[10], m[12])
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
        """, (src_id, dom_id, m[2], m[3], m[4], m[5], m[6], m[7],
              m[8], m[9], m[10], m[11], m[12],
              quadrant, m[13], m[14], m[15], m[16]))
        inserted += 1

    conn.commit()

    # Report
    total = cur.execute("SELECT COUNT(*) FROM mentions").fetchone()[0]
    src_count = cur.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
    print(f"\nDB3 batch 2 complete. Inserted {inserted} new mentions.")
    print(f"Total: {total} mentions, {src_count} sources")

    print("\nBy domain L1:")
    for row in cur.execute("""
        SELECT d1.name, COUNT(m.id) FROM mentions m
        JOIN domains d ON m.domain_id = d.id
        LEFT JOIN domains d1 ON d.parent_id = d1.id OR d.id = d1.id
        WHERE d1.level = 1
        GROUP BY d1.name ORDER BY COUNT(m.id) DESC
    """):
        print(f"  {row[0]}: {row[1]}")

    print("\nBy QoL dimension:")
    for row in cur.execute("SELECT qol_dimension, COUNT(*) FROM mentions GROUP BY qol_dimension ORDER BY COUNT(*) DESC"):
        print(f"  {row[0]}: {row[1]}")

    print("\nBy consensus:")
    for row in cur.execute("SELECT consensus_level_code, COUNT(*) FROM mentions GROUP BY consensus_level_code ORDER BY COUNT(*) DESC"):
        print(f"  {row[0]}: {row[1]}")

    print("\nBy quadrant:")
    for row in cur.execute("SELECT quadrant, COUNT(*) FROM mentions GROUP BY quadrant ORDER BY quadrant"):
        print(f"  Quadrant {row[0]}: {row[1]}")

    conn.close()


if __name__ == '__main__':
    seed()
