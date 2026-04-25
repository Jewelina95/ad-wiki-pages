---
title: Intervention agent
type: agent
last_updated: 2026-04-25
sources:
  - code/src/agents/intervention_agent.py
status: future
---

> 🌙 **Status: future / 暂缓.**
> 当前阶段一个统一的 [Clinical analysis agent](unified_clinical_agent.md) 已经够用——单 prompt + 知识库查询，规模上来或要做亚专科深度时再拆成这个独立 Agent。详见 [_architecture.md](_architecture.md)。

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
