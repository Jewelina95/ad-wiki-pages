---
title: MCR — Motoric Cognitive Risk syndrome
type: concept
last_updated: 2026-04-25
sources:
  - code/kb_loader/data/clinical/mcr_criteria.json
  - code/kb_loader/data/clinical/gait_norms.json
status: settled
---

# MCR — Motoric Cognitive Risk syndrome (Verghese 2013)

A pre-dementia syndrome defined by **slow gait + subjective cognitive complaint**, in the absence of dementia or mobility disability. Strong independent predictor of progression to AD.

## Diagnostic criteria (all four)

1. Slow gait — gait speed below the age- and sex-matched mean by ≥1 SD.
2. Subjective cognitive complaint — patient self-report of memory or cognitive decline.
3. No dementia (does not meet dementia criteria).
4. No mobility disability — independently ambulatory, no aid required.

## Prevalence and predictive value

- ~10% of community-dwelling older adults.
- Independent risk factor for AD.
- Source: Verghese J et al., 2013.

## Why this matters here

MCR is the **only AD-precursor syndrome that is fully measurable by this glove**:

- Gait speed → IMU, continuous passive measurement, compared against [gait norms](gait_norms.md) by age × sex.
- Subjective cognitive complaint → audio analysis can detect spontaneous mentions of memory difficulty in conversation.

No neuropsychological testing required. This is the [Motor-cognitive agent](../agents/motor_cognitive_agent.md)'s anchor task.

## Implementation pointer

Structured KB entry: [`code/kb_loader/data/clinical/mcr_criteria.json`](../../code/kb_loader/data/clinical/mcr_criteria.json).
