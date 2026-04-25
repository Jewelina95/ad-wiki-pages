---
title: Agent data loader interface
type: method
last_updated: 2026-04-25
sources:
  - code/src/sensors/data_pipeline.py
  - code/src/sensors/preprocessing.py
  - code/src/utils/data_models.py
  - wiki/methods/data_pipeline.md
  - wiki/methods/preprocessing_per_modality.md
status: draft
---

# Agent data loader interface

The contract by which preprocessed sensor data reaches an Agent. Sensor pipeline produces typed feature dicts; agents consume them via `extract_relevant_features`.

## Data flow

```
Hardware → edge preprocessing (ESP32) → CSV storage → AgentDataLoader → MultimodalFeatures → Agent.assess()
```

## Core types (Python)

Defined in [`code/src/utils/data_models.py`](../../code/src/utils/data_models.py):

- `MultimodalFeatures` — bundle of per-modality feature dicts + timestamp.
- `PatientProfile` — demographics, current diagnosis, medications.
- `ContextInfo` — current activity, time-of-day, sundowning window flag, visitor presence, medication taken today.
- `AgentAssessment` — output: findings, confidence, alert level, reasoning, recommendations.
- `AlertLevel` — green / yellow / red.

## Agent contract

Each Agent inherits from `BaseAgent` ([`code/src/agents/base_agent.py`](../../code/src/agents/base_agent.py)) and implements:

- `system_prompt` — specialty identity and reasoning frame.
- `extract_relevant_features(features: MultimodalFeatures) -> dict` — narrows the multimodal bundle to what this Agent cares about.

Inference path (already implemented in `BaseAgent.assess`):

1. Extract relevant features.
2. Build prompt: patient profile + context + sensor features + recent assessment history (last 3).
3. Call Claude (via `anthropic` SDK).
4. Parse JSON response into `AgentAssessment`.

Failure mode: JSON parse error → assessment with `confidence=0.0`, `alert_level=YELLOW`, "需人工审查".

## Why this design

- Decouples Agents from raw signal handling — they reason on already-extracted features.
- Each Agent's KB lookup, prompt template, and feature filter are local to that Agent file. Cross-Agent dependencies go through the [Master coordinator](../agents/master_coordinator.md).
- Recent-history injection is what makes this *agentic* rather than stateless single-shot — agents see their own and peers' past assessments.

## Implementation status

- `BaseAgent.assess()` and prompt scaffolding: implemented.
- All 7 specialist Agents: stubs only ([`code/src/agents/`](../../code/src/agents/)).
- One real `Skill` in [`code/src/skills/ad_staging.py`](../../code/src/skills/ad_staging.py); the rest are placeholders.

## See also

- [Architecture overview](../agents/_architecture.md)
- [Data pipeline](data_pipeline.md), [Preprocessing per modality](preprocessing_per_modality.md)
- [Claude CLI inference pattern](claude_cli_inference_pattern.md) — alternative to SDK calls.
