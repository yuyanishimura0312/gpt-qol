"""
Batch 4: DB2 telephone (35 events) + electricity (18 events) + steam engine (13 events).
"""
import sqlite3, os
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'gpt_impact_genealogy.db')

def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    cur = conn.cursor()
    gpt_ids = {r[1]:r[0] for r in cur.execute("SELECT id, name FROM gpt_technologies")}
    existing = set(r[0] for r in cur.execute("SELECT name FROM usage_events"))

    def ins(gpt, name, name_ja, ys, ye, yc, region, domain, etype, desc, trigger,
            sa, se, sm, sr, sau, sc, secon, intended, path_type, evidence):
        if name in existing: return
        cur.execute("""INSERT INTO usage_events (gpt_id,name,name_ja,year_start,year_end,year_confidence,
            region,domain,event_type,description,trigger_pattern,score_aesthetic,score_emotional,
            score_meaning,score_relational,score_autonomy,score_cultural,score_economic_macro,
            intended_by_inventor,adoption_path_type,evidence_strength) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (gpt_ids[gpt],name,name_ja,ys,ye,yc,region,domain,etype,desc,trigger,sa,se,sm,sr,sau,sc,secon,intended,path_type,evidence))
        existing.add(name)

    T,E,S = "Telephone","Electricity","Steam Engine"

    # TELEPHONE events
    ins(T,"SMS Language Emergence","SMS言語の出現",1993,None,"exact","Global","communication","cultural",
        "SMS textese (l8r, gr8, lol) adapted to 160-char limits. Distinct linguistic subculture among youth. Debates about literacy impacts while becoming identity expression",
        "160-char limit + expensive per-message charges + multi-tap keypads",2,2,3,3,2,3,2,0,"grassroots","strong")
    ins(T,"Nokia Developing World Democratization","ノキア発展途上国モバイル民主化",1998,2010,"exact","Africa/Asia","communication","social",
        "Affordable feature phones with LED flashlights, dust/water resistance. Local repair ecosystems. Made mobile accessible to billions without prior communication infrastructure",
        "Expanding market opportunity + cost reduction through modular manufacturing",1,2,4,4,4,2,5,1,"linear","strong")
    ins(T,"M-Pesa Mobile Banking","M-Pesa携帯金融サービス",2007,None,"exact","Kenya/East Africa","commerce","social",
        "Cash transfers via SMS without bank account. By 2021, 25M users transformed Kenya financial inclusion 26%→84%. Reduced crime in cash societies. Model spread across Africa/Asia",
        "Pilot research on unbanked populations + DFID funding + mobile carrier partnerships",0,2,5,3,5,3,5,1,"linear","strong")
    ins(T,"Japanese Keitai Culture","日本ケータイ文化",1997,2010,"exact","Japan","culture","aesthetic",
        "Mobile phones as intimate personal objects. Email over calls. i-mode (1999) mobile internet. Status symbols and aesthetic customization. Distinct keitai culture reshaping social protocols",
        "Japanese manufacturers' early internet integration + cultural emphasis on personalization",5,4,4,3,3,5,3,0,"serendipitous","strong")
    ins(T,"Emoji Invention and Global Adoption","絵文字の発明と世界的普及",1999,2011,"exact","Japan/Global","communication","aesthetic",
        "Kurita designed 176 emoji for i-mode (1999), inspired by manga. Apple added to iPhone 2009. By 2011 spread globally via Unicode. Fastest-adopted written language innovation in history",
        "Manga symbolic tradition + limited text display + Apple iPhone keyboard decision",5,5,4,4,2,5,2,0,"serendipitous","strong")
    ins(T,"Philippines Texting Capital","フィリピン世界一のテキスト大国",1999,2005,"exact","Philippines","communication","social",
        "1B+ SMS daily. Average Filipino 195 SMS/month vs 13 in USA. SMS enabled political mobilization: Estrada ouster (2001) involved millions of texts, volume jumping to 70M/day",
        "Poor fixed-line infrastructure + cheap SMS relative to voice",1,3,3,5,3,4,2,0,"grassroots","strong")
    ins(T,"India Missed Call Culture","インドミスコール文化",2001,None,"exact","India","communication","social",
        "Calling and hanging up as cost-free communication code. Each outgoing minute ~8 cents (roughly daily wage). 70% uptake in healthcare services via missed calls vs 30% toll-free",
        "Extremely high voice charges relative to income + accessibility for illiterate populations",1,2,3,4,5,2,4,0,"grassroots","strong")
    ins(T,"India Women Mobile Safety","インド女性モバイル安全機能",2012,None,"exact","India","social","political",
        "Mandated panic button on phones for women's safety. But women 18% of mobile subscribers despite 50% of population. 96% give male children smartphones before female siblings",
        "High harassment/assault rates + advocate pressure + recognition of mobile as safety prerequisite",0,1,5,2,3,1,1,1,"resistance","strong")
    ins(T,"WeChat Life Operating System","WeChat生活OS化",2011,None,"exact","China","communication","social",
        "From messaging to super-app: payments, mini-programs, e-commerce, government services. 1.385B MAU. WeChat Pay 4T RMB (74% of mobile payment). Phone prerequisite for Chinese society participation",
        "Tencent's mini-program architecture + government pandemic health code integration",2,3,5,5,-2,3,5,1,"linear","strong")
    ins(T,"Smartphone Primary Internet Global South","グローバルサウスのスマホ唯一のネット接続",2010,None,"exact","Global South","communication","social",
        "90% of internet users in developing economies access exclusively via smartphone. Phone prerequisite for social media, learning, government services, jobs. 84% own mobile, but smartphone varies 33-80%",
        "High cost of fixed broadband + no viable alternatives + smartphone price reductions",0,1,5,3,4,2,5,1,"linear","strong")
    ins(T,"QR Code Contactless Culture","QRコード非接触社会",2020,None,"exact","Japan/China/Global","commerce","social",
        "COVID catalyzed QR adoption for menus, payments, contact tracing. China standardized QR health codes integrating vaccination/infection status. Phones as mediators of biological and social control",
        "COVID contact fear + existing QR infrastructure in Asia + government tracking need",0,0,2,1,-3,1,3,1,"serendipitous","strong")
    ins(T,"Smartphone Photography Visual Culture","スマートフォン写真と視覚文化変容",2007,None,"exact","Global","artistic","aesthetic",
        "Sharp J-SH04 (2000) first camera phone. iPhone 2G (2007) mass-market. Instagram (2010) institutionalized smartphone photography. Time between seeing and sharing collapses. Smartphone as extension of eye and memory",
        "Moore's Law camera miniaturization + Instagram frictionless sharing",5,3,3,4,4,4,2,0,"serendipitous","strong")
    ins(T,"Tinder Mobile Dating Transformation","Tinder時代の出会い変容",2012,None,"exact","Global","social","social",
        "1.6B daily swipes, 50M users. 30% of US adults use dating apps (up from 11% 2013). Both positive (30% more likely to form relationships) and negative (loss/gain cycles, humiliation) psychological effects",
        "Smartphone ubiquity + app store ecosystem + camera quality enabling profile curation",2,-1,1,1,3,1,2,1,"linear","strong")
    ins(T,"Ringtone Culture and Personalization","着メロ文化と個性化",1998,2010,"exact","Global","culture","aesthetic",
        "$600M US market by 2006. Polyphonic→MP3 evolution. Ringtone as personal signature, as expressive as shoes. Industry collapsed 2010s with smartphone notifications but represented era of playful personalization",
        "Nokia 2110 monophonic→polyphonic + carrier revenue diversification + identity desire",4,2,2,1,3,2,3,1,"linear","strong")
    ins(T,"Voice Assistants Daily Companions","音声アシスタント日常のコンパニオン",2011,None,"exact","Global","domestic","social",
        "Siri (2011), Alexa (2014). 8.4B digital assistants by 2024. Children perceive as trustworthy entities. Elderly/disabled report increased autonomy. Parents concerned about child-device attachment",
        "NLP advances + machine learning + smartphone integration + smart speaker hardware",0,2,2,2,3,1,2,0,"linear","moderate")
    ins(T,"Nomophobia Phone Addiction","ノモフォビア（携帯恐怖症）",2008,None,"exact","Global","social","social",
        "77% of teens anxious without phones. 40-70% suffer some addiction. Symptoms: trembling, perspiration, tachycardia. Phone as extension of self; separation triggers withdrawal-like symptoms",
        "Rising phone ubiquity + dependence for connection/identity + behavioral reinforcement loops in app design",0,-5,1,-2,-3,-2,1,0,"serendipitous","moderate")
    ins(T,"WhatsApp Family Group Dynamics","WhatsAppファミリーグループ",2009,None,"exact","Global","social","social",
        "Strengthened intergenerational bonds but also amplified tensions. Grandparents often become group administrators establishing new authority structures. Reliance on digital replaces meaningful face-to-face",
        "WhatsApp group feature + smartphone normalization + pandemic isolation",0,2,2,3,1,2,0,0,"serendipitous","moderate")
    ins(T,"Keitai Shosetsu Mobile Novels","携帯小説ブーム",2003,2010,"exact","Japan","artistic","aesthetic",
        "First mobile novel 'Deep Love' (2003) became 2.6M-copy bestseller. By 2007 half of Japan's bestsellers were mobile-authored. $240M market. 70-100 word chapters capturing teen texting rhythm",
        "Keitai culture maturation + mobile email prevalence among youth + publisher recognition",3,4,3,2,4,4,3,0,"grassroots","strong")
    ins(T,"TikTok Youth Creative Expression","TikTok短編動画文化",2018,None,"exact","Global","artistic","cultural",
        "User-generated 3-60 second videos democratizing video production. Lip-sync, dance, DIY, comedy, educational tutorials. Platform for youth activism. Enhanced self-expression and peer connection",
        "5G capability + algorithmic recommendation + smartphone camera maturity + ByteDance ML",4,3,2,4,3,4,2,0,"linear","strong")
    ins(T,"Podcasting Democratization","ポッドキャスト民主化",2005,None,"exact","Global","culture","cultural",
        "Anyone with microphone + smartphone becomes creator. Lowers barriers for marginalized voices. Billions of listeners by 2024. Diverse voices from academia, activism, comedy, journalism",
        "Smartphone audio + reliable broadband + open RSS standards + COVID isolation",0,3,4,3,5,4,2,0,"grassroots","strong")
    ins(T,"Phone Camera Citizen Journalism","スマホカメラ市民ジャーナリズム",2007,None,"exact","Global","political","political",
        "Citizen camera-witnessing: documenting police violence, political repression. Arab Spring, BLM videos as evidence and mobilization tools. Speed advantage over DSLRs. Distributed accountability networks",
        "Smartphone ubiquity + social media platforms + civil rights movements",1,4,5,4,4,3,0,0,"grassroots","strong")
    ins(T,"Arab Spring Social Media Mobilization","アラブの春スマートフォン動員",2010,2012,"exact","MENA","political","political",
        "85% of Egyptians/86% Tunisians used social media to organize. Facebook event pages for Tahrir Square. SMS enabled coordination. Anyone with smartphone becomes witness/documentarian",
        "Government repression + smartphone ubiquity + youth unemployment + political grievances",0,4,5,5,4,3,0,0,"grassroots","strong")
    ins(T,"Korea PC Bang to Mobile Gaming","韓国PC部屋からモバイルゲームへ",1998,2020,"exact","South Korea","leisure","cultural",
        "PC bangs peaked 21,549 locations (2009). 84.2% of Korean gamers enjoy mobile vs 54.2% PC (2020s). COVID accelerated transition. PC bangs survive as esports arenas and social third spaces",
        "Mobile game sophistication + smartphone ubiquity + COVID + 5G rollout",1,2,1,2,3,2,1,0,"serendipitous","strong")
    ins(T,"Latin America WhatsApp Business","ラテンアメリカWhatsAppビジネス",2009,None,"exact","Latin America","commerce","social",
        "87% of companies use WhatsApp. 80% of Mexican consumers prefer it for business. 72% have purchased via messaging. WhatsApp as de facto business infrastructure replacing email and SMS",
        "High mobile penetration + poor fixed broadband + cultural preference for personal communication",0,1,3,3,2,2,4,1,"linear","strong")
    ins(T,"Voicemail as Emotional Archive","ボイスメール感情的記録",1980,None,"decade","Global","domestic","social",
        "Voicemail evolves to emotional archive. Users preserve deceased loved ones' voices. Hearing voice after death offers 'enduring presence transcending mortality'. PostSecret project collects thousands",
        "Recording permanence + grief/loss + voice as irreplaceable identity marker",1,5,5,5,2,3,0,0,"serendipitous","moderate")
    ins(T,"Conference Calling Remote Work Origins","電話会議リモートワーク起源",1915,None,"exact","USA/Global","labor","social",
        "Bell's first conference call 1915 (NY-SF mayors + President Wilson). Picturephone 1964. Skype 2010, Zoom 2011. COVID catalyzed hybrid/remote adoption. Conference calling now dominant work mode",
        "Long-distance business needs + switching infrastructure + COVID lockdowns",0,1,3,2,3,1,3,1,"linear","strong")
    ins(T,"Japan Fax Machine Business Culture","日本ファックスビジネス文化",1980,2000,"decade","Japan","commerce","cultural",
        "Japan dominated global fax market 1980s-90s. Cultural embedding creates path dependency: 'reliable traditional method' for legal documents. Persists in 2025 despite technological obsolescence. Tangibility and formality values",
        "G3 standards + Japanese manufacturing + cultural preference for paper + institutional inertia",2,2,3,1,0,3,2,1,"linear","strong")
    ins(T,"Indigenous Mobile Phone Adaptation","先住民モバイル電話適応",2005,None,"exact","Global","social","cultural",
        "Indigenous communities adopt phones for language preservation (texting in indigenous languages), family connection. M-Pesa impacts Maasai. Cultural tensions between customs and technology. iCow for livestock management",
        "Geographic isolation + family dispersal + language preservation potential",0,2,3,4,2,-1,2,0,"repurposed","moderate")
    ins(T,"Instagram Visual Consumption Culture","Instagramビジュアル消費文化",2010,None,"exact","Global","artistic","aesthetic",
        "Filters and editing enable aesthetic curation. Algorithmic feed drives endless scroll. Mental health impacts: appearance comparison, performative identity. Photographers' professional disruption",
        "Smartphone camera + Instagram frictionless sharing + algorithmic engagement maximization",4,-1,1,2,2,2,3,1,"linear","strong")
    ins(T,"Mobile Payment Proliferation","モバイル決済普及",2007,None,"exact","Global","commerce","social",
        "M-Pesa (2007), Alipay QR (2010s), Apple Pay (2014). Smartphones as wallets. Unbanked gain financial inclusion. But transaction trails create unprecedented financial visibility",
        "Smartphone ubiquity + NFC standardization + QR adoption + fintech investment",0,1,3,1,-1,1,5,1,"linear","strong")
    ins(T,"Gender Digital Divide Crystallization","デジタルジェンダー格差構造化",1995,None,"decade","Global","social","political",
        "India: women 18% of mobile subscribers. Male children get smartphones first (96%). Patriarchal gatekeeping constrains women's digital autonomy. Phone as contested technology enabling and surveilling women",
        "Patriarchal resource control + safety concerns justifying restriction + gendered labor",0,-2,2,-1,-3,-2,1,0,"serendipitous","strong")
    ins(T,"Mobile Learning in Development","発展途上国モバイル学習",2010,None,"exact","Global South","education","social",
        "SMS agricultural extension, WhatsApp teacher-student coordination, YouTube vocational training. COVID: phones as primary learning device where schools closed. Limitations: small screens, battery, data",
        "Limited education infrastructure + economic constraints + pandemic school closures",0,1,4,2,3,2,3,1,"linear","moderate")
    ins(T,"Smartphone as Health Device","スマートフォンヘルスケア",2008,None,"exact","Global","healthcare","social",
        "Health apps, telemedicine, wearable integration, melanoma detection via camera, medication reminders. In developing countries: eye exams via camera, missed-call maternal health (70% uptake in rural India)",
        "Smartphone sensor proliferation + health data market + telemedicine normalization post-COVID",0,1,4,1,0,1,3,1,"linear","moderate")
    ins(T,"Algorithmic Attention Economy","アルゴリズム注意力経済",2012,None,"exact","Global","culture","social",
        "Social media algorithms optimize for engagement, commodifying human consciousness. Notification systems engineer behavioral loops. Adolescent mental health correlates with algorithmic social comparison",
        "ML capability + VC engagement optimization + mobile-first + behavioral psychology in UX",0,-3,-1,-1,-4,-2,4,0,"serendipitous","strong")

    # ELECTRICITY events
    ins(E,"Home Refrigeration Revolution","家庭冷蔵庫革命",1927,None,"exact","USA","domestic","social",
        "GE Monitor-Top (1927). By 1940 50%+ of households had refrigerators. Freon reduced costs $275→$154. Expanded dietary diversity and eliminated seasonal food dependence",
        "Freon innovation + New Deal financing + middle-class affordability",2,3,2,2,3,2,2,1,"linear","strong")
    ins(E,"Electric Washing Machine Liberation","電動洗濯機と家事解放",1904,None,"exact","USA","domestic","social",
        "By 1940 60% of electrified homes (25M) had washing machines. Reduced physical strain 8→4 hours/week. But raised standards consumed freed time. Enabled workforce participation despite unchanged total housework",
        "Electrical safety mechanisms + spin-dryer technology + cultural normalization",1,2,1,2,2,1,2,0,"linear","strong")
    ins(E,"Electric Iron Domestic Efficiency","電動アイロンと家事効率化",1904,None,"exact","USA","domestic","social",
        "Ironing time 4.5→1.75 hours per 38-pound load. Temperature control eliminated scorching. Physical burden of heated cast-iron irons on stovetops completely eliminated",
        "Thermostat controls + widespread home electrification 1910s-1920s",1,2,1,1,2,0,1,1,"linear","strong")
    ins(E,"Gramophone Home Entertainment","蓄音機家庭音楽文化",1900,None,"exact","USA/Europe","leisure","cultural",
        "Production surged 190K (1923) to 5M (1929). Victor designed machines as aesthetic cabinets. Jazz/blues fueled 'gramomania'. Evening entertainment centered on record listening with friends",
        "Victor's cabinet design innovation + affordable discs + jazz/blues explosion",4,3,3,3,2,3,2,1,"linear","strong")
    ins(E,"Cinema Electric Projection","映画と電気映写技術",1895,None,"exact","Global","artistic","aesthetic",
        "Lumière Brothers (1895). By 1939: 85M weekly attendees (2/3 of US population). Working-class first collective aesthetic encounter with moving images. New art form emerged",
        "Incandescent projection + improved frame rates 1920s + urban middle class with leisure",5,4,3,3,2,4,2,1,"serendipitous","strong")
    ins(E,"Television as Family Hearth","テレビが家庭の中心に",1950,None,"exact","USA/Europe","domestic","cultural",
        "TV replaced fireplace as spatial center of living rooms. Families gathered after dinner for shared programs. Unified American culture through identical nationwide broadcasts",
        "Post-WWII affluence + improved picture quality + mass-appeal programming",2,3,2,3,0,2,2,1,"linear","strong")
    ins(E,"Electric Elevator Skyscraper City","電動エレベーターと垂直都市",1880,None,"exact","USA/Europe","urban","social",
        "Siemens patent (1880), Sprague traction (1887), Otis first electric elevator NYC (1889). Manhattan density doubled 1880-1910 to 113,881/sq mi. Created new vertical property markets",
        "Electromechanical innovations + structural steel + urban land scarcity",3,2,2,2,1,2,3,1,"linear","strong")
    ins(E,"Neon Signs Urban Nightscape","ネオン照明と都市夜景",1910,None,"exact","Global","artistic","aesthetic",
        "Georges Claude invented neon (1910). Times Square became iconic. Film noir appropriated neon shadows. Poets celebrated 'electric poetry'. Urban night became designed, intentional aesthetic space",
        "Claude's engineering + economic boom enabling advertising + urbanization",5,4,3,2,1,4,2,1,"linear","strong")
    ins(E,"Air Conditioning Sunbelt Migration","エアコンとサンベルト人口移動",1930,None,"decade","USA","domestic","social",
        "Affordable window units (1950s) triggered dramatic migration reversal. 100M+ people relocated to Sunbelt regions for work and comfort. Fundamentally restructured American geography",
        "1950s window AC affordability + industrial productivity + post-WWII expansion",2,2,2,1,2,1,3,0,"serendipitous","strong")
    ins(E,"Electric Fan Summer Comfort","電動扇風機と夏季快適",1902,None,"exact","USA","domestic","social",
        "By 1930 ~6M electric fans in homes. Maintained temperatures 4F cooler. Extended leisure seasons and reduced heat-related mortality in urban tenements",
        "Standardized AC electrical system + manufacturing scale + heat-mortality awareness",1,2,1,1,2,1,1,1,"linear","moderate")
    ins(E,"Christmas Electric Lights","クリスマス電飾と季節儀式",1920,None,"decade","USA","domestic","cultural",
        "Affordable by 1920s. Denver 'Christmas Capital'. By 1930s replaced dangerous wax candles. By 1940s (rural electrification) Christmas transformed from candlelit intimacy to electric spectacle",
        "Industrialization reducing bulb costs + residential electrification + consumer culture",4,4,4,2,1,3,1,1,"linear","strong")
    ins(E,"Rural Electrification REA","農村電化局プログラム",1935,1955,"exact","USA","rural","social",
        "Roosevelt's REA (1935). By 1938: 1.5M farms. By 1955: nearly all. Pumped water, indoor toilets, electric light. Women's burden shifted from hauling water to appliance operation",
        "New Deal policy + cooperative cost-sharing + distribution system maturity",2,3,3,2,2,2,3,1,"grassroots","strong")
    ins(E,"Electric Streetcar Suburbs","電気路面電車と郊外",1887,None,"exact","USA","urban","social",
        "Sprague's Richmond streetcar (1887). Track 5,783 mi (1890) to 34,404 (1907). Five-cent flat fares enabled suburban commute. Mixed-use neighborhoods along lines",
        "Sprague motor innovation + municipal franchises + residential land availability",2,2,2,2,2,1,3,1,"linear","strong")
    ins(E,"Electric Telegraph News Revolution","電信とニュース速度革新",1844,None,"exact","Global","communication","social",
        "Morse's telegraph (1844). Before: news at transportation speed (days-weeks). After: instantly. US Midwest news lag from Washington fell 7 days. By 1866 transatlantic cable connected continents",
        "Morse-Vail innovation + submarine cable technology + business demand for price information",1,2,3,3,1,3,3,1,"linear","strong")
    ins(E,"Hospital Electrification","病院電化と医療水準向上",1890,None,"decade","Global","healthcare","social",
        "Edison's bulb replaced dangerous gas lamps in operating theaters. Electric surgery lamps (1920s). Electric stimulation treated paralyzed muscles. Heated incisors enabled simultaneous cutting/cauterization",
        "Edison's bulb reliability + germ theory + surgical specialization requiring precision",0,3,3,3,2,1,2,1,"linear","strong")
    ins(E,"Factory Electric Lighting","工場電化と労働条件",1890,None,"decade","USA/UK","labor","economic",
        "Extended factory hours, improved visibility. Productivity 1.2%/yr (1899-1919) → 3.5%/yr (1919-1937). Hawthorne Studies: worker attention, not just light levels, drove productivity",
        "Electrical distribution standardization + competitive pressures + factory safety advocacy",0,1,1,1,-1,0,3,1,"linear","strong")
    ins(E,"Electric Hair Dryer Beauty Culture","ヘアドライヤーと美容文化",1920,None,"decade","USA","culture","cultural",
        "Handheld dryers (1920s) $10-25. Bob hairstyles and shorter cuts enabled by quick drying. Beauty salon culture flourished as female sociability and entrepreneurship site. Drying hours→minutes",
        "Home electrification + flapper culture shorter hairstyles + salon expansion",3,2,2,2,2,3,2,1,"linear","moderate")
    ins(E,"Electric Heating Residential Comfort","電動暖房と住宅快適性",1912,None,"exact","USA","domestic","social",
        "Thermostat-controlled automatic heating (1912). Gas (1927), oil (1930s-40s). Constant temperature eliminated dangerous swings. Women no longer tended furnaces. Heating became invisible reliable utility",
        "Thermostat innovation + fuel diversification + residential electrification",0,2,1,1,1,0,1,1,"linear","moderate")

    # STEAM ENGINE events
    ins(S,"Railway Time Standardization","鉄道による標準時間採用",1840,1880,"decade","UK/USA","political","social",
        "GWR adopted London time (1840). Most UK railways standardized GMT by 1847. US railways unified Nov 18, 1883. Human rhythm detached from sun/seasons, synchronized to clock discipline",
        "Railway scheduling necessity + telegraph speed + imperial coordination demands",0,-2,-1,2,-2,-2,2,1,"linear","strong")
    ins(S,"Steam Printing Press Mass Newspapers","蒸気印刷機と大量新聞",1814,None,"exact","Global","communication","cultural",
        "Koenig's press (1814): 1,100 pages/hr vs 300. Hoe's rotary (1843): 8,000/hr. Affordable daily newspapers enabled working-class political participation and cultural awareness",
        "Steam efficiency + urban literacy expansion + mercantile information demand",1,2,3,3,1,3,3,1,"linear","strong")
    ins(S,"Steamship Mass Emigration","蒸気船と大量移民",1850,1920,"decade","Atlantic","social","social",
        "Atlantic crossing: 38.8 days (sail)→14.9 (steam). 1880-1914: 20M Europeans to USA. Steam enabled temporary labor migration vs permanent settlement. Diaspora formation and transnational family networks",
        "Steam cost reduction + industrial labor demand + European poverty/upheaval",0,1,2,2,0,2,3,0,"serendipitous","strong")
    ins(S,"Factory Worker Alienation","蒸気工場と労働疎外",1780,None,"decade","UK/USA/Europe","labor","social",
        "Marx/Engels: workers as 'living appendages of machinery'. Four alienations: from product, activity, human nature, other workers. Women/children at 1/3 wages. Motivated labor organization and socialist movements",
        "Steam scalability + competitive pressures + capital accumulation + labor scarcity strategies",-3,-3,-2,-2,-3,-2,3,0,"linear","strong")
    ins(S,"Coal Mining Communities","石炭採掘コミュニティ文化",1750,None,"quarter_century","UK/Germany/USA","labor","social",
        "Underground work forged intense solidarity despite dangerous conditions. Brass bands, choirs, union halls. Strict gender division. From 1880s miners became most militant industrial workers globally",
        "Steam engine demand + isolated geography + dangerous conditions motivating collective action",1,2,3,3,0,3,0,0,"grassroots","strong")
    ins(S,"Textile Mill Child Labor","紡織工場と児童女性労働",1770,None,"decade","UK/USA","labor","social",
        "50% of 1818-19 Manchester workers began under age 10. 20,000 pauper apprentices (1800). 12+ hour days. Women at 1/3 wages. 1802 Act limited child hours to 12/day. Created wealth concentration while destroying worker bodies",
        "Steam scalability + labor scarcity via children/women + profit maximization",-4,-4,-2,-2,-4,-3,3,0,"linear","strong")
    ins(S,"Railway Station Public Architecture","ヴィクトリア朝駅舎と公共空間",1840,None,"decade","UK/USA","urban","aesthetic",
        "Monumental buildings: Bristol Temple Meads (Tudor), Euston Station neo-classical. Frith's 1862 painting depicted all classes mingling. Stations as civic identity and social mixing across class boundaries",
        "Railway expansion + architectural competition + imperial pride + urban growth",4,2,2,2,1,2,2,1,"linear","strong")
    ins(S,"Railway Psychology of Speed","鉄道速度とヴィクトリア朝心理変化",1830,None,"decade","UK/USA","culture","cultural",
        "NYC-Chicago: 2 days vs weeks by stagecoach. 'Railway madness' as alleged psychiatric condition. By journey's end Victorians internalized unprecedented velocity as normal—profound consciousness shift",
        "Unprecedented speed experience + absence of prior human motion exceeding horse pace",2,-1,2,1,0,3,2,0,"serendipitous","strong")
    ins(S,"Great Exhibition 1851","万博1851年と技術の見世物化",1851,None,"exact","UK","culture","aesthetic",
        "100,000 exhibits in Crystal Palace (1,851ft). 6M visitors (1/3 British population). 'Shilling days' democratized access. Profits funded V&A, Science, Natural History Museums. Technology-as-civic-pride blueprint",
        "Industrial confidence + imperial competition + urban leisure + scientific institution ambitions",4,3,3,3,1,4,2,1,"linear","strong")
    ins(S,"Railway Seaside Excursions","鉄道遠足と海辺レジャー",1840,None,"decade","UK","leisure","cultural",
        "Rail made coasts accessible day-trips. Bank Holidays Act (1871) designated 4 holidays/year. Seaside villages→resort towns. Deckchairs, ice cream, Punch & Judy, amusement arcades. Working-class leisure democratized",
        "Workday shortening + wage increases + rail cost reduction + seaside infrastructure",3,3,3,2,2,3,2,0,"grassroots","strong")
    ins(S,"Turner Rain Steam Speed","ターナー『雨、蒸気、速度』と鉄道美学",1844,None,"exact","UK","artistic","aesthetic",
        "1844 painting of GWR—masterwork of dynamic composition. Hare futilely outrunning locomotive: nature's powerlessness vs industrial modernity. Captured ambivalence: awe + anxiety about nature's displacement",
        "Railway symbolic dominance + Turner's mastery + Romantic-to-Modern artistic transition",5,3,4,1,-1,4,0,1,"serendipitous","strong")
    ins(S,"Canal Displacement by Railways","鉄道による運河の衰退",1840,1870,"decade","UK/USA","commerce","economic",
        "From 1840 rail networks displaced canal traffic. By 1850s cargo fell two-thirds. Speed decisive: 2 days NYC-Chicago vs weeks via canal. Massive infrastructure investments became stranded assets",
        "Steam locomotive speed/reliability + capital mobility + competitive market dynamics",0,0,-1,0,1,0,2,0,"linear","strong")
    ins(S,"Steam Threshing Agricultural Mechanization","蒸気脱穀機と農業機械化",1860,None,"decade","USA/UK","rural","social",
        "Pre-mechanization: flails consuming 1/4 of agricultural work. 'Threshing Day' became Iowa farm ritual congregating 30+ men. Eliminated drudgery but displaced laborers, generating ambivalent responses",
        "Steam scalability + grain production expansion + agricultural commercialization",0,1,1,1,1,0,2,0,"linear","moderate")

    conn.commit()

    total = cur.execute("SELECT COUNT(*) FROM usage_events").fetchone()[0]
    by_gpt = cur.execute("""SELECT g.name, COUNT(*) FROM usage_events e
        JOIN gpt_technologies g ON e.gpt_id=g.id GROUP BY g.name ORDER BY COUNT(*) DESC""").fetchall()
    by_q = cur.execute("SELECT quadrant, COUNT(*) FROM usage_events GROUP BY quadrant ORDER BY quadrant").fetchall()
    print(f"\nDB2 batch 4 complete. Total events: {total}")
    for r in by_gpt: print(f"  {r[0]}: {r[1]}")
    print("Quadrants:")
    for r in by_q: print(f"  {r[0]}: {r[1]}")
    conn.close()

if __name__ == '__main__':
    seed()
