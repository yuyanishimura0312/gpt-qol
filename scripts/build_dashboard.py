"""
Build dashboard by injecting DB data as JSON into HTML template.
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'gpt_impact_genealogy.db')
HTML_TEMPLATE = os.path.join(os.path.dirname(__file__), '..', 'dashboards', 'index.html')
HTML_OUTPUT = HTML_TEMPLATE  # overwrite in place


def build():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    data = {}

    # Total
    data['total'] = cur.execute("SELECT COUNT(*) FROM usage_events").fetchone()[0]

    # By GPT
    data['by_gpt'] = cur.execute("""
        SELECT g.name, COUNT(*) FROM usage_events e
        JOIN gpt_technologies g ON e.gpt_id = g.id
        GROUP BY g.name ORDER BY COUNT(*) DESC
    """).fetchall()

    # Quadrants
    data['quadrants'] = cur.execute("""
        SELECT quadrant, COUNT(*) FROM usage_events
        GROUP BY quadrant ORDER BY quadrant
    """).fetchall()

    # Domains
    data['domains'] = cur.execute("""
        SELECT domain, COUNT(*) FROM usage_events
        GROUP BY domain ORDER BY COUNT(*) DESC
    """).fetchall()

    # Adoption paths count
    data['adoption_paths'] = cur.execute("SELECT COUNT(*) FROM adoption_paths").fetchone()[0]

    # Relations count
    data['relations'] = cur.execute("SELECT COUNT(*) FROM event_relations").fetchone()[0]

    # Dimension scores per GPT
    dim_scores = []
    for gpt_name, _ in data['by_gpt']:
        scores = cur.execute("""
            SELECT
                ROUND(AVG(score_aesthetic), 2),
                ROUND(AVG(score_emotional), 2),
                ROUND(AVG(score_meaning), 2),
                ROUND(AVG(score_relational), 2),
                ROUND(AVG(score_autonomy), 2),
                ROUND(AVG(score_cultural), 2)
            FROM usage_events e
            JOIN gpt_technologies g ON e.gpt_id = g.id
            WHERE g.name = ?
        """, (gpt_name,)).fetchone()
        dim_scores.append([gpt_name, {
            'aesthetic': scores[0] or 0,
            'emotional': scores[1] or 0,
            'meaning': scores[2] or 0,
            'relational': scores[3] or 0,
            'autonomy': scores[4] or 0,
            'cultural': scores[5] or 0,
        }])
    data['dim_scores'] = dim_scores

    # Quadrant II samples (top 20 by qol_composite)
    q2_rows = cur.execute("""
        SELECT e.name, e.name_ja, g.name, e.year_start, e.region,
               e.score_aesthetic, e.score_emotional, e.score_meaning,
               e.score_relational, e.score_autonomy, e.score_cultural,
               e.adoption_path_type, e.description
        FROM usage_events e
        JOIN gpt_technologies g ON e.gpt_id = g.id
        WHERE e.quadrant = 'II'
        AND e.description IS NOT NULL AND length(e.description) > 50
        AND e.name_ja IS NOT NULL AND length(e.name_ja) > 3
        ORDER BY e.qol_composite DESC
        LIMIT 20
    """).fetchall()
    data['q2_samples'] = [{
        'name': r[0], 'name_ja': r[1], 'gpt': r[2], 'ys': r[3], 'region': r[4],
        'sa': r[5] or 0, 'se': r[6] or 0, 'sm': r[7] or 0,
        'sr': r[8] or 0, 'sau': r[9] or 0, 'sc': r[10] or 0,
        'path': r[11], 'desc': r[12]
    } for r in q2_rows]

    # Path types
    data['path_types'] = cur.execute("""
        SELECT adoption_path_type, COUNT(*) FROM usage_events
        WHERE adoption_path_type IS NOT NULL
        GROUP BY adoption_path_type ORDER BY COUNT(*) DESC
    """).fetchall()

    conn.close()

    # Inject into HTML
    with open(HTML_TEMPLATE, 'r') as f:
        html = f.read()

    json_str = json.dumps(data, ensure_ascii=False)
    html = html.replace('/*DATA_PLACEHOLDER*/null', json_str)

    with open(HTML_OUTPUT, 'w') as f:
        f.write(html)

    print(f"Dashboard built: {HTML_OUTPUT}")
    print(f"  Total events: {data['total']:,}")
    print(f"  Quadrant II: {dict(data['quadrants']).get('II', 0):,}")
    print(f"  GPTs: {len(data['by_gpt'])}")


if __name__ == '__main__':
    build()
