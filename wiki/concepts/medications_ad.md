---
title: AD medications and their sensor footprints
type: concept
last_updated: 2026-04-25
sources:
  - code/kb_loader/data/clinical/medications.json
status: settled
---

# AD medications

Two main classes plus the recent disease-modifying mAbs. Each has a sensor-level footprint that the agents must distinguish from disease progression.

## Cholinesterase inhibitors (donepezil, rivastigmine, galantamine)

- Indication: MCI → moderate AD.
- Effect: modest symptomatic improvement, ~3 months delayed progression (Birks 2006 meta-analysis).
- Side effects: nausea, diarrhoea (20–40% discontinue), bradycardia.
- **Sensor footprint:** PPG must monitor for bradycardia (medication side-effect, not autonomic decline). EDA may show GI-distress signatures.

## Memantine (NMDA antagonist)

- Indication: moderate–severe AD.
- Mechanism: glutamate excitotoxicity modulation.
- Often combined with cholinesterase inhibitors at later stages.

## Disease-modifying mAbs (Lecanemab, Donanemab)

- Indication: MCI / mild AD with confirmed amyloid positivity.
- FDA approval but limited window of efficacy — reinforces the value of *early staging* that this project targets.

## Why agents need this

The [Autonomic agent](../agents/autonomic_agent.md) and [Emotion-behavior agent](../agents/emotion_behavior_agent.md) must subtract medication effects before attributing changes to disease progression. The patient profile carried in `ContextInfo` includes `medication_taken_today` for this reason — see [`code/src/utils/data_models.py`](../../code/src/utils/data_models.py).

## Source

[`code/kb_loader/data/clinical/medications.json`](../../code/kb_loader/data/clinical/medications.json).
