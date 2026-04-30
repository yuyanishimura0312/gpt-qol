"""
Batch 3: DB2 printing press events (23) + adoption paths (25).
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
    existing_events = set(r[0] for r in cur.execute("SELECT name FROM usage_events"))
    existing_paths = set(r[0] for r in cur.execute("SELECT path_name FROM adoption_paths"))

    def ins_event(gpt, name, name_ja, ys, ye, yc, region, domain, etype, desc, trigger,
                  sa, se, sm, sr, sau, sc, secon, intended, path_type, evidence):
        if name in existing_events: return
        cur.execute("""INSERT INTO usage_events
            (gpt_id,name,name_ja,year_start,year_end,year_confidence,region,domain,event_type,
             description,trigger_pattern,score_aesthetic,score_emotional,score_meaning,
             score_relational,score_autonomy,score_cultural,score_economic_macro,
             intended_by_inventor,adoption_path_type,evidence_strength)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (gpt_ids[gpt],name,name_ja,ys,ye,yc,region,domain,etype,desc,trigger,
             sa,se,sm,sr,sau,sc,secon,intended,path_type,evidence))
        existing_events.add(name)

    def ins_path(gpt, path_name, path_name_ja, desc, intended, actual, pivot_year, trigger, qol_summary, path_type):
        if path_name in existing_paths: return
        cur.execute("""INSERT OR IGNORE INTO adoption_paths
            (gpt_id, path_name, path_name_ja, path_description,
             intended_use, actual_use, pivot_year, pivot_trigger,
             qol_impact_summary, path_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (gpt_ids[gpt], path_name, path_name_ja, desc, intended, actual,
             pivot_year, trigger, qol_summary, path_type))
        existing_paths.add(path_name)

    # ============================================================
    # PRINTING PRESS — Non-European + 19th-20th century + Quadrant II
    # ============================================================
    P = "Printing Press"
    ins_event(P,"Bengali Renaissance Print Culture","ベンガルルネサンス印刷文化",
        1842,1920,"decade","India","culture","cultural",
        "Literary magazines (Tattvabodhini Patrika 1842, Bangadarshan) published Tagore et al. Created new Bengali prose forms, spread nationalist and humanist thought beyond elite",
        "British colonial printing infrastructure + Bengali intellectual revival",
        5,4,5,3,4,5,1,0,"grassroots","strong")
    ins_event(P,"Bulaq Press and Arab Nahda","ブラク印刷所とアラブナフダ",
        1822,1890,"exact","Egypt/Arab world","education","cultural",
        "Muhammad Ali Pasha's government press (1822) published 243+ titles by 1842. Translated European science/literature into Arabic, catalyzed nahda (Arab Renaissance) without Western intermediaries",
        "State modernization policy + desire for scientific knowledge",
        3,3,5,3,4,4,2,1,"linear","strong")
    ins_event(P,"Meiji Mass Publishing and Manga Origins","明治期大量出版と漫画の起源",
        1868,1912,"decade","Japan","artistic","aesthetic",
        "Western letterpress transformed 1870s-1880s publishing. Woodblock+type hybrid experiments. Edo ukiyo-e transitioned to commercial manga via print. Created entirely new art form merging traditions",
        "Meiji modernization + Western printing technology import + ukiyo-e tradition",
        5,5,4,4,5,5,2,0,"hybridization","strong")
    ins_event(P,"Commercial Press Shanghai and May Fourth","上海商務印書館と五四運動",
        1900,1930,"decade","China","education","cultural",
        "Commercial Press published vernacular Chinese (baihua) textbooks during May Fourth Movement (1919). Workers actively participated in demonstrations. Literary modernization from classical wenyan to modern baihua",
        "Nationalist intellectual awakening + modern education demand",
        4,4,5,3,5,4,1,0,"grassroots","strong")
    ins_event(P,"Missionary Presses and African Language Literacy","宣教師印刷所とアフリカ言語識字",
        1820,1920,"decade","Africa","education","social",
        "Christian missionaries established presses for Bible translation, creating written standards for previously oral-only languages. First newspapers and textbooks in African languages. Paradox: colonial tool yet liberation technology",
        "Evangelization + need for vernacular texts + colonial infrastructure",
        2,2,4,3,3,4,1,0,"serendipitous","strong")
    ins_event(P,"Korean Hangul Independence Newspaper","韓国ハングル独立新聞",
        1896,1910,"exact","Korea","political","political",
        "Tongnip sinmun (1896) was first Korean newspaper published entirely in Hangul (not classical Chinese). Founded by Seo Jae-pil for grassroots enlightenment. Established Hangul as vehicle for modern journalism",
        "Reformist politics + belief in grassroots over elite reform",
        3,3,5,4,5,5,0,0,"grassroots","strong")
    ins_event(P,"Penguin Paperback Revolution","ペンギン・ペーパーバック革命",
        1935,1960,"exact","UK/Global","culture","cultural",
        "Allen Lane's Penguin Books at 6 pence (1/15 of hardcover price). First 10 titles sold 3M copies in year one. Sold at Woolworth's and station kiosks. Democratized quality literature to working class",
        "Vision of affordable literature + non-traditional distribution channels",
        4,4,5,4,4,4,4,1,"grassroots","strong")
    ins_event(P,"American Dime Novels","アメリカ・ダイムノベル",
        1860,1920,"decade","USA","leisure","cultural",
        "Beadle's dime novels: ~50,000 titles on cheap wood-pulp paper. Western, mystery, adventure, SF at 1-5 cents. First serialized fiction market creating cross-class leisure reading",
        "Cheap wood-pulp paper + newsstand distribution + mass literacy",
        3,4,3,2,3,3,1,0,"grassroots","strong")
    ins_event(P,"Comic Books as Art Form","コミックブックの芸術化",
        1938,1970,"exact","USA","artistic","aesthetic",
        "Superman (Action Comics #1, 1938) launched comics as distinct medium. Color printing innovations enabled affordable sequential art. Underground comix (1960s-70s) reflected countercultural values",
        "Printing color innovations + youth culture demand + artistic ambition",
        4,4,3,3,3,4,2,0,"serendipitous","strong")
    ins_event(P,"Underground Press Movement","アンダーグラウンドプレス運動",
        1966,1975,"exact","USA","political","cultural",
        "Underground Press Syndicate grew from 15 (1966) to 271 papers (1971). Offset lithography enabled $300-400 startup. Experimental layouts, excluded themes. Parallel information ecosystem during Vietnam era",
        "Affordable offset printing + anti-war movement + countercultural energy",
        5,5,5,5,5,4,-1,0,"resistance","strong")
    ins_event(P,"Zine Culture and DIY Publishing","ジン文化とDIY出版",
        1976,2000,"decade","USA/Global","culture","cultural",
        "Punk zines (1970-80s), Riot Grrrl feminist zines (1990s), queer zine explosion during AIDS crisis. Photocopy and low-cost printing. Protest, preservation, horizontal knowledge sharing outside commercial publishing",
        "Photocopy technology + punk DIY ethic + marginalized community needs",
        5,5,5,5,5,5,-2,0,"resistance","strong")
    ins_event(P,"Braille Printing and Blind Literacy","点字印刷と視覚障害者識字",
        1825,1932,"exact","France/Global","education","social",
        "Louis Braille's six-dot system (1824-25) enabled independent reading/writing for blind. 'Braille Wars' (1829-1932) standardized competing systems. Mass-produced accessible literature transformed blind literacy",
        "Braille's innovation + institutional adoption + standardization",
        2,4,5,3,5,4,-1,1,"linear","strong")
    ins_event(P,"Samizdat Soviet Underground Publishing","サミズダート・ソビエト地下出版",
        1960,1989,"decade","Soviet Union","political","spiritual",
        "Hand-typed carbon-copy manuscripts circulating banned literature (Solzhenitsyn, Sakharov). Each reader became publisher by retyping. Spiritual/intellectual resistance to state censorship. Preserved cultural memory",
        "State censorship + intellectual resistance + carbon copy technology",
        2,5,5,4,5,5,-2,0,"resistance","strong")
    ins_event(P,"Illustrated Newspapers Visual Journalism","挿絵新聞と視覚ジャーナリズム",
        1842,1900,"exact","UK/USA","communication","aesthetic",
        "Illustrated London News (1842) and Harper's Weekly (1857) pioneered wood-engraved images alongside type. Sketches hand-carved by multiple engravers in 2-inch sections. Photography gradually replaced woodcuts",
        "Relief printing compatibility with type + public demand for visual news",
        4,3,2,2,2,3,3,0,"serendipitous","strong")
    ins_event(P,"Children's Picture Books","児童向け絵本の発展",
        1658,1920,"quarter_century","Europe","education","aesthetic",
        "First picture book Orbis Sensualium Pictus (1658, 150 illustrations). Edmund Evans' 1860s color printing created 'toy books'. 20th-c psychologists established scientific basis for picture books as developmental tools",
        "Educational theory + color printing innovation + child development science",
        5,4,4,3,3,4,1,0,"serendipitous","strong")
    ins_event(P,"Greeting Cards and Emotional Expression","グリーティングカードと感情表現",
        1910,1950,"exact","USA","social","social",
        "Hallmark (1910) moved from postcards to folded cards with envelopes (1913) for privacy. Pre-printed sentiments democratized emotional expression as hand-letter writing declined. New social rituals around printed emotion",
        "Industrialization reducing letter-writing leisure + demand for emotional communication",
        3,5,2,5,2,3,2,0,"serendipitous","strong")
    ins_event(P,"Wallpaper Printing and Domestic Aesthetics","壁紙印刷と家庭美学",
        1700,1880,"quarter_century","UK/Europe","domestic","aesthetic",
        "Woodblock improvements enabled multicolor wallpaper. Roller printing (1839) produced 400 rolls/day. UK: 1M rolls (1830) to 50M (1900). Transformed wallpaper from luxury to everyday domestic aesthetic accessible across classes",
        "Printing technology improvements + middle-class expansion + fashion diffusion",
        4,2,1,1,2,3,2,0,"grassroots","strong")
    ins_event(P,"Women's Magazines and Identity","女性雑誌とアイデンティティ",
        1828,1970,"decade","USA","culture","social",
        "Sarah Josepha Hale (1828) first US women's magazine editor. Ladies' Home Journal defined femininity through consumer culture. Helen Gurley Brown's Cosmopolitan (1965) covered premarital sex/careers. 1970 feminist sit-in at LHJ",
        "Women's literacy + advertising industry + feminist movement",
        3,4,3,3,4,4,3,0,"serendipitous","strong")
    ins_event(P,"Scientific Journal Peer Review System","科学雑誌ピアレビューシステム",
        1665,1960,"quarter_century","Europe/Global","scientific","cultural",
        "Peer review formalized post-WWII (term appeared 1960s only). Created as gatekeeping for scarce print/distribution resources. Became foundation for scientific credibility, quality control, institutional authority",
        "Print resource scarcity + need for quality control + institutional knowledge production",
        1,1,4,3,2,3,3,0,"serendipitous","strong")

    # ============================================================
    # ADOPTION PATHS (across all GPTs)
    # ============================================================
    ins_path("Automobile","Car Radio Mobile Entertainment","カーラジオ移動娯楽化",
        "Car radios from optional accessory to primary news/music/education delivery system during commute",
        "Optional vehicle accessory for driver entertainment",
        "Primary news source, music distribution platform, educational programming for commuters. 40%→90% adoption 1946-1970s",
        1950,"Transistor invention (1947) + FM expansion + suburban commuting culture",
        "Quadrant I: enabled knowledge access during transit, reduced solo driver isolation","creative_misuse")
    ins_path("Automobile","Parking Lot Tailgating Culture","駐車場テイルゲーティング文化",
        "Parking areas designed for vehicle storage became spontaneous community gathering spaces",
        "Efficient vehicle storage adjacent to venues",
        "Pre/post-game social bonding, barbecuing, commerce in asphalt lots. Democratic gathering independent of admission fees",
        1975,"Suburban stadium construction with vast parking + no transit alternatives + high concession costs",
        "Quadrant II: informal community spaces strengthening bonds across strangers","grassroots")
    ins_path("Automobile","Food Truck Mobile Cuisine","フードトラック移動料理",
        "Car trunk/van transformed from cargo space to mobile restaurant kitchen",
        "Vehicle cargo storage for goods transport",
        "Gourmet mobile cuisine, culinary entrepreneurship with minimal startup costs, food culture democratization",
        2008,"2008 recession forcing chefs to low-overhead models + social media enabling location sharing",
        "Quadrant I: culinary innovation + entrepreneurship + food access in underserved areas","creative_misuse")
    ins_path("Automobile","EV Acoustic Environment Transformation","EV音響環境変容",
        "Electric propulsion eliminated engine noise, transforming urban acoustic environment",
        "Efficient zero-emission transportation",
        "Urban quietness (reducing health impacts of noise), but pedestrian collision 2.1x higher requiring artificial sound systems",
        2015,"EV adoption surge + WHO noise pollution health data + pedestrian safety research",
        "Quadrant II: health benefits from noise reduction, but safety tradeoffs require new solutions","serendipity")
    ins_path("Telephone","Phone Camera Citizen Journalism","携帯カメラ市民ジャーナリズム",
        "Camera integrated into phone became tool for documenting injustice and news events",
        "Personal photography convenience feature",
        "Citizen journalism, police accountability (George Floyd 2020), democratized visual documentation",
        2005,"Camera phone ubiquity + social media sharing platforms + civil rights movements",
        "Quadrant I: accountability and transparency + new profession of citizen journalist","repurpose")
    ins_path("Telephone","SMS New Linguistic Forms","SMS新言語形態",
        "Text messaging character limits forced linguistic innovation, creating new written forms",
        "Efficient short business communication",
        "New abbreviations (LOL, BRB), emoji as universal pictographic language, Japanese mobile novels (keitai shosetsu)",
        1999,"160-character SMS limit + teen adoption + need for speed in communication",
        "Quadrant II: linguistic creativity, new literary forms, cross-cultural communication symbols","creative_misuse")
    ins_path("Telephone","Voicemail Emotional Archive","ボイスメール感情アーカイブ",
        "Voicemail messages preserved as emotional artifacts, especially of deceased loved ones",
        "Message recording for missed calls",
        "Preserved voices of deceased family members become cherished artifacts. Digital hoarding of voicemails as grief processing",
        1990,"Answering machine + digital voicemail persistence + loss/grief experience",
        "Quadrant II: emotional preservation and grief processing with no economic value","serendipity")
    ins_path("Telephone","Ringtone Personal Identity","着信音パーソナルアイデンティティ",
        "Phone ringtone selection became form of personal identity expression",
        "Audio alert for incoming calls",
        "Custom ringtones as self-expression ($4.4B global market 2004). Polyphonic→MP3→custom. Cultural identity signaling",
        2001,"Polyphonic ringtone technology + teen identity culture + mobile music downloads",
        "Quadrant I: personal identity expression + $4.4B market at peak","creative_misuse")
    ins_path("Telephone","Smartphone as Primary Computer","スマートフォンが主要コンピュータに",
        "Phone transformed from voice communication to primary computing device for billions in Global South",
        "Portable telephone for voice calls",
        "Internet access, banking, education, government services via smartphone for populations without PC access. Digital inclusion",
        2010,"Affordable Android smartphones + mobile data infrastructure + app ecosystems",
        "Quadrant I: digital inclusion for billions, but creates new digital dependencies","democratization")
    ins_path("Printing Press","Newspaper Want Ads Personal Connection","新聞案内広告パーソナル接続",
        "Commercial classified advertising section repurposed for personal connection and dating",
        "Revenue-generating commercial advertising space",
        "Personal ads for romantic connection, 'Lonely hearts' columns, pen pal networks. Predecessor to dating apps",
        1695,"Newspaper subscription model + human desire for connection + anonymity of print",
        "Quadrant II: personal connection for isolated individuals, economically marginal","repurpose")
    ins_path("Printing Press","Printed Wallpaper Domestic Aesthetics","印刷壁紙の家庭美学民主化",
        "Industrial printing wallpaper democratized domestic interior aesthetics",
        "Wall covering for practical protection",
        "Aesthetic self-expression through home decoration accessible to middle and working class. 1M→50M rolls/year UK 1830-1900",
        1750,"Roller printing technology + middle-class expansion + fashion diffusion from elite",
        "Quadrant I: aesthetic democratization + wallpaper industry growth","democratization")
    ins_path("Printing Press","Trading Cards Collecting Culture","トレーディングカード収集文化",
        "Commercial advertising inserts in cigarette packages became childhood collecting and imagination medium",
        "Cigarette package advertising stiffener",
        "Baseball cards, educational cards, fantasy cards. Childhood imagination, social bonding through trading, nostalgia",
        1886,"Cigarette packaging needs + lithographic color printing + children's collecting instinct",
        "Quadrant II: childhood imagination and social bonding, economically marginal for children","serendipity")
    ins_path("Printing Press","Menu Printing Restaurant Culture","メニュー印刷レストラン文化",
        "Printed menus transformed dining from communal table to individual choice",
        "Communication of available dishes to diners",
        "Individual dietary autonomy, food culture literacy, culinary tourism enabled by readable menus",
        1765,"Parisian restaurant emergence + printing affordability + individual dining concept",
        "Quadrant I: food culture democratization + restaurant industry foundation","democratization")
    ins_path("Electricity","Electric Lighting Nightclub Culture","電灯ナイトクラブ文化",
        "Electric lighting enabled controlled atmospheric environments for nighttime entertainment",
        "Practical illumination for safety and productivity",
        "Nightclub/dance culture, mood lighting, disco, rave culture. New aesthetic and social experiences in controlled darkness",
        1920,"Electric lighting control + urban entertainment demand + jazz/dance culture",
        "Quadrant II: new aesthetic/social experiences, economically marginal","creative_misuse")
    ins_path("Electricity","Refrigeration Dietary Revolution","冷蔵庫食生活革命",
        "Electric refrigeration transformed diet from seasonal/local to year-round global variety",
        "Industrial food preservation and transport",
        "Year-round fresh food access, dietary diversity, food safety improvement, changed cooking practices",
        1930,"Domestic refrigerator affordability + food supply chain + middle-class expansion",
        "Quadrant I: dietary diversity and health improvement + food industry growth","serendipity")
    ins_path("Electricity","Cinema Collective Dream Experience","映画館集団夢体験",
        "Electric projection created new collective aesthetic experience in darkened theaters",
        "Scientific demonstration of moving images",
        "Cinema as collective dream, new art form combining image/sound/narrative. Movie-going as social ritual",
        1910,"Projection technology + storytelling tradition + urban entertainment demand",
        "Quadrant I: new art form + massive entertainment industry","serendipity")
    ins_path("Electricity","Christmas Lights Seasonal Ritual","クリスマスライト季節儀式",
        "Electric Christmas tree lights created new domestic/civic seasonal ritual",
        "Practical illumination technology",
        "Seasonal decoration as family/community ritual. Neighborhood light displays as shared aesthetic experience. $6B+ annual market",
        1882,"Edison's associate Johnson first electric tree (1882) + GE marketing + suburban culture",
        "Quadrant I: seasonal emotional enrichment + decoration industry","serendipity")
    ins_path("Steam Engine","Railway Time Standardization","鉄道時間標準化",
        "Railway scheduling necessitated standardized time zones, replacing local solar time",
        "Efficient rail transport scheduling",
        "GMT adoption, time zone system. Standardized human temporal experience globally. Enabled coordination of modern life",
        1847,"Railway scheduling conflicts + telegraph enabling synchronization + commercial need",
        "Quadrant IV: efficiency gain but loss of local temporal autonomy and natural time rhythms","repurpose")
    ins_path("Steam Engine","Steamship Mass Emigration","蒸気船大量移民",
        "Steam-powered ocean crossing enabled mass emigration transforming global demographics",
        "Commercial maritime cargo transport",
        "Mass emigration (60M Europeans 1815-1930), diaspora communities, cultural cross-pollination, family separation and reunion",
        1840,"Steamship reliability + European push factors + New World pull factors",
        "Quadrant I: cultural diversity and opportunity + economic growth, but family separation trauma","repurpose")
    ins_path("Steam Engine","Factory Labor Movement","工場労働運動",
        "Factory system's concentration of workers enabled collective organizing and labor rights movement",
        "Efficient industrial production through worker concentration",
        "Trade unions, workers' rights, shorter work hours, child labor laws. Factory conditions created class consciousness",
        1830,"Worker concentration + harsh conditions + Enlightenment ideas of rights + literacy",
        "Quadrant II: workers' rights and dignity improvements, initially against economic interests","grassroots")

    conn.commit()

    total_events = cur.execute("SELECT COUNT(*) FROM usage_events").fetchone()[0]
    total_paths = cur.execute("SELECT COUNT(*) FROM adoption_paths").fetchone()[0]
    by_gpt = cur.execute("""SELECT g.name, COUNT(*) FROM usage_events e
        JOIN gpt_technologies g ON e.gpt_id=g.id GROUP BY g.name ORDER BY COUNT(*) DESC""").fetchall()
    by_q = cur.execute("SELECT quadrant, COUNT(*) FROM usage_events GROUP BY quadrant ORDER BY quadrant").fetchall()

    print(f"\nDB2 batch 3 (print+paths) complete.")
    print(f"Total events: {total_events}")
    for r in by_gpt: print(f"  {r[0]}: {r[1]}")
    print(f"\nTotal adoption paths: {total_paths}")
    print("\nQuadrants:")
    for r in by_q: print(f"  {r[0]}: {r[1]}")
    conn.close()

if __name__ == '__main__':
    seed()
