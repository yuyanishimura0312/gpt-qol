"""
Batch 3: DB2 automobile events — non-Western + modern era (30 events).
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'gpt_impact_genealogy.db')

def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()
    auto_id = cur.execute("SELECT id FROM gpt_technologies WHERE name='Automobile'").fetchone()[0]
    existing = set(r[0] for r in cur.execute("SELECT name FROM usage_events").fetchall())

    def ins(name, name_ja, ys, ye, yc, region, domain, etype, desc, trigger,
            sa, se, sm, sr, sau, sc, secon, intended, path_type, evidence):
        if name in existing: return
        cur.execute("""INSERT INTO usage_events
            (gpt_id,name,name_ja,year_start,year_end,year_confidence,region,domain,event_type,
             description,trigger_pattern,score_aesthetic,score_emotional,score_meaning,
             score_relational,score_autonomy,score_cultural,score_economic_macro,
             intended_by_inventor,adoption_path_type,evidence_strength)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (auto_id,name,name_ja,ys,ye,yc,region,domain,etype,desc,trigger,
             sa,se,sm,sr,sau,sc,secon,intended,path_type,evidence))
        existing.add(name)

    # Non-Western
    ins("Auto-Rickshaw Culture in India","インド・オートリクシャー文化",
        1960,None,"decade","India","urban","social",
        "Auto-rickshaws as dominant flexible micro-mobility in Indian cities, ~10% of motorized trips. Drivers construct urban belonging through deep place-based navigation knowledge",
        "Post-independence demand for affordable urban transport",
        1,2,3,3,2,2,2,0,"grassroots","strong")
    ins("Tata Nano People's Car","タタナノ庶民の車",
        2008,2019,"exact","India","commerce","cultural",
        "Revolutionary 'car for price of scooter' with 200K+ bookings. Paradox: cheapest car label prevented aspirational adoption. Revealed status hierarchies in emerging market automobile consumption",
        "Ratan Tata's democratization vision + two-wheeler competition",
        -1,3,4,-2,2,-1,1,1,"repurposed","strong")
    ins("Dekotora Decorated Trucks","デコトラ装飾トラック",
        1970,None,"decade","Japan","artistic","aesthetic",
        "Originated from salt-corrosion resistance on fishing trucks, evolved into $100K+ neon/mural/steel art installations. 1975 film 'Truck Guys' catalyzed nationwide phenomenon. Workers appropriating commercial tools as folk art",
        "Salt-water corrosion damage + Toei truck driver film popularity",
        5,4,4,3,4,4,2,0,"serendipitous","strong")
    ins("Kei Car Culture","軽自動車文化",
        1949,None,"exact","Japan","urban","cultural",
        "Post-war regulation (11.2ft, 660cc) created distinct automotive culture. 33% of new sales by 2023. Regulatory constraints became cultural assets: space efficiency as urban sophistication",
        "Post-WWII resource scarcity + congested urban environments",
        2,1,2,1,3,3,3,0,"grassroots","strong")
    ins("Matatu Decorated Minibuses","ケニア・マタトゥ装飾ミニバス",
        1980,None,"decade","Kenya","artistic","cultural",
        "Hip-hop influenced urban youth expression on minibuses carrying 70%+ of Nairobi commuters. $2,000+ custom murals with global icons. Colonial vehicle inheritance indigenized as grassroots aesthetic",
        "Hip-hop cultural influence + rapid urbanization + commuting demand",
        4,3,3,3,3,4,1,0,"hybridization","strong")
    ins("Jeepney as Philippine National Symbol","フィリピン・ジープニー国家シンボル",
        1945,None,"exact","Philippines","culture","cultural",
        "Surplus US military vehicles transformed into extended passenger vehicles serving 40M daily trips. 1964 World's Fair exhibit. Anime/Bollywood/religious decorated galleries. Colonial legacy indigenized as national pride",
        "Post-WWII surplus vehicles + destroyed local transit + tropical adaptation",
        3,4,5,4,3,5,2,0,"hybridization","strong")
    ins("Saudi Tafheet Drifting Culture","サウジアラビア・タフヒート漂流文化",
        1978,None,"decade","Saudi Arabia","leisure","cultural",
        "High-speed highway performative spectacle by youth at 100-160mph. In country restricting public expression, cars provided rare space for identity-making and implicit resistance. Government response: sanctioned racing academies",
        "Oil boom suburban sprawl + wide highways + cultural restrictions on public behavior",
        2,4,3,3,4,2,0,0,"resistance","strong")
    ins("Thai Tuk-Tuk Cultural Identity","タイ・トゥクトゥク文化的アイデンティティ",
        1948,None,"exact","Thailand","culture","cultural",
        "Adapted from Italian Piaggio Ape, became Bangkok's icon. Drivers as unofficial tour guides. Transition from two-stroke→LPG→electric (600+ EVs via MuvMi 2024) preserves cultural significance while modernizing",
        "Italian vehicle availability + rapid 1960s urbanization + climate concerns",
        3,4,4,4,2,5,1,0,"hybridization","strong")
    ins("China Bicycle-to-Car Transition","中国自転車から自動車への転換",
        2001,None,"exact","China","urban","social",
        "Beijing bicycle mode share collapsed from 65%(1986) to 15%(2015) after WTO entry. State media framed as 'entry into car society'. Bicycles devalued from proletarian pride. Eroded spatial knowledge and social encounter",
        "WTO membership + auto industry government support + urban sprawl",
        -2,-1,-2,-2,-1,-2,2,1,"linear","strong")
    ins("West African Bush Taxi System","西アフリカ・ブッシュタクシー",
        1950,None,"decade","West Africa","rural","social",
        "Share-taxis (sept place, taxi brousse) constitute nearly 100% of rural motor transport. Ancient Peugeots depart when full, arrive 'whenever'. Grassroots solution to infrastructure deficit enabling cross-border commerce",
        "Post-colonial infrastructure gaps + high vehicle costs + rural dispersal",
        -1,1,2,3,1,1,2,0,"grassroots","strong")
    ins("Colombian Chiva Buses","コロンビア・チバス農村バス",
        1908,None,"exact","Colombia","culture","aesthetic",
        "Painted rural buses with flag colors, arabesques, religious imagery. Lifelines connecting remote Andean communities to healthcare/education/commerce. Artisanal woodworking traditions on imported chassis",
        "Difficult Andean terrain + imported chassis + artisanal traditions",
        4,3,4,4,2,4,1,0,"appropriation","strong")
    ins("Indian Truck Art Tradition","インド・トラック美術伝統",
        1920,None,"decade","India","artistic","aesthetic",
        "Folk art adapted onto commercial vehicles since 1920s colonial era. Drivers decorated trucks to remind of home during months-long separations. Kaleidoscopic patterns, religious icons, Bollywood imagery, philosophical slogans",
        "British colonial vehicle import + long-haul driver isolation + folk art traditions",
        4,3,3,2,3,4,0,0,"hybridization","strong")
    ins("Itasha Anime-Wrapped Cars","イタシャ・アニメラッピング車",
        2005,None,"exact","Japan","artistic","aesthetic",
        "Vehicle decoration with large-scale anime/manga imagery. Dedicated conventions (Autosalone 2007+). Variants: itansha(motorcycles), itachari(bicycles), itabasu(buses). Otaku identity expression via vehicular appropriation",
        "Anime globalization via internet + fan convention infrastructure + vehicle wrap technology",
        4,4,3,3,4,3,1,0,"serendipitous","strong")
    ins("Mexico City Pesero Colectivo","メキシコシティ・ペセロ",
        1970,None,"decade","Mexico","urban","social",
        "One-peso VW microbuses evolved to carry 12 passengers on flexible routes. 28,000 peseros carrying 60% of passengers by 2007. Cholo aesthetics, cumbia imagery, custom lighting. Informalized transit with door-open accessibility",
        "Metro capacity insufficiency + economic crisis + informal labor",
        3,2,2,3,3,3,1,0,"grassroots","strong")
    ins("Gulf States Exotic Car Culture","湾岸諸国エキゾチックカー文化",
        1990,None,"decade","Gulf States","leisure","cultural",
        "In oil-wealthy GCC nations, exotic cars as primary status signifiers. Dubai ~5% luxury vehicle concentration. Car meets as elite social gatherings. Conspicuous consumption as essential social practice",
        "Oil wealth concentration + Islamic restrictions on public leisure + car as privatizable luxury",
        1,2,2,1,1,2,4,1,"linear","strong")
    ins("Cuba Vintage American Cars Heritage","キューバ・ヴィンテージ車遺産",
        1962,None,"exact","Cuba","culture","cultural",
        "1962 embargo froze ~60,000 pre-revolution American classics as family heirlooms. Coffee-filter carburetors, 'Fordyotas' from salvaged parts. Antiquated vehicles acquired heritage status through isolation and creative reuse",
        "US trade embargo + restricted imports + tropical climate corrosion",
        3,4,5,4,2,4,2,0,"serendipitous","strong")
    ins("Didi Ride-Hailing China","中国ディディ配車サービス",
        2012,None,"exact","China","commerce","social",
        "Captured 80% of private ride-hailing by 2015. Broke language barriers and taxi fare conflicts. Created gig jobs but income instability. Highly educated workers forced into low-skill roles",
        "Beijing traffic congestion + language barriers + mobile-first population",
        -1,2,1,-1,2,-1,-1,1,"linear","strong")

    # Modern era
    ins("GPS Navigation and Spatial Cognition Decline","GPS航法と空間認知低下",
        2000,None,"exact","Global","other","mixed",
        "Dose-dependent negative correlation between GPS use and hippocampal spatial memory. Users show steeper decline in cognitive mapping and landmark encoding. Replaces spatial memory with stimulus-response",
        "Smartphone GPS ubiquity post-2007 + declining route memorization",
        -2,-1,-2,-1,-2,-2,1,0,"serendipitous","strong")
    ins("Ride-Sharing Car-Free Lifestyle","ライドシェアカーフリーライフスタイル",
        2009,None,"exact","USA","urban","social",
        "6-9% of Uber/Lyft users would have purchased cars without service. Enables car-free living for urban/affluent/young. But overall VMT and emissions increased—substitution vs induced demand paradox",
        "Smartphone ubiquity + GPS infrastructure + gig economy regulatory arbitrage",
        1,2,1,1,2,1,1,1,"linear","strong")
    ins("Electric Vehicle Acoustic Transformation","電動車両の音響変容",
        2010,None,"exact","Global","other","mixed",
        "EVs eliminate engine noise (WHO: second health harm after air pollution), reducing insomnia/depression/CVD. But pedestrian collision 2.1x higher. Mandated AVAS reintroduce artificial sounds—quietness creates new risks",
        "EV adoption surge + safety research on pedestrian risks",
        2,2,1,-1,-1,1,0,1,"serendipitous","strong")
    ins("Car-Sharing Access Over Ownership","カーシェアリング所有から利用へ",
        2000,None,"exact","USA/Europe","commerce","social",
        "Zipcar etc repositioned consumption from ownership to access. 500K vehicles unsold/not purchased by members 2024. 'Cool, trendy, green' framing. But ownership still more valued culturally",
        "2008 recession + urbanization + smartphone allocation systems",
        -1,1,1,1,1,-1,1,1,"linear","strong")
    ins("Autonomous Vehicles for Elderly/Disabled","自動運転車の高齢者・障害者向け",
        2015,None,"exact","USA","healthcare","social",
        "Pilot programs (goMARTI, Detroit) deploy ADA-compliant shuttles with $13M+ investment. Multimodal interfaces (voice/gesture/haptic). But 6M Americans currently lack needed transportation and older adults remain skeptical",
        "Aging population + disability rights advocacy + autonomous technology advances",
        -1,1,3,2,3,0,0,1,"linear","strong")
    ins("Dashcam Culture and Surveillance","ドライブレコーダー文化と監視",
        2010,None,"exact","Global","other","mixed",
        "Continuous recording devices for accident documentation. But capture pedestrians without consent, manufacturers create commercial maps from footage. Every vehicle becomes a data collection point",
        "Smartphone video ubiquity + liability documentation needs + commercial mapping demand",
        -3,-2,-1,-2,-3,-2,1,1,"serendipitous","strong")
    ins("Vanlife Movement","バンライフムーブメント",
        2011,None,"exact","USA","leisure","cultural",
        "Instagram-filtered aspirational freedom from career constraints. COVID-19 supercharged adoption (remote work). But deflated: new campers dropped 40%→16% (2022-2024). Material contradictions limit sustainability",
        "2008 recession recovery + social media aestheticization + COVID remote work + housing costs",
        2,3,2,0,3,1,0,0,"serendipitous","strong")
    ins("Podcast Commuting Culture","ポッドキャスト通勤文化",
        2006,None,"exact","Global","culture","cultural",
        "Podcast awareness 22%→79% (2006-2022). Commuting as primary consumption context transforms dead time into education/entertainment. Cars become 'auto-edification' classrooms on wheels",
        "Podcast ecosystem + smartphone audio + long commute times",
        0,2,1,0,1,1,1,0,"serendipitous","moderate")
    ins("Ride-Hailing Gender Safety Features","配車サービスのジェンダー安全機能",
        2019,None,"exact","Global","social","social",
        "170-6,160 sexual assaults in rideshares (2012-2015). 40% women prefer female drivers. Uber Women Preferences in 40 countries, 100M+ trips. Technological response to gendered safety anxieties",
        "Sexual assault prevalence + #MeToo movement + platform safety competition",
        0,2,2,1,2,1,0,1,"linear","strong")
    ins("China Bicycle-to-EV Sharing Revival","中国自転車→電動シェア復活",
        2015,None,"exact","China","urban","social",
        "After automobile dominance (2001-2015), Chinese cities launched bike-sharing to reverse car culture. Rare 'reversal' pattern: conscious deprioritization of automobiles after recognizing congestion/emission costs",
        "Urban pollution/congestion costs + climate policy + e-bike technology",
        1,1,2,1,1,2,1,1,"resistance","moderate")
    ins("TikTok/Instagram Car Influencer Aesthetics","TikTok/Instagram自動車インフルエンサー美学",
        2016,None,"exact","Global","artistic","cultural",
        "Social media created new automobile aestheticization through customization showcases. Young demographics consume cars through visual media rather than ownership. Image acquires market value independent of use-value",
        "Social media platform growth + algorithmic recommendation + creator economy",
        3,2,0,0,0,1,1,0,"serendipitous","moderate")
    ins("India Women Automotive Manufacturing","インド自動車産業の女性製造労働力",
        2010,None,"exact","India","labor","social",
        "Tata Motors 6,500+ female technicians, Hero MotoCorp 3,500. Advanced manufacturing requires precision over brute strength. Tata Kaushalya trained 20,000+ students (21% women). Gender labor division reconfigured by technology",
        "Advanced manufacturing adoption + skill shortages + gender diversity initiatives",
        0,1,2,2,2,1,2,1,"linear","strong")
    ins("Car Dependency Infrastructure Lock-in","自動車依存インフラロックイン",
        1956,None,"exact","USA","urban","political",
        "1956 Federal-Aid Highway Act authorized 40,000 miles of interstate. 91% households own 1+ car, 75% commuters drive alone, 45% have no transit. Path dependency through infrastructure, zoning, and cultural narratives",
        "Post-WWII suburban development + military-industrial advocacy + oil industry influence",
        -2,2,1,-2,1,1,2,1,"linear","strong")

    conn.commit()
    total = cur.execute("SELECT COUNT(*) FROM usage_events").fetchone()[0]
    by_gpt = cur.execute("""SELECT g.name, COUNT(*) FROM usage_events e
        JOIN gpt_technologies g ON e.gpt_id=g.id GROUP BY g.name ORDER BY COUNT(*) DESC""").fetchall()
    print(f"DB2 auto batch 3 complete. Total events: {total}")
    for r in by_gpt: print(f"  {r[0]}: {r[1]}")
    by_q = cur.execute("SELECT quadrant, COUNT(*) FROM usage_events GROUP BY quadrant ORDER BY quadrant").fetchall()
    print("Quadrants:")
    for r in by_q: print(f"  {r[0]}: {r[1]}")
    conn.close()

if __name__ == '__main__':
    seed()
