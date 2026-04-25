---
title: BPSD — Behavioural and Psychological Symptoms of Dementia
type: concept
last_updated: 2026-04-25
sources:
  - code/kb_loader/data/clinical/bpsd/
status: settled
---

# BPSD — Behavioural and Psychological Symptoms of Dementia

Umbrella term for the non-cognitive symptoms (mood, behaviour, perception) that affect 50–90% of AD patients across the disease course. Major source of caregiver burden and a primary target for the [Emotion-behavior agent](../agents/emotion_behavior_agent.md) and [Intervention agent](../agents/intervention_agent.md).

## Catalog

| Symptom         | Peak stage    | Sensor signature (multimodal)            | Detail page |
|-----------------|---------------|------------------------------------------|-------------|
| Agitation       | Moderate      | EDA↑ + HR↑ + activity↑                   | [bpsd_agitation](bpsd_agitation.md) |
| Anxiety         | MCI–Mild      | EDA↑ + HR↑ + activity normal             | [bpsd_anxiety](bpsd_anxiety.md) |
| Apathy          | Mild–Moderate | activity↓ + EDA flat + voice prosody flat | [bpsd_apathy](bpsd_apathy.md) |
| Depression      | MCI–Moderate  | activity↓ + HRV↓ + voice prosody flat    | [bpsd_depression](bpsd_depression.md) |
| Sleep disorder  | All stages    | nighttime activity surges + PPG arrhythmia | [bpsd_sleep_disorder](bpsd_sleep_disorder.md) |
| Sundowning      | Moderate      | 4–6 PM gradual EDA↑ + HR↑ + restlessness | [bpsd_sundowning](bpsd_sundowning.md) |
| Wandering       | Moderate      | high step count + atypical location pattern | [bpsd_wandering](bpsd_wandering.md) |

Best multimodal combinations (EDA + HR + activity) reach AUC 0.80–0.95 in individualized models (Iaboni 2022, n=48 nursing-home cohort).

## Why disambiguation matters

A raw HR↑ can come from agitation, exercise, anxiety, medication side-effect, or fever. Without context (current activity, time-of-day, medication state), the same physiological signal has different clinical meaning. This is the central problem the multi-agent context-reasoning approach is designed to solve — see [innovation thesis](../synthesis/innovation_thesis.md) and the master coordinator's conflict arbitration in [`wiki/agents/master_coordinator.md`](../agents/master_coordinator.md).

## Caveats

- Most published evidence is from Western nursing-home cohorts. Chinese community-dwelling patients may show different baseline rates and triggers.
- Detection windows (e.g., agitation 1–2 hr forewarning) are aspirational — to be validated on the project's own data.
