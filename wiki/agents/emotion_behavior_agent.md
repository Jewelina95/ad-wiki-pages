---
title: Emotion-behavior agent
type: agent
last_updated: 2026-04-25
sources:
  - code/src/agents/emotion_behavior_agent.py
  - wiki/concepts/bpsd.md
status: draft
---

# Emotion-behavior agent

Clinical role: psychiatry + psychology.

## Inputs

EDA + PPG + IMU + voice prosody (multimodal — single modality is not enough).

## Core capabilities

- BPSD detection + classification ([agitation](../concepts/bpsd_agitation.md), [anxiety](../concepts/bpsd_anxiety.md), [apathy](../concepts/bpsd_apathy.md), [sundowning](../concepts/bpsd_sundowning.md), etc.).
- Real-time emotional-state inference via multimodal fusion: EDA arousal × HR activation × voice prosody × motion pattern.
- Agitation-episode forewarning (target: 1–2 hr alert window).
- **Signal disambiguation** — *"is HR↑ from agitation, exercise, or anxiety?"* — using context.
- Personalized BPSD-pattern learning (individual baselines outperform group thresholds; Iaboni 2022).

## Outputs

Emotional-state assessment, BPSD type classification, risk forewarning, full reasoning chain.

## KB used

- [BPSD catalog](../concepts/bpsd.md) — 7 symptom-specific JSONs in [`code/kb_loader/data/clinical/bpsd/`](../../code/kb_loader/data/clinical/bpsd/).
- NPI 12-domain reference (TBD).

## Code

[`code/src/agents/emotion_behavior_agent.py`](../../code/src/agents/emotion_behavior_agent.py) — stub.

## Status

Stub. This is the agent most dependent on **personalized models** rather than population thresholds — the pipeline therefore needs a per-patient baseline learning phase before it produces useful alerts.
