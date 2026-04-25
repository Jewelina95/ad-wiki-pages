---
title: Clinical diagnosis agent
type: agent
last_updated: 2026-04-25
sources:
  - code/src/agents/clinical_diagnosis_agent.py
  - code/src/skills/ad_staging.py
  - code/src/knowledge/ad_staging_criteria.py
  - wiki/concepts/ad_staging.md
  - wiki/concepts/atn_framework.md
  - wiki/synthesis/clinical_to_sensor_mapping.md
status: future
---

> 🌙 **Status: future / 暂缓.**
> 当前阶段一个统一的 [Clinical analysis agent](unified_clinical_agent.md) 已经够用——单 prompt + 知识库查询，规模上来或要做亚专科深度时再拆成这个独立 Agent。详见 [_architecture.md](_architecture.md)。

---

# Clinical diagnosis agent

Clinical role: senior geriatrician / neurologist.

## Inputs

The four specialist agents' outputs + medical context (medications, history, scale scores) + recent assessment history.

## Core capabilities

- AD staging against [Jack 2024 AT(N)](../concepts/atn_framework.md) and [GDS](../concepts/ad_staging.md).
- Transition risk scoring: SCD → MCI → mild → moderate → severe.
- Differential diagnosis support (AD vs DLB vs VaD vs FTD).
- Composite Cognitive Index (CCI) computation and longitudinal tracking.
- Personalized cognitive-trajectory modelling: baseline establishment → drift detection → inflection identification.
- **Referral logic** — when to recommend PET / CSF / plasma p-tau217.

## Outputs

Integrated diagnostic report (stage, confidence, reasoning chain), referral recommendations.

## KB used

- [AD staging](../concepts/ad_staging.md), [AT(N) framework](../concepts/atn_framework.md), [Amyloid hypothesis](../concepts/amyloid_hypothesis.md)
- Atri 2024 AA practice guideline (DETeCD-ADRD) — [`raw/papers/atri_2024_AA_practice_guideline.pdf`](../../raw/papers/atri_2024_AA_practice_guideline.pdf)
- [Clinical-to-sensor mapping](../synthesis/clinical_to_sensor_mapping.md) — the agent's primary reasoning template.

## Code

[`code/src/agents/clinical_diagnosis_agent.py`](../../code/src/agents/clinical_diagnosis_agent.py) — stub.
A working `Skill` for staging exists at [`code/src/skills/ad_staging.py`](../../code/src/skills/ad_staging.py) and serves as the reference implementation.

## Status

Stub agent, working Skill. Of all the agents this one has the most concrete implementation guidance.
