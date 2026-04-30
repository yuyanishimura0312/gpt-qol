"""
Bulk import pipe-separated event data from /tmp files into DB2.
Handles format variations across different agent outputs.
"""
import sqlite3
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'gpt_impact_genealogy.db')

VALID_DOMAINS = {'transportation','communication','culture','education','leisure','domestic',
    'commerce','social','spiritual','artistic','political','healthcare','labor','urban',
    'rural','military','scientific','other'}

VALID_TYPES = {'economic','cultural','social','aesthetic','spiritual','political',
    'technological','mixed'}

VALID_PATHS = {'linear','serendipitous','repurposed','grassroots','resistance',
    'appropriation','hybridization'}

def normalize_domain(raw):
    raw = raw.strip().lower().split('/')[0].split(',')[0].strip()
    mapping = {
        'manufacturing': 'labor', 'infrastructure': 'urban', 'engineering': 'urban',
        'policy': 'political', 'wage': 'labor', 'worker': 'labor', 'activism': 'political',
        'system': 'commerce', 'comfort': 'domestic', 'cognitive': 'other',
        'behavioral': 'social', 'psychological': 'social', 'entertainment': 'leisure',
        'finance': 'commerce', 'safety': 'social', 'gender': 'social',
        'environmental': 'other', 'heritage': 'culture', 'linguistic': 'culture',
        'aesthetic': 'artistic', 'personal': 'domestic', 'romantic': 'social',
        'creative': 'artistic', 'media': 'communication', 'archival': 'culture',
        'development': 'social', 'medical': 'healthcare', 'journalistic': 'communication',
        'technology': 'commerce', 'gaming': 'leisure', 'emotional': 'social',
    }
    if raw in VALID_DOMAINS:
        return raw
    return mapping.get(raw, 'other')

def normalize_type(raw):
    raw = raw.strip().lower().split('/')[0].split(',')[0].strip()
    mapping = {
        'technological': 'technological', 'economic': 'economic', 'cultural': 'cultural',
        'social': 'social', 'aesthetic': 'aesthetic', 'spiritual': 'spiritual',
        'political': 'political', 'mixed': 'mixed',
        'labor': 'social', 'linguistic': 'cultural', 'psychological': 'social',
        'system innovation': 'technological', 'wage policy': 'economic',
        'worker experience': 'social', 'labor activism': 'political',
        'intellectual leadership': 'cultural', 'engineering standard': 'technological',
        'policy adoption': 'political', 'national project': 'political',
        'urban connection': 'economic', 'modernization': 'technological',
    }
    if raw in VALID_TYPES:
        return raw
    for k, v in mapping.items():
        if k in raw:
            return v
    return 'mixed'

def normalize_path(raw):
    raw = raw.strip().lower()
    if raw in VALID_PATHS:
        return raw
    mapping = {
        'creative_misuse': 'appropriation', 'creative misuse': 'appropriation',
        'democratization': 'grassroots', 'political': 'resistance',
        'technological': 'linear', 'institution': 'linear',
    }
    for k, v in mapping.items():
        if k in raw:
            return v
    return 'serendipitous'

def parse_score(raw):
    raw = str(raw).strip()
    # Remove common prefixes
    raw = re.sub(r'^(aesthetic|emotional|meaning|relational|autonomy|cultural|economic)[=:]?\s*', '', raw, flags=re.I)
    try:
        val = int(float(raw))
        return max(-5, min(5, val))
    except:
        return 0

def parse_intended(raw):
    raw = str(raw).strip().lower()
    if raw in ('1', 'yes', 'true', 'y'):
        return 1
    return 0

def parse_year(raw):
    raw = str(raw).strip().lower()
    if raw in ('null', 'none', '', 'present', 'ongoing', 'n/a'):
        return None
    try:
        return int(float(raw))
    except:
        return None

