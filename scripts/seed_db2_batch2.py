"""
Batch 2: Additional DB2 events from automobile, telephone, and printing press research agents.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'gpt_impact_genealogy.db')


def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()

    gpt_ids = {}
    for row in cur.execute("SELECT id, name FROM gpt_technologies"):
        gpt_ids[row[1]] = row[0]

    auto_id = gpt_ids["Automobile"]
    tel_id = gpt_ids["Telephone"]
    print_id = gpt_ids["Printing Press"]

    # Check existing events to avoid duplicates
    existing = set(r[0] for r in cur.execute("SELECT name FROM usage_events").fetchall())

    def insert_event(gpt_id, name, name_ja, ys, ye, yc, region, domain, etype,
                     desc, trigger, sa, se, sm, sr, sau, sc, secon,
                     intended, path_type, evidence):
        if name in existing:
            return
        cur.execute("""
            INSERT INTO usage_events
            (gpt_id, name, name_ja, year_start, year_end, year_confidence,
             region, domain, event_type, description, trigger_pattern,
             score_aesthetic, score_emotional, score_meaning,
             score_relational, score_autonomy, score_cultural,
             score_economic_macro,
             intended_by_inventor, adoption_path_type, evidence_strength)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (gpt_id, name, name_ja, ys, ye, yc, region, domain, etype,
              desc, trigger, sa, se, sm, sr, sau, sc, secon,
              intended, path_type, evidence))
        existing.add(name)

    # ============================================================
    # AUTOMOBILE — Additional events
    # ============================================================
    insert_event(auto_id, "Italian Automotive Design Renaissance", "イタリア自動車デザイン・ルネサンス",
        1950, 1965, "decade", "Italy", "artistic", "aesthetic",
        "Pininfarina, Zagato transformed automobiles into moving artworks through revolutionary aesthetic principles",
        "Post-war European recovery + haute couture influence on industrial design",
        5, 3, 2, 1, 1, 5, -1, 1, "linear", "strong")

    insert_event(auto_id, "American Cruising Culture", "アメリカンクルージング文化",
        1955, 1975, "decade", "USA", "leisure", "cultural",
        "Teenage cruising on Whittier Blvd, Woodward Ave became primary unsupervised youth congregation defining adolescent autonomy",
        "Affordable used cars + Baby Boomer generation + interstate highway",
        2, 4, 2, 5, 5, 3, -2, 0, "grassroots", "strong")

    insert_event(auto_id, "Sunday Drive Family Ritual", "日曜ドライブの家族儀式",
        1920, 1950, "decade", "USA", "leisure", "cultural",
        "Weekly family drive to countryside became cultural institution for family bonding, landscape appreciation, escape from urban life",
        "Affordable automobiles + expanding roads + national parks",
        3, 3, 3, 5, 2, 3, -1, 0, "grassroots", "strong")

    insert_event(auto_id, "Lowrider Culture", "ローライダー文化",
        1940, 1975, "decade", "USA", "artistic", "cultural",
        "Mexican-American veterans created lowriders as hydraulic-suspended art installations with airbrushed Chicano iconography. Moving monuments of cultural identity and resistance",
        "WWII veteran skills + economic discrimination + Chicano Movement",
        5, 4, 5, 4, 4, 5, -2, 0, "appropriation", "strong")

    insert_event(auto_id, "Bosozoku Subculture", "暴走族サブカルチャー",
        1950, 1985, "decade", "Japan", "social", "cultural",
        "Japanese youth rebellion through extreme aesthetic customization: modified exhausts, kamikaze motifs. Peaked at 42,510 members 1982. Inspired anime (Akira)",
        "Post-war social dislocation + American greaser influence + urban motorcycle culture",
        4, 3, 2, 4, 4, 4, -2, 0, "grassroots", "strong")

    insert_event(auto_id, "Hot Rod Rock Music", "ホットロッドロック音楽",
        1961, 1970, "exact", "USA", "artistic", "aesthetic",
        "~1,500 car songs recorded 1961-1965. Beach Boys, Chuck Berry established automobile as primary metaphor for freedom and youth identity in rock music",
        "California surf culture + youth automotive enthusiasm + rock music",
        3, 5, 3, 3, 4, 3, 0, 0, "serendipitous", "strong")

    insert_event(auto_id, "Kerouac On the Road and Road Movies", "ケルアック『路上』とロードムービー",
        1957, 1991, "exact", "USA", "artistic", "aesthetic",
        "Kerouac's novel established master narrative for automobile-based exploration. Inspired Easy Rider (1969), Paris Texas (1984), Thelma & Louise (1991)",
        "Post-war identity + countercultural challenge + Buddhist influence",
        4, 5, 5, 2, 5, 4, -2, 0, "serendipitous", "strong")

    insert_event(auto_id, "Car as Psychological Sanctuary", "心理的避難所としての車",
        1950, None, "decade", "Global", "domestic", "social",
        "Automobile as mobile sanctuary for psychological refuge. Night driving as therapy. Car seat as most accessible private space for emotional processing",
        "Urbanization eliminating private space + social acceleration",
        2, 5, 3, 0, 5, 1, -3, 0, "serendipitous", "moderate")

    insert_event(auto_id, "Blue Ridge Parkway Scenic Highway", "ブルーリッジパークウェイ",
        1935, 1987, "exact", "USA", "leisure", "aesthetic",
        "469-mile non-commercial scenic drive designed for pleasure, not efficiency. Established template for scenic byways prioritizing aesthetic value",
        "New Deal conservation + WPA programs + automotive tourism demand",
        4, 3, 3, 2, 2, 4, -1, 1, "linear", "strong")

    insert_event(auto_id, "Wheelchair-Accessible Vehicles", "車椅子対応車両",
        1945, 1990, "decade", "USA", "healthcare", "social",
        "Post-WWII hand controls (Alan Ruprecht 1952), hydraulic lifts. ADA 1990 mandated standards. Primary independence infrastructure for mobility-disabled",
        "WWII disabled veterans + disability rights movement + ADA",
        0, 3, 5, 3, 5, 2, 0, 1, "linear", "strong")

    insert_event(auto_id, "Car-Free Movements", "カーフリー運動",
        1991, None, "exact", "Global", "urban", "social",
        "Reclaim the Streets (1991), Critical Mass (1992), Ghent/Amsterdam/Barcelona car-free zones. Documented positive QoL from automobile removal: air quality, safety, social interaction",
        "Environmental movement + pedestrian advocacy + European urban design tradition",
        3, 3, 3, 5, 3, 4, 0, 0, "resistance", "strong")

    insert_event(auto_id, "Jaywalking and Pedestrian Displacement", "ジェイウォーキングと歩行者排除",
        1920, 1935, "decade", "USA", "urban", "political",
        "Motordom redefined urban public space from pedestrian commons to automobile zones. 'Jaywalker' campaign (1920s). Children disappeared from streets. Loss of centuries of pedestrian rights",
        "Auto industry strategic campaign + traffic engineering + political alignment",
        -3, -3, -2, -4, -5, -3, -2, 0, "serendipitous", "strong")

    insert_event(auto_id, "Road Rage Phenomenon", "ロードレージ現象",
        1980, None, "decade", "Global", "social", "social",
        "82% of drivers committed road rage acts; 1,035 fatalities/year; 500% increase 2006-2015. Cars amplify aggression through anonymity and disassociation",
        "Traffic congestion + anonymity effects + declining social cohesion",
        -4, -5, -2, -4, -2, -2, -3, 0, "serendipitous", "strong")

    insert_event(auto_id, "Automobile Noise Pollution", "自動車騒音公害",
        1929, None, "exact", "Global", "other", "mixed",
        "Motor Cars Excessive Noise regulations (UK 1929). By 2000, 97.4% of continental US affected. Causes hypertension, hearing loss, depression, cardiovascular disease",
        "Urban densification + environmental movement + WHO recognition",
        -5, -3, -1, -2, -1, -2, -3, 0, "serendipitous", "strong")

    insert_event(auto_id, "Classic Car Restoration Craft", "クラシックカー修復職人技",
        1970, None, "decade", "Global", "artistic", "cultural",
        "Restoration evolved into serious craft discipline preserving endangered mechanical and metalworking skills. McPherson College established formal educational pathway. Elder-to-youth knowledge transmission",
        "Recognition of disappearing mechanical knowledge + nostalgia + community formation",
        3, 4, 4, 4, 3, 5, -2, 0, "grassroots", "moderate")

    insert_event(auto_id, "Touge Mountain Pass Racing", "峠レース文化",
        1970, None, "decade", "Japan", "leisure", "cultural",
        "Underground mountain pass racing developing drifting techniques. Keiichi Tsuchiya 'Drift King'. Initial D manga/anime (1995+) made culture globally visible",
        "Limited racetrack access + mountainous geography + youth culture",
        3, 5, 3, 4, 5, 4, -1, 0, "grassroots", "strong")

    insert_event(auto_id, "Emotional Attachment to Cars", "自動車への感情的愛着",
        1950, None, "decade", "Global", "domestic", "social",
        "14% report emotional attachment; 23% remember first cars nostalgically; 78% associate cars with major life events. Cars as repositories of personal and family history",
        "Automobile permanence across lifespans + association with life transitions",
        2, 5, 4, 3, 3, 2, -2, 0, "serendipitous", "strong")

    insert_event(auto_id, "Women in Motorsport", "モータースポーツにおける女性",
        1950, None, "decade", "Global", "social", "social",
        "Pat Moss-Carlsson won European Ladies' Rally 5x. Michèle Mouton first woman WRC champion. Challenged gender norms, established women's technical competence",
        "Post-WWII gender destabilization + women's liberation + professional motorsport expansion",
        2, 3, 4, 3, 5, 3, 0, 0, "resistance", "strong")

    insert_event(auto_id, "Elderly Mobility and Aging in Place", "高齢者モビリティと地域での加齢",
        1970, None, "decade", "Global", "healthcare", "social",
        "Automobiles as primary infrastructure enabling elderly independence and community participation. Modified vehicles with hand controls, automatic transmissions. Difference between independent living and institutionalization",
        "Aging population + decline of public transportation + suburban sprawl",
        0, 2, 4, 3, 5, 2, -1, 0, "serendipitous", "strong")

    insert_event(auto_id, "1959 Cadillac Tailfin Design Peak", "1959年キャデラックテールフィンデザイン頂点",
        1955, 1965, "exact", "USA", "artistic", "aesthetic",
        "1959 Cadillac Eldorado represented peak of automobile as pure aesthetic expression. Tailfins became globally recognizable symbol of 1950s modernity and American cultural confidence",
        "Post-war prosperity + Harley Earl design philosophy + advertising",
        5, 4, 2, 1, 1, 4, 0, 1, "linear", "strong")

    # ============================================================
    # TELEPHONE — Additional events
    # ============================================================
    insert_event(tel_id, "Telefon Hirmondo Telephone Newspaper", "テレフォン・ヒールモンドー電話新聞",
        1893, 1944, "exact", "Hungary", "culture", "cultural",
        "Tivadar Puskas created service delivering daily news, music, stock quotations, literary criticism via telephone. 6,000+ subscribers. Preceded radio by decades",
        "Edison background + desire for commercial telephone use",
        4, 2, 3, 3, 3, 5, 2, 1, "linear", "strong")

    insert_event(tel_id, "Samaritans Crisis Hotline", "サマリタンズ危機相談",
        1953, None, "exact", "UK/Global", "healthcare", "spiritual",
        "Rev. Chad Varah established first suicide prevention hotline. Pioneered non-judgmental telephone emotional support. Now operates in dozens of countries",
        "Funeral of 14-year-old suicide victim + recognition of isolation",
        0, 5, 5, 5, 3, 3, -1, 0, "grassroots", "strong")

    insert_event(tel_id, "Mobile Phone Revolution in Africa", "アフリカ携帯電話革命",
        2000, None, "exact", "Sub-Saharan Africa", "communication", "social",
        "Mobile access expanded from 1.7/100 (2000) to 82.4/100 (2018). 15% employment increase. Improved maternal-child health. Transformed rural community QoL",
        "Cost reduction + entrepreneurial models (Village Pay Phone) + NGO investment",
        1, 3, 4, 4, 5, 2, 4, 0, "grassroots", "strong")

    insert_event(tel_id, "TTY/TDD Deaf Telephone Access", "TTY/TDD聴覚障害者電話アクセス",
        1964, None, "exact", "USA/Global", "healthcare", "social",
        "Robert Weitbrecht (himself deaf) invented acoustic coupler for text telephone. ADA Title IV (1990) mandated relay services. Liberated 45M+ hearing-impaired from reliance on intermediaries",
        "Weitbrecht's own deafness + recognition of systematic exclusion",
        0, 2, 5, 5, 5, 3, 0, 1, "linear", "strong")

    insert_event(tel_id, "Dial-A-Poem Telephone Art", "ダイアル・ア・ポエム電話アート",
        1968, 1970, "exact", "USA", "artistic", "aesthetic",
        "John Giorno rigged 10 phones to deliver free poetry by Amiri Baraka, Patti Smith at Architectural League. Buddhist mantras, experimental art. FBI shut it down. Proved telephone as artistic medium",
        "Warhol/Rauschenberg influence + desire to liberate poetry from institutions",
        5, 3, 4, 2, 3, 5, -2, 0, "grassroots", "strong")

    insert_event(tel_id, "Music On Hold", "保留音楽",
        1962, None, "exact", "Global", "culture", "aesthetic",
        "Alfred Levy's serendipitous discovery (loose wire picking up radio). Callers with music hold 30s longer. Transformed waiting from anxiety to aesthetic pleasure",
        "Accidental technical discovery + recognition of psychological impact",
        3, 2, 0, 0, 0, 2, 2, 0, "serendipitous", "moderate")

    insert_event(tel_id, "Telephone Booth as Public Art", "電話ボックスのパブリックアート",
        1990, None, "decade", "Global", "artistic", "aesthetic",
        "As booths became obsolete, artists repurposed them: Banksy's submerged booth, Times Square immigrant stories, Telepoem Booth. Cultural persistence beyond functional utility",
        "Technological obsolescence + artistic recognition of cultural symbol",
        5, 3, 3, 2, 1, 5, -1, 0, "appropriation", "moderate")

    insert_event(tel_id, "Telephone Surveillance and Privacy Erosion", "電話監視とプライバシー侵食",
        1960, None, "decade", "Global", "political", "political",
        "Watergate-era fears. NSA revelations: 28% reduction in media activity, 24% topic avoidance. 68% experience surveillance anxiety. Chilling effect on free expression",
        "Government/corporate surveillance capability + knowledge asymmetry",
        -2, -4, -2, -3, -5, -2, -2, 0, "serendipitous", "strong")

    insert_event(tel_id, "Telemarketing Intrusion", "テレマーケティング侵入",
        1990, None, "decade", "Global", "commerce", "social",
        "TCPA 1991 response to 'relentless' telemarketing. Do-Not-Call Registry 2003. 2.4B+ robocalls/month. Systematic intrusion on sanctuary of the home",
        "Commercial scale-up + cost efficiency + regulatory loopholes",
        -2, -3, -1, -2, -4, -1, -3, 0, "repurposed", "strong")

    insert_event(tel_id, "Answering Machine and Mediated Presence", "留守電話と仲介された存在",
        1949, None, "exact", "Global", "domestic", "cultural",
        "1949 Electronic Secretary enabled asynchronous voice messaging. Transformed from 'always available' to 'message-mediated presence'. Created call screening, surveillance anxiety, persistent accessibility expectations",
        "Technology maturation + desire for communication buffer",
        0, -1, 0, -2, 2, 2, 1, 0, "linear", "strong")

    insert_event(tel_id, "Rural Women Telephone Isolation Reduction", "農村女性の電話による孤立軽減",
        1930, 1980, "decade", "USA/Australia", "domestic", "social",
        "Party lines described as 'sunlight' breaking months of homesteader women's solitude. Used for medical consultation, emergency alerts, social communion. Partially mitigated depression linked to frontier separation",
        "Recognition of mental health crisis + REA 1949 infrastructure investment",
        0, 4, 3, 5, 2, 2, 0, 0, "serendipitous", "suggestive")

    insert_event(tel_id, "Village Pay Phone Gender Empowerment", "ビレッジペイフォンのジェンダーエンパワメント",
        1995, None, "exact", "Bangladesh/South Asia", "social", "social",
        "Grameen Bank model: rural women lease mobile phones for community fee-per-call service. Creates female entrepreneurship, community communication hub. 5% gender gap remains",
        "Grameen microfinance model + gender equity focus + rural communication gap",
        0, 2, 4, 3, 4, 2, 4, 0, "appropriation", "strong")

    insert_event(tel_id, "Early Telemedicine via Telephone", "電話による初期遠隔医療",
        1879, 1970, "decade", "Europe/USA", "healthcare", "technological",
        "1879 Lancet proposed telephone to reduce office visits. 1905 Einthoven transmitted heart sounds. 1967 EKG via telephone wires. Pioneered remote diagnosis and rural healthcare access",
        "Transportation limitations + voice transmission capacity for clinical data",
        0, 1, 4, 1, 4, 1, 2, 0, "repurposed", "strong")

    insert_event(tel_id, "Telephone Directory Community Identity", "電話帳のコミュニティ・アイデンティティ",
        1878, 2010, "exact", "Global", "social", "cultural",
        "First directory: New Haven 1878, 50 subscribers on cardboard. Evolved into community portraits. Presence = social existence; absence = invisibility. Annual snapshot of neighborhood evolution",
        "Operational need for subscriber access + business directory demand",
        1, 1, 3, 2, 1, 3, 1, 1, "linear", "moderate")

    insert_event(tel_id, "Phone Tree Grassroots Organizing", "電話チェーンによる草の根組織化",
        1970, None, "decade", "Global", "political", "political",
        "Phone trees became foundational infrastructure for grassroots movements: civil rights, environmental, anti-war, feminist consciousness-raising. Low-cost mass mobilization bypassing media gatekeeping",
        "Technology availability + grassroots necessity + cost efficiency vs broadcast",
        0, 2, 4, 3, 4, 2, 0, 0, "grassroots", "suggestive")

    # ============================================================
    # PRINTING PRESS — Additional events
    # ============================================================
    insert_event(print_id, "Renaissance Woodcut Book Illustration", "ルネサンス木版画挿絵",
        1470, 1550, "decade", "Europe", "artistic", "aesthetic",
        "Woodcut illustrations integrated into printed books. Albrecht Durer elevated medium to fine art with 300+ prints circulating throughout Europe. Visual textbook for artists, brought fine art into ordinary homes",
        "Technological compatibility of movable type and woodblock + artist ambition",
        5, 4, 3, 2, 3, 4, 1, 0, "serendipitous", "strong")

    insert_event(print_id, "First Printed Cookbook", "初の印刷レシピ本",
        1470, 1500, "decade", "Italy", "domestic", "cultural",
        "Platina's De honesta voluptate (1470) based on chef Martino's recipes. Democratized culinary knowledge restricted to elite. Reprinted in French, German, Italian",
        "Printing technology + educated middle-class households",
        2, 3, 2, 3, 3, 4, 1, 0, "serendipitous", "strong")

    insert_event(print_id, "Printed Maps and Atlases", "印刷地図と地図帳",
        1475, 1600, "quarter_century", "Europe", "education", "cultural",
        "Ptolemy's Geographia (1475+), Ortelius (1570), Mercator (1595). Expanded geographical understanding. Public houses displayed wall maps creating geographic discussion spaces",
        "Classical text revival + exploration data + printing mass distribution",
        4, 3, 4, 3, 3, 4, 3, 0, "serendipitous", "strong")

    insert_event(print_id, "Printed Botanical Illustrations and Herbals", "印刷植物画と本草書",
        1485, 1550, "decade", "Europe", "healthcare", "cultural",
        "Woodblock botanical illustrations revolutionized medical knowledge. Leonhart Fuchs commissioned naturalistic illustrations. Made herbal/medicinal knowledge accessible to households",
        "Medical knowledge democratization + accurate scientific illustration",
        3, 2, 3, 2, 4, 3, 2, 0, "serendipitous", "strong")

    insert_event(print_id, "Culpeper's English Vernacular Medicine", "カルペッパーの英語俗語医学",
        1653, 1750, "exact", "England", "healthcare", "social",
        "Culpeper translated Latin Pharmacopoeia into English, added affordable herbal formulas. Broke physician monopoly on medical knowledge. Enabled self-diagnosis for common people",
        "Intentional democratization of medical knowledge + affordable printing",
        1, 3, 4, 2, 5, 3, 1, 1, "linear", "strong")

    insert_event(print_id, "Broadside Ballads Popular Poetry", "ブロードサイド・バラッド民衆詩",
        1520, 1850, "quarter_century", "Britain/Ireland", "artistic", "aesthetic",
        "Penny single-sheet prints sold in streets. 400,000+ annually by 1660s. Brought contemporary news, moral instruction, entertainment to working/rural populations",
        "Cheap printing + itinerant merchant distribution",
        4, 4, 2, 3, 2, 4, 0, 0, "grassroots", "strong")

    insert_event(print_id, "Chapbooks Popular Literature", "チャップブック民衆文学",
        1500, 1800, "quarter_century", "Europe", "culture", "cultural",
        "Small cheap booklets by itinerant peddlers carrying folklore, children's stories, ballads. Preserved oral traditions in written form. Reached populations excluded from formal book culture",
        "Cheap small editions + existing merchant networks",
        3, 3, 3, 3, 2, 4, 0, 0, "grassroots", "strong")

    insert_event(print_id, "Brothers Grimm Illustrated Fairy Tales", "グリム兄弟挿絵付き童話",
        1812, 1850, "exact", "Germany", "culture", "aesthetic",
        "Grimm brothers published Kinder- und Hausmarchen (1812). 1825 small edition with Ludwig Grimm illustrations for children. Transformed oral tradition into standardized printed form, directly shaped childhood imagination",
        "Romantic nationalism + affordable illustrated printing",
        5, 5, 4, 4, 3, 5, 1, 0, "linear", "strong")

    insert_event(print_id, "Women Writers and Professional Authorship", "女性作家と職業的著述",
        1650, 1800, "quarter_century", "England/Europe", "culture", "social",
        "Aphra Behn (1640-1689) first woman to earn living entirely from writing. By 18th century women novelists dominated popular fiction. New genres reflecting female experience",
        "Printing enabling text dissemination + emerging middle-class audience",
        3, 4, 4, 3, 5, 4, 2, 0, "grassroots", "strong")

    insert_event(print_id, "Japanese Ukiyo-e Woodblock Prints", "浮世絵木版画",
        1615, 1868, "decade", "Japan", "artistic", "aesthetic",
        "Pictures of floating world produced in thousands. Inexpensive prints brought fine art to ordinary people: kabuki actors, landscapes, daily life. 1765 full-color innovation. Profoundly influenced Western aesthetics (Japonism)",
        "Woodblock tradition + commercial demand + color printing innovation",
        5, 4, 3, 3, 3, 5, 1, 0, "serendipitous", "strong")

    insert_event(print_id, "Korean Movable Type and Hangul", "朝鮮金属活字とハングル",
        1234, 1500, "quarter_century", "Korea", "education", "social",
        "Korean movable metal type (c.1234) preceded Gutenberg by two centuries. Hangul alphabet (1443) by King Sejong combined with type to democratize literacy. Enabled women's education and popular literature",
        "Metal casting innovation + deliberate royal literacy policy",
        2, 3, 4, 3, 5, 5, 1, 1, "linear", "strong")

    insert_event(print_id, "Ottoman Printing Restriction", "オスマン帝国の印刷制限",
        1485, 1727, "decade", "Ottoman Empire", "political", "political",
        "250-year restriction on Arabic-script printing prevented knowledge democratization. Maintained elite manuscript monopoly. Created knowledge asymmetry with Europe. Illustrates censorship preventing QoL benefits",
        "Religious scholars' resistance + scribe economic interests + elite aesthetic preference",
        -3, -2, -4, -2, -4, -3, -3, 0, "resistance", "strong")

    insert_event(print_id, "Hebrew Printing and Jewish Literacy", "ヘブライ語印刷とユダヤ人識字",
        1514, 1600, "decade", "Eastern Europe", "spiritual", "spiritual",
        "Hebrew presses in Prague (1514), Krakow (1530), Lublin (1534) made Torah and prayer texts accessible. Mass production enabled active religious participation. 1577 Yiddish women's guide reached underserved",
        "Printing technology + desire to democratize religious participation",
        2, 3, 5, 4, 4, 5, 0, 0, "grassroots", "strong")

    insert_event(print_id, "Vesalius Anatomical Illustration", "ウェサリウスの解剖学図譜",
        1543, 1600, "exact", "Europe", "healthcare", "aesthetic",
        "De Humani Corporis Fabrica (1543) with 200+ meticulously crafted woodcuts from Titian's workshop. Revolutionized anatomical understanding and set unprecedented standards for scientific accuracy and aesthetic merit",
        "Printing technology + artistic skill + direct anatomical observation",
        4, 2, 4, 2, 3, 3, 2, 0, "serendipitous", "strong")

    insert_event(print_id, "English Almanacs Popular Knowledge", "英国暦暦と民衆知識",
        1500, 1800, "quarter_century", "England", "education", "cultural",
        "Second most distributed literature after Bible. 400,000 copies/year by 17th century. Astrological predictions, medical advice, agricultural guidance, moral commentary for people who read little else",
        "Cheap production + audience demand for practical/predictive knowledge",
        2, 2, 3, 2, 3, 3, 1, 0, "grassroots", "strong")

    insert_event(print_id, "Women's Spiritual Literature", "女性宗教文学の印刷",
        1550, 1700, "quarter_century", "Catholic Europe", "spiritual", "spiritual",
        "Printing enabled publication of women mystics' spiritual writings. Spanish mystics' introspective narratives. In 17th-c Lima women gained theological understanding through reading. New spaces for female intellectual/spiritual authority",
        "Counter-Reformation + printing mass distribution",
        2, 4, 5, 3, 4, 4, 0, 0, "serendipitous", "moderate")

    insert_event(print_id, "Conduct Books and Social Behavior", "作法書と社会的行動",
        1485, 1750, "quarter_century", "Europe", "social", "social",
        "Castiglione's Il Cortegiano (1528) and hundreds of conduct books standardized social behavior guidance. Reached women, youth, servants. Allowed aspiring individuals to imagine improved social status",
        "Printing enabling rapid dissemination + audience desire for social advancement",
        1, 2, 2, 2, 3, 3, 1, 0, "serendipitous", "strong")

    insert_event(print_id, "Information Overload and Misinformation", "情報過多と誤情報",
        1500, 1600, "quarter_century", "Europe", "social", "mixed",
        "Sudden proliferation created information overload and challenges in source reliability. False information spread as easily as accurate knowledge. Required development of critical thinking and media literacy",
        "Printing technology's capacity for rapid mass production",
        -2, -1, -1, -1, -2, -1, 0, 0, "serendipitous", "moderate")

    conn.commit()

    # Report
    total = cur.execute("SELECT COUNT(*) FROM usage_events").fetchone()[0]
    by_gpt = cur.execute("""
        SELECT g.name, COUNT(*) FROM usage_events e
        JOIN gpt_technologies g ON e.gpt_id = g.id
        GROUP BY g.name ORDER BY COUNT(*) DESC
    """).fetchall()
    by_quad = cur.execute("""
        SELECT quadrant, COUNT(*) FROM usage_events GROUP BY quadrant ORDER BY quadrant
    """).fetchall()

    print(f"\nDB2 batch 2 complete. Total events: {total}")
    print("\nBy GPT:")
    for r in by_gpt:
        print(f"  {r[0]}: {r[1]}")
    print("\nBy quadrant:")
    for r in by_quad:
        print(f"  Quadrant {r[0]}: {r[1]}")

    conn.close()


if __name__ == '__main__':
    seed()
