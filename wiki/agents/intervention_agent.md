---
title: Intervention agent
type: agent
last_updated: 2026-04-25
sources:
  - code/src/agents/intervention_agent.py
status: draft
---

# Intervention agent

Clinical role: therapist (music therapy, cognitive training, TCM).

## Inputs

Emotion-behavior agent output + clinical diagnosis agent output + patient preference profile.

## Core capabilities

- **Non-pharmacologic interventions:**
  - Music therapy with personalized song selection (preference-archive-driven).
  - Voice-guided breathing / meditation.
  - Cognitive-training task delivery.
  - Reminiscence-therapy voice prompts.
- Intervention-effectiveness tracking (does the music actually reduce EDA arousal?).
- Routing to in-person care when non-pharmacologic intervention is insufficient.

## Outputs

Intervention plan, delivery instructions, effectiveness check schedule.

## Why non-pharmacologic first

For BPSD, non-pharmacologic interventions are first-line per all major guidelines (evidence level A). Antipsychotics carry stroke and mortality risks in dementia. The agent's default action is non-drug; drug recommendations require explicit clinical agent escalation.

## Code

[`code/src/agents/intervention_agent.py`](../../code/src/agents/intervention_agent.py) — stub.

## Status

Stub.