def parse_evidence(raw):
    raw = str(raw).strip().lower()
    if 'strong' in raw:
        return 'strong'
    elif 'moderate' in raw:
        return 'moderate'
    elif 'suggestive' in raw:
        return 'suggestive'
    return 'moderate'


def import_file(filepath, gpt_name, conn, existing):
    cur = conn.cursor()
    gpt_id = cur.execute("SELECT id FROM gpt_technologies WHERE name=?", (gpt_name,)).fetchone()
    if not gpt_id:
        print(f"GPT '{gpt_name}' not found!")
        return 0
    gpt_id = gpt_id[0]

    imported = 0
    skipped = 0
    errors = 0

    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#') or '|' not in line:
                continue

            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 18:
                errors += 1
                continue

            try:
                name = parts[0][:200]
                if name in existing:
                    skipped += 1
                    continue

                name_ja = parts[1][:200] if len(parts) > 1 else ''
                year_start = parse_year(parts[2])
                year_end = parse_year(parts[3])

                # year_confidence
                yc_raw = str(parts[4]).strip().lower() if len(parts) > 4 else 'decade'
                yc_map = {'5': 'exact', '4': 'decade', '3': 'quarter_century', '2': 'century', '1': 'estimated',
                          'exact': 'exact', 'decade': 'decade', 'quarter_century': 'quarter_century',
                          'century': 'century', 'estimated': 'estimated'}
                year_confidence = yc_map.get(yc_raw, 'decade')

                region = parts[5][:100] if len(parts) > 5 else 'Global'
                domain = normalize_domain(parts[6]) if len(parts) > 6 else 'other'
                event_type = normalize_type(parts[7]) if len(parts) > 7 else 'mixed'
                description = parts[8][:1000] if len(parts) > 8 else ''
                trigger = parts[9][:500] if len(parts) > 9 else ''

                sa = parse_score(parts[10]) if len(parts) > 10 else 0
                se = parse_score(parts[11]) if len(parts) > 11 else 0
                sm = parse_score(parts[12]) if len(parts) > 12 else 0
                sr = parse_score(parts[13]) if len(parts) > 13 else 0
                sau = parse_score(parts[14]) if len(parts) > 14 else 0
                sc = parse_score(parts[15]) if len(parts) > 15 else 0
                secon = parse_score(parts[16]) if len(parts) > 16 else 0
                intended = parse_intended(parts[17]) if len(parts) > 17 else 0
                path_type = normalize_path(parts[18]) if len(parts) > 18 else 'serendipitous'
                evidence = parse_evidence(parts[19]) if len(parts) > 19 else 'moderate'

                cur.execute("""INSERT INTO usage_events
                    (gpt_id,name,name_ja,year_start,year_end,year_confidence,
                     region,domain,event_type,description,trigger_pattern,
                     score_aesthetic,score_emotional,score_meaning,
                     score_relational,score_autonomy,score_cultural,
                     score_economic_macro,intended_by_inventor,
                     adoption_path_type,evidence_strength)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (gpt_id, name, name_ja, year_start, year_end, year_confidence,
                     region, domain, event_type, description, trigger,
                     sa, se, sm, sr, sau, sc, secon, intended, path_type, evidence))
                existing.add(name)
                imported += 1

            except Exception as e:
                errors += 1
                if errors <= 3:
                    print(f"  Error line {line_num}: {e}")
                    print(f"  Data: {parts[:3]}")

    return imported


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    existing = set(r[0] for r in conn.execute("SELECT name FROM usage_events"))

    files = [
        ('/tmp/auto_events.txt', 'Automobile'),
        ('/tmp/automobile_gpt_events.txt', 'Automobile'),
        ('/tmp/automobile_events.txt', 'Automobile'),
        ('/tmp/automobile_social_dynamics.txt', 'Automobile'),
        ('/tmp/printing_press_gpt_events.txt', 'Printing Press'),
        ('/tmp/printing_press_qol_events.txt', 'Printing Press'),
        ('/tmp/steam_engine_events.txt', 'Steam Engine'),
        ('/tmp/automobile_events_final.txt', 'Automobile'),
        # Electricity agent output (inline pipe data)
        ('/tmp/electricity_events.txt', 'Electricity'),
        ('/tmp/telephone_events.txt', 'Telephone'),
        ('/tmp/auto_global.txt', 'Automobile'),
        ('/tmp/auto_daily.txt', 'Automobile'),
        ('/tmp/auto_safety_ev.txt', 'Automobile'),
        ('/tmp/auto_racing_events.txt', 'Automobile'),
        ('/tmp/electricity_final_80.txt', 'Electricity'),
        ('/tmp/auto_final_300.txt', 'Automobile'),
        # Round 3: 1000-target expansion
        ('/tmp/tel_batch_a.txt', 'Telephone'),
        ('/tmp/tel_batch_b.txt', 'Telephone'),
        ('/tmp/elec_batch_a.txt', 'Electricity'),
        ('/tmp/elec_batch_b.txt', 'Electricity'),
        ('/tmp/steam_batch_a.txt', 'Steam Engine'),
        ('/tmp/steam_batch_b.txt', 'Steam Engine'),
        ('/tmp/print_batch_a.txt', 'Printing Press'),
        ('/tmp/print_batch_b.txt', 'Printing Press'),
        # Round 4: Auto 10K
        ('/tmp/auto_10k_a.txt', 'Automobile'),
        ('/tmp/auto_10k_b.txt', 'Automobile'),
        ('/tmp/auto_10k_c.txt', 'Automobile'),
        ('/tmp/auto_10k_d.txt', 'Automobile'),
        ('/tmp/auto_10k_e.txt', 'Automobile'),
        ('/tmp/steam_final.txt', 'Steam Engine'),
    ]

    # Also try to extract pipe data from electricity agent output
    elec_output = '/private/tmp/claude-502/-Users-nishimura-/ea9d1e4e-0230-40fc-89a2-328b16fe582d/tasks/a7c4c1dc9c9e8c4cf.output'
    if os.path.exists(elec_output) and not os.path.exists('/tmp/electricity_events.txt'):
        import json
        extracted = []
        with open(elec_output) as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    if obj.get('type') == 'assistant':
                        for c in obj.get('message', {}).get('content', []):
                            if c.get('type') == 'text':
                                for tl in c['text'].split('\n'):
                                    tl = tl.strip()
                                    if '|' in tl and len(tl.split('|')) >= 15:
                                        extracted.append(tl)
                except:
                    pass
        if extracted:
            with open('/tmp/electricity_events.txt', 'w') as f:
                f.write('\n'.join(extracted))
            print(f"Extracted {len(extracted)} electricity event lines from agent output")

    total = 0
    for filepath, gpt in files:
        if os.path.exists(filepath):
            count = import_file(filepath, gpt, conn, existing)
            print(f"Imported {count} events from {os.path.basename(filepath)} ({gpt})")
            total += count
        else:
            print(f"File not found: {filepath}")

    conn.commit()

    # Report
    cur = conn.cursor()
    total_events = cur.execute("SELECT COUNT(*) FROM usage_events").fetchone()[0]
    by_gpt = cur.execute("""SELECT g.name, COUNT(*) FROM usage_events e
        JOIN gpt_technologies g ON e.gpt_id=g.id GROUP BY g.name ORDER BY COUNT(*) DESC""").fetchall()
    by_q = cur.execute("SELECT quadrant, COUNT(*) FROM usage_events GROUP BY quadrant ORDER BY quadrant").fetchall()

    print(f"\nTotal imported this run: {total}")
    print(f"Total events in DB: {total_events}")
    for r in by_gpt:
        print(f"  {r[0]}: {r[1]}")
    print("Quadrants:")
    for r in by_q:
        print(f"  {r[0]}: {r[1]}")

    conn.close()


if __name__ == '__main__':
    main()
