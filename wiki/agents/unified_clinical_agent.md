---
title: Unified clinical analysis agent
type: agent
last_updated: 2026-04-25
status: draft
sources:
  - wiki/agents/_architecture.md
  - code/src/skills/ad_staging.py
  - code/src/agents/base_agent.py
---

# Unified clinical analysis agent

**Current active agent.** One single Claude-backed agent handles end-to-end clinical analysis: takes the multimodal sensor features + patient profile + context, queries the expert KB, and emits a staged assessment + intervention recommendation.

## Why a single agent (right now)

When this project started the design called for **7 specialist agents + 1 coordinator** mirroring an MDT meeting. After implementation, two realities collapsed that to one:

1. **Data sparsity.** Real wearable data: N=4 healthy baseline subjects. There is no labeled AD data to train per-specialty thresholds against. A single agent that reads the KB at inference time outperforms 7 thin specialists with hand-engineered prompts.

2. **Claude is capable enough.** Modern frontier models hold the full clinical reasoning + multimodal feature interpretation + KB lookup in one prompt without losing coherence. The conflict-arbitration value the coordinator was supposed to provide doesn't show up when the same model is reasoning across all domains in one pass.

## What it does

- Reads the [agent data interface](../methods/agent_data_loader_interface.md) feature bundle.
- Queries the [expert KB](../synthesis/expert_kb_report.md) (5 directories: 分期 / 症状 / 传感器指标 / 干预方案 / 证据文献).
- Outputs:
  - Stage assessment ([SCD/MCI/Mild/Moderate/Severe](../concepts/ad_staging.md)) + confidence
  - Reasoning chain with KB citations
  - BPSD risk flags (if any)
  - Non-pharmacologic intervention recommendation

## When to split back into specialists

The 7-specialist design ([masters](master_coordinator.md), [motor-cognitive](motor_cognitive_agent.md), [language-cognitive](language_cognitive_agent.md), [autonomic](autonomic_agent.md), [emotion-behavior](emotion_behavior_agent.md), [clinical diagnosis](clinical_diagnosis_agent.md), [intervention](intervention_agent.md), [care management](care_management_agent.md)) is preserved as a **future architecture**, marked `status: future`. Trigger conditions for revisiting:

- Real labeled AD wearable data > 100 subjects → per-specialty threshold tuning becomes feasible
- Cost / latency pressure → smaller specialty-specific models cheaper than always-on frontier
- Audit / regulatory requirement → per-specialty reasoning chains improve traceability

## Code

[`code/src/agents/base_agent.py`](../../code/src/agents/base_agent.py) — Claude SDK call scaffold (the foundation, currently the only implemented agent reasoning path).
[`code/src/skills/ad_staging.py`](../../code/src/skills/ad_staging.py) — the one working Skill (staging logic) that the unified agent uses.
