---
title: Multi-agent architecture overview
type: agent
last_updated: 2026-04-25
sources:
  - raw/source_docs/plan_2026-03-13.md
  - wiki/synthesis/project_overview.md
  - wiki/entities/mdt_team_template.md
  - code/src/agents/
status: draft
---

# Multi-agent architecture — 7 specialists + 1 coordinator

Mirrors the clinical [MDT model](../entities/mdt_team_template.md). Each Agent is one specialty; a coordinator integrates and arbitrates conflicts.

```
┌─────────────────────────────────┐
│   Master Coordinator            │
│   integration + conflict        │
│   arbitration + reasoning chain │
└──────────────┬──────────────────┘
               │
   ┌─────┬─────┼─────┬─────┬─────┬─────┐
   │     │     │     │     │     │     │
 Motor Lang Auto Emot Clin Intv Care
```

## Per-agent quick reference

| Agent | Specialty | Inputs | Outputs |
|-------|-----------|--------|---------|
| [Motor-cognitive](motor_cognitive_agent.md) | Rehab + cognitive eval | IMU | Gait/MCR/fall risk |
| [Language-cognitive](language_cognitive_agent.md) | Cognitive eval + speech-lang therapy | Audio | Acoustic + linguistic + stage signals |
| [Autonomic](autonomic_agent.md) | Neurology | PPG + EDA | HRV / autonomic balance / sleep |
| [Emotion-behavior](emotion_behavior_agent.md) | Psychiatry + psychology | EDA + PPG + IMU + voice prosody | BPSD detection + forewarning |
| [Clinical diagnosis](clinical_diagnosis_agent.md) | Senior geriatrician | All other agents' outputs + medical context | Stage assessment + referral logic |
| [Intervention](intervention_agent.md) | Therapist (music / cognitive / TCM) | Emotion + clinical outputs + patient profile | Non-pharmacologic intervention plan |
| [Care management](care_management_agent.md) | GP + care coordinator | All agents | Report assembly + caregiver alerts |
| [Master coordinator](master_coordinator.md) | MDT chair | All specialist assessments | Integrated diagnosis + reasoning chain |

## Message flow

1. Sensor preprocessing emits a `MultimodalFeatures` bundle (per-modality dicts + timestamp).
2. Specialist agents (Motor, Language, Autonomic, Emotion-behavior) run in parallel — each filters relevant features and produces an `AgentAssessment`.
3. Clinical diagnosis agent consumes all four specialist outputs + `PatientProfile` + `ContextInfo` + history → integrated stage assessment.
4. Intervention agent consumes emotion + clinical + profile → recommendation.
5. Care management agent consumes everything → caregiver-facing report and alerts.
6. Master coordinator owns the conflict-arbitration step at any point: when two agents disagree on alert level or stage, the coordinator's prompt encodes the MDT-meeting heuristics for resolution.

## Implementation status

All 7 specialist agents and the master coordinator are **stubs**. The `BaseAgent.assess()` scaffold + Claude SDK call path is implemented in [`code/src/agents/base_agent.py`](../../code/src/agents/base_agent.py). One real Skill exists ([`code/src/skills/ad_staging.py`](../../code/src/skills/ad_staging.py)).

See [What we don't know #3](../synthesis/what_we_dont_know.md) for the implementation gap as a tracked open question.

## Why multi-agent (not a single big prompt)

- **Knowledge boundary:** each specialty's KB and feature filter is local. Easier to curate and audit.
- **Conflict surfacing:** disagreement between agents is *informative* (e.g., "elevated HR" — autonomic agent says decline, emotion agent says agitation, clinical agent must arbitrate using context). A monolithic prompt buries this.
- **Auditability:** each agent emits an `AgentAssessment` with its own reasoning string — the system produces a multi-perspective record per evaluation.
- **Cost control:** specialists can run on cheaper models; coordinator can be the only one on the top-tier model.
