"""
Batch 2: Additional DB2 event relations from research agent analysis.
77 new causal/influence relationships identified.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'gpt_impact_genealogy.db')


def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()

    # Build event name -> id lookup
    event_ids = {}
    for row in cur.execute("SELECT id, name FROM usage_events"):
        event_ids[row[1]] = row[0]

    existing = set()
    for row in cur.execute("SELECT from_event_id, to_event_id, relation_type FROM event_relations"):
        existing.add((row[0], row[1], row[2]))

    def add_rel(from_name, to_name, rel_type, strength, lag, desc):
        fid = event_ids.get(from_name)
        tid = event_ids.get(to_name)
        if not fid or not tid:
            return False
        if (fid, tid, rel_type) in existing:
            return False
        cur.execute("""
            INSERT OR IGNORE INTO event_relations
            (from_event_id, to_event_id, relation_type, strength, time_lag_years, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (fid, tid, rel_type, strength, lag, desc))
        existing.add((fid, tid, rel_type))
        return True

    count = 0

    # ============================================================
    # AUTOMOBILE internal relations
    # ============================================================
    rels = [
        # Freedom chain
        ("Personal Freedom Symbol", "Dating Culture Transformation", "enabled", 0.8, 30,
         "Freedom of mobility enabled unsupervised courtship away from parental oversight"),
        ("Personal Freedom Symbol", "American Cruising Culture", "enabled", 0.7, 35,
         "Freedom symbolism directly motivated youth cruising as autonomous social activity"),
        ("American Cruising Culture", "Hot Rod Rock Music", "inspired", 0.7, 6,
         "Cruising culture inspired ~1500 car songs celebrating automotive freedom 1961-1965"),
        ("American Cruising Culture", "Drive-in Cinema", "parallel", 0.6, -22,
         "Cruising and drive-ins co-developed as car-centered youth social spaces"),
        ("Mass Production (Ford Model T)", "Sunday Drive Family Ritual", "enabled", 0.8, 12,
         "Affordable cars enabled weekly family drives to countryside as leisure ritual"),
        ("Sunday Drive Family Ritual", "Road Trip Culture", "evolved_from", 0.7, 10,
         "Weekend drives evolved into extended road trips as highway system expanded"),
        ("Road Trip Culture", "Blue Ridge Parkway Scenic Highway", "inspired", 0.6, 5,
         "Demand for scenic driving led to purpose-built pleasure roads"),
        ("Suburbanization", "Jaywalking and Pedestrian Displacement", "enabled", 0.85, 0,
         "Car-centric suburban design drove redefinition of streets as automobile-exclusive zones"),
        ("Jaywalking and Pedestrian Displacement", "Car-Free Movements", "inspired", 0.7, 71,
         "Loss of pedestrian rights eventually inspired organized resistance to car hegemony"),
        ("Social Isolation via Car-Centric Design", "Car-Free Movements", "inspired", 0.8, 41,
         "Recognition of automobile-caused isolation motivated car-free advocacy"),
        ("Suburbanization", "Road Rage Phenomenon", "enabled", 0.6, 60,
         "Car-dependent commuting created chronic traffic frustration leading to road rage"),
        ("Suburbanization", "Automobile Noise Pollution", "amplified", 0.7, 30,
         "Mass automobile use in dense suburban/urban areas amplified noise pollution"),
        ("Mass Production (Ford Model T)", "Wheelchair-Accessible Vehicles", "prerequisite", 0.5, 37,
         "Mass production infrastructure prerequisite for vehicle modification for disability"),
        ("Wheelchair-Accessible Vehicles", "Elderly Mobility and Aging in Place", "enabled", 0.6, 25,
         "Accessible vehicle technology extended to elderly mobility solutions"),
        ("Automobile as Art Form", "Italian Automotive Design Renaissance", "evolved_from", 0.8, 20,
         "General car-as-art appreciation evolved into formalized Italian design philosophy"),
        ("Italian Automotive Design Renaissance", "1959 Cadillac Tailfin Design Peak", "parallel", 0.5, 5,
         "Italian and American design schools competed in parallel aesthetic innovation"),
        ("Personal Freedom Symbol", "Kerouac On the Road and Road Movies", "inspired", 0.8, 37,
         "Automobile freedom symbolism directly inspired Beat literary exploration"),
        ("Kerouac On the Road and Road Movies", "Car as Psychological Sanctuary", "inspired", 0.5, -7,
         "Road literature legitimized car as space for inner exploration and psychological refuge"),
        ("Mass Production (Ford Model T)", "Lowrider Culture", "prerequisite", 0.6, 32,
         "Affordable used cars provided raw material for Chicano artistic transformation"),
        ("Lowrider Culture", "Classic Car Restoration Craft", "parallel", 0.5, 30,
         "Both movements share deep engagement with automotive craft and customization"),
        ("Mass Production (Ford Model T)", "Emotional Attachment to Cars", "enabled", 0.7, 42,
         "Mass ownership created personal car-human relationships across lifespans"),
        ("Women's Mobility", "Women in Motorsport", "enabled", 0.5, 30,
         "Women's driving normalization was prerequisite for competitive motorsport participation"),
        ("Hot Rod Rock Music", "Bosozoku Subculture", "inspired", 0.4, 9,
         "American automotive rebellion culture influenced Japanese youth subculture"),
        ("American Cruising Culture", "Touge Mountain Pass Racing", "parallel", 0.4, 15,
         "Both represent grassroots automotive skill culture outside institutional racing"),
    ]
    for r in rels:
        if add_rel(*r):
            count += 1

    # ============================================================
    # TELEPHONE internal relations
    # ============================================================
    rels_tel = [
        ("Party Line Communities", "Rural Women Telephone Isolation Reduction", "enabled", 0.85, 30,
         "Party lines provided 'sunlight' breaking homesteader women's months of solitude"),
        ("Social Chatting Culture", "Telephone Anxiety", "enabled", 0.6, 20,
         "Social expectation of telephone availability created anxiety about performance/intrusion"),
        ("Telephone Anxiety", "Answering Machine and Mediated Presence", "inspired", 0.5, 29,
         "Desire to buffer telephone demands motivated answering machine adoption"),
        ("Answering Machine and Mediated Presence", "Telemarketing Intrusion", "enabled", 0.4, 41,
         "Message-mediated presence created infrastructure exploited by telemarketers"),
        ("Emergency Services (911)", "Early Telemedicine via Telephone", "parallel", 0.5, -89,
         "Both represent telephone as healthcare infrastructure, developing in parallel"),
        ("Telephone Operators as Women's Employment", "Rural Women Telephone Isolation Reduction", "enabled", 0.5, 50,
         "Female operators facilitated rural women's connection to telephone network"),
        ("Long-Distance Family Bonds", "Emotional Intimacy via Voice", "amplified", 0.8, -20,
         "Family voice bonds deepened understanding of telephone's emotional intimacy capacity"),
        ("Social Chatting Culture", "Party Line Communities", "parallel", 0.7, -10,
         "Social chatting and party line communities developed as parallel social telephone uses"),
        ("Teen Phone Culture", "Telephone Anxiety", "amplified", 0.5, 30,
         "Teen phone obsession intensified adult anxiety about telephone intrusion"),
        ("Telefon Hirmondo Telephone Newspaper", "Radio Broadcasting via Telephone Lines", "inspired", 0.7, 27,
         "Hungarian telephone newspaper model inspired European radio-over-telephone experiments"),
        ("Business Communication Tool", "Telephone Directory Community Identity", "enabled", 0.8, 2,
         "Business subscriber directories evolved into community identity records"),
        ("Samaritans Crisis Hotline", "Phone Tree Grassroots Organizing", "parallel", 0.4, 17,
         "Both represent grassroots appropriation of telephone for social organizing"),
        ("Mobile Phone Revolution in Africa", "Village Pay Phone Gender Empowerment", "parallel", 0.7, -5,
         "African mobile revolution and Grameen village phone model co-developed"),
        ("TTY/TDD Deaf Telephone Access", "Wheelchair-Accessible Vehicles", "parallel", 0.3, -19,
         "Both represent disability rights movement's technology accessibility achievements"),
        ("Telephone Surveillance and Privacy Erosion", "Telemarketing Intrusion", "amplified", 0.5, 30,
         "Surveillance infrastructure normalized telephone privacy invasion for commercial exploitation"),
    ]
    for r in rels_tel:
        if add_rel(*r):
            count += 1

    # ============================================================
    # PRINTING PRESS internal relations
    # ============================================================
    rels_print = [
        ("Literacy Democratization", "Women Writers and Professional Authorship", "enabled", 0.7, 200,
         "Mass literacy created audience for women's writing and professional female authorship"),
        ("Literacy Democratization", "English Almanacs Popular Knowledge", "enabled", 0.7, 50,
         "Literacy enabled cheap almanacs to reach 400,000 copies/year by 17th century"),
        ("Broadside Ballads Popular Poetry", "Chapbooks Popular Literature", "parallel", 0.8, -20,
         "Broadsides and chapbooks co-developed as complementary popular print media"),
        ("Chapbooks Popular Literature", "Brothers Grimm Illustrated Fairy Tales", "inspired", 0.7, 312,
         "Oral traditions preserved in chapbooks provided source material for Grimm collection"),
        ("Vernacular Literature Flourishing", "Women Writers and Professional Authorship", "enabled", 0.6, 150,
         "Vernacular literary market enabled women to write in native languages for wide audiences"),
        ("Renaissance Woodcut Book Illustration", "Vesalius Anatomical Illustration", "enabled", 0.7, 73,
         "Woodcut illustration techniques prerequisite for Vesalius's anatomical masterwork"),
        ("Renaissance Woodcut Book Illustration", "Printed Botanical Illustrations and Herbals", "enabled", 0.8, 15,
         "Woodcut technology directly enabled botanical illustration printing"),
        ("Printed Botanical Illustrations and Herbals", "Culpeper's English Vernacular Medicine", "inspired", 0.6, 168,
         "Herbal illustration tradition inspired Culpeper's vernacular medical democratization"),
        ("Bible Mass Production", "Hebrew Printing and Jewish Literacy", "inspired", 0.6, 59,
         "Christian Bible printing inspired Jewish communities to establish Hebrew presses"),
        ("Protestant Reformation", "Women's Spiritual Literature", "enabled", 0.5, 33,
         "Reformation emphasis on individual scripture reading opened space for women's spiritual writing"),
        ("Literacy Democratization", "Conduct Books and Social Behavior", "enabled", 0.7, 35,
         "Literacy enabled conduct books to reach aspiring middle class across social boundaries"),
        ("Newspaper and Public Sphere", "Pamphlet Wars and Propaganda", "amplified", 0.6, -83,
         "Newspaper infrastructure amplified pamphlet distribution and ideological warfare"),
        ("Printed Maps and Atlases", "Scientific Revolution", "enabled", 0.5, 68,
         "Printed maps expanded geographical understanding supporting empirical scientific worldview"),
        ("Music Score Printing", "Broadside Ballads Popular Poetry", "parallel", 0.5, 19,
         "Music printing and ballad printing co-developed as popular cultural media"),
        ("First Printed Cookbook", "Culpeper's English Vernacular Medicine", "parallel", 0.4, 183,
         "Both represent democratization of practical domestic knowledge through printing"),
        ("Personal Reading as Private Experience", "Kerouac On the Road and Road Movies", "prerequisite", 0.3, 457,
         "Private reading culture prerequisite for literary road narratives consumed individually"),
        ("Ottoman Printing Restriction", "Information Overload and Misinformation", "opposed", 0.5, 15,
         "Ottoman restriction represented opposite response to same information proliferation challenge"),
        ("Korean Movable Type and Hangul", "Bible Mass Production", "preceded", 0.3, 221,
         "Korean movable type (1234) preceded Gutenberg by two centuries as knowledge democratization"),
        ("Information Overload and Misinformation", "Telemarketing Intrusion", "inspired", 0.3, 490,
         "Information pollution pattern from print era persisted into telephone commercial exploitation"),
    ]
    for r in rels_print:
        if add_rel(*r):
            count += 1

    # ============================================================
    # ELECTRICITY internal relations
    # ============================================================
    rels_elec = [
        ("Night-time Activity Expansion", "Domestic Electrification", "enabled", 0.8, 30,
         "Night-time lighting prerequisite for electric domestic appliance adoption"),
        ("Domestic Electrification", "Great White Way (Theater District)", "parallel", 0.6, -25,
         "Domestic and commercial electrification co-developed as electricity infrastructure expanded"),
        ("Radio and Shared National Culture", "Hot Rod Rock Music", "enabled", 0.7, 41,
         "National radio culture synchronized youth identity that car songs celebrated"),
        ("Radio and Shared National Culture", "American Cruising Culture", "enabled", 0.6, 35,
         "Radio created synchronized cultural references enabling coordinated youth cruising identity"),
    ]
    for r in rels_elec:
        if add_rel(*r):
            count += 1

    # ============================================================
    # CROSS-GPT relations
    # ============================================================
    rels_cross = [
        ("Literacy Democratization", "Telephone Directory Community Identity", "prerequisite", 0.6, 428,
         "Mass literacy prerequisite for telephone directories to function as community identity records"),
        ("Newspaper and Public Sphere", "Telefon Hirmondo Telephone Newspaper", "inspired", 0.7, 293,
         "Newspaper format directly inspired telephone-based news service concept"),
        ("Personal Freedom Symbol", "Mobile Phone Revolution in Africa", "inspired", 0.3, 80,
         "Automobile freedom model influenced framing of mobile phone as empowerment technology"),
        ("Women's Mobility", "Telephone Operators as Women's Employment", "parallel", 0.4, -40,
         "Both represent women's economic empowerment through technology in same era"),
        ("Women Writers and Professional Authorship", "Rural Women Telephone Isolation Reduction", "prerequisite", 0.3, 280,
         "Women's literary autonomy established cultural value of women's voices that telephone later amplified"),
        ("Night-time Activity Expansion", "Drive-in Cinema", "enabled", 0.7, 43,
         "Electric lighting prerequisite for outdoor nighttime cinema"),
        ("Night-time Activity Expansion", "Teen Phone Culture", "enabled", 0.5, 60,
         "Extended evening hours enabled late-night telephone socializing"),
        ("Domestic Electrification", "Answering Machine and Mediated Presence", "prerequisite", 0.8, 29,
         "Domestic electricity prerequisite for electronic recording devices"),
        ("Radio and Shared National Culture", "Kerouac On the Road and Road Movies", "enabled", 0.4, 37,
         "Radio-created national culture gave Beat writers shared references to critique"),
        ("Birth of Tourism", "Sunday Drive Family Ritual", "inspired", 0.5, 90,
         "Steam-era tourism concept evolved into automobile Sunday drives"),
        ("Birth of Tourism", "Road Trip Culture", "evolved_from", 0.6, 100,
         "Railway tourism model evolved into automobile road trip culture"),
        ("Scientific Revolution", "Early Telemedicine via Telephone", "prerequisite", 0.4, 336,
         "Scientific medical knowledge prerequisite for meaningful telephone medical consultation"),
        ("Samaritans Crisis Hotline", "Dial-A-Poem Telephone Art", "parallel", 0.3, 15,
         "Both represent creative non-commercial appropriation of telephone for human connection"),
        ("Jaywalking and Pedestrian Displacement", "Automobile Noise Pollution", "parallel", 0.6, 9,
         "Both represent negative externalities of automobile hegemony on urban commons"),
        ("Environmental Pollution", "Car-Free Movements", "inspired", 0.7, 41,
         "Environmental damage from automobiles directly inspired car-free advocacy"),
    ]
    for r in rels_cross:
        if add_rel(*r):
            count += 1

    conn.commit()

    # Report
    total = cur.execute("SELECT COUNT(*) FROM event_relations").fetchone()[0]
    print(f"\nDB2 relations batch 2 complete. Added {count} new relations.")
    print(f"Total relations: {total}")

    print("\nBy relation type:")
    for r in cur.execute("""
        SELECT relation_type, COUNT(*) FROM event_relations
        GROUP BY relation_type ORDER BY COUNT(*) DESC
    """):
        print(f"  {r[0]}: {r[1]}")

    # Network stats
    nodes_with_edges = cur.execute("""
        SELECT COUNT(DISTINCT id) FROM (
            SELECT from_event_id as id FROM event_relations
            UNION SELECT to_event_id FROM event_relations
        )
    """).fetchone()[0]
    total_events = cur.execute("SELECT COUNT(*) FROM usage_events").fetchone()[0]
    print(f"\nNetwork: {nodes_with_edges}/{total_events} events connected ({100*nodes_with_edges//total_events}%)")

    conn.close()


if __name__ == '__main__':
    seed()
