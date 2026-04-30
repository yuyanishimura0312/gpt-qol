# GPT Impact on Quality of Life (GPT-QoL)

General Purpose Technology (GPT) that enhances quality of life: an academic knowledge base for identifying non-linear routes from historical technology adoption patterns to future robotics possibilities.

## Framework

2-axis, 4-quadrant model:
- X-axis: Macro-economic contribution (positive/negative)
- Y-axis: Quality of life enhancement (positive/negative)
- Target: Quadrant I (QoL+, Econ+) and especially Quadrant II (QoL+, Econ-)

## 6-Dimension QoL Scoring Model

| Dimension | Japanese | Academic Foundation |
|-----------|----------|-------------------|
| Aesthetic | 感覚・美的経験 | Nussbaum, AEQ, Flow |
| Emotional | 感情的豊かさ | Kama Muta, PANAS, Ryff |
| Meaning | 意味・目的 | Ikigai-9, PERMA, Ryff |
| Relational | 関係性・帰属 | PERMA-R, Ryff |
| Autonomy | 自律・成長 | Sen Capability, Ryff |
| Cultural | 文化的感受性 | GNH, Mono no Aware, Wabi-Sabi |

Each dimension scored -5 to +5.

## Three Databases

### DB1: QoL Sensibility Scoring Knowledge (`qol_sensibility.db`)
Academic frameworks and measurement scales for QoL with emphasis on emotional richness and aesthetic sensitivity.

### DB2: GPT Impact Genealogy (`gpt_impact_genealogy.db`)
Historical GPT usage genealogy scored against 6-dimension QoL model.
- Primary: Automobile, Telephone, Printing Press
- Auxiliary: Electricity, Steam Engine

### DB3: Robotics Futures Evidence (`robotics_futures_evidence.db`)
Academic mentions of future robotics possibilities (4-layer architecture following AI Acceleration Evidence DB pattern).

## Architecture

All DBs use SQLite with shared patterns:
- 4-layer structure: Taxonomy -> Source -> Evidence -> Aggregate
- Multi-signal scoring (6 QoL dimensions + economic axis)
- Year confidence tracking
- Genealogy network management

## Setup

```bash
python3 scripts/init_db1_qol_sensibility.py
python3 scripts/init_db2_gpt_impact.py
python3 scripts/init_db3_robotics_futures.py
```
