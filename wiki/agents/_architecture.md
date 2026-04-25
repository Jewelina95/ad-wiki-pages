---
title: Agent architecture — 1 active + 7 future
type: agent
last_updated: 2026-04-25
sources:
  - wiki/agents/unified_clinical_agent.md
  - wiki/synthesis/project_overview.md
  - wiki/entities/mdt_team_template.md
status: draft
---

# Agent architecture — 1 active + 7 future

> 🌱 **Current state:** one [unified clinical analysis agent](unified_clinical_agent.md) handles end-to-end reasoning. The 7-specialist + 1-coordinator design from the original plan is **kept as future architecture** (greyed in dashboard) — to be revisited when real labeled AD wearable data > 100 subjects, or cost/latency/audit pressure justifies the split.

```
   NOW                                    FUTURE (status: future, greyed)
┌──────────────────┐                ┌─────────────────────────────────┐
│  Unified         │                │   Master Coordinator            │
│  Clinical        │      →         │   integration + conflict        │
│  Analysis        │                │   arbitration + reasoning chain │
│  Agent           │                └──────────────┬──────────────────┘
│                  │                               │
│  ↑ KB query      │                   ┌─────┬─────┼─────┬─────┬─────┬─────┐
│  ↑ all features  │                   │     │     │     │     │     │     │
└──────────────────┘                 Motor Lang Auto Emot Clin Intv Care
```

## Why one agent, not seven (right now)

The original plan called for 7 specialists + 1 coordinator mirroring an MDT meeting. After implementation reality kicked in:

1. **Data sparsity.** N=4 healthy baseline subjects; no labeled AD wearable corpus yet. Per-specialty thresholds aren't trainable. A unified agent that reads the KB at inference time gives more leverage per token.
2. **Modern Claude is capable enough.** Frontier models hold full clinical reasoning + multimodal feature interpretation + KB lookup in one prompt without losing coherence.
3. **Conflict arbitration is theoretical until conflicts exist.** The MDT-style "specialists disagree → coordinator arbitrates" flow needs actual parallel reasoning to disagree about. With one prompt and one KB, conflicts collapse.

The 7-specialist design is **not abandoned** — it's parked as the answer to a future scaling problem. Documentation kept, status: `future`, greyed in dashboard.

## When to split back

Trigger conditions for activating the 7 specialists:

- Real labeled AD wearable data > 100 subjects → per-specialty threshold tuning becomes feasible
- Cost / latency pressure → smaller specialty-specific models cheaper than always-on frontier
- Audit / regulatory requirement → per-specialty reasoning chains improve traceability
- Multi-modal data load grows beyond what a single-prompt context window comfortably handles

## The active agent

[`unified_clinical_agent.md`](unified_clinical_agent.md) — single agent, reads the [agent data interface](../methods/agent_data_loader_interface.md) feature bundle, queries the [expert KB](../synthesis/expert_kb_report.md), outputs stage + reasoning + intervention.

Implementation: [`code/src/agents/base_agent.py`](../../code/src/agents/base_agent.py) (Claude SDK scaffold) + [`code/src/skills/ad_staging.py`](../../code/src/skills/ad_staging.py) (the working Skill).

## The 7 future specialists (kept as roadmap)

| Agent | Future role | When to activate |
|---|---|---|
| [Motor-cognitive](motor_cognitive_agent.md) | Gait / MCR / tremor specialist | When IMU corpus > 50 subjects |
| [Language-cognitive](language_cognitive_agent.md) | Speech / linguistic specialist | When ASR pipeline + Chinese voice corpus stabilizes |
| [Autonomic](autonomic_agent.md) | HRV / EDA specialist | When 24h continuous monitoring data accumulates |
| [Emotion-behavior](emotion_behavior_agent.md) | BPSD detection specialist | When per-patient personalized model becomes the bottleneck |
| [Clinical diagnosis](clinical_diagnosis_agent.md) | Senior geriatrician integration | When referral logic complexity exceeds single-prompt capacity |
| [Intervention](intervention_agent.md) | Music / cognitive / TCM therapist | When intervention library outgrows simple lookup |
| [Care management](care_management_agent.md) | Caregiver report + alert triage | When end-user UX needs dedicated tone-tuning |
| [Master coordinator](master_coordinator.md) | MDT chair / conflict arbitration | When ≥3 specialists are active and disagreeing |
