---
title: BPSD — Wandering
type: concept
last_updated: 2026-04-25
sources:
  - code/kb_loader/data/clinical/bpsd/wandering.json
status: settled
---

# Wandering

Aimless or repetitive ambulation, common in moderate AD. Major safety concern for caregivers.

## Sensor signature

- **IMU:** high step count, atypical movement pattern (repetitive, non-purposeful)
- **Activity context:** activity level high but not aligned with scheduled tasks
- **HR / EDA:** can be elevated if accompanied by agitation, or *normal* (purposeless wandering ≠ agitated wandering — important distinction)

## Detection challenges

- Distinguishing purposeful walking (exercise, errands) from wandering requires either location context (out of scope for the glove alone) or temporal-pattern analysis (repetition, atypical hour).
- The synthetic data v0 includes a `wandering_simulate` task — see [`raw/sensor_data/baseline_4.8/cleaned/`](../../raw/sensor_data/baseline_4.8/cleaned/) and the synthetic outputs derived from it. ⚠ Whether this simulation captures real wandering kinematics is one of the open questions in [`wiki/methods/synthetic_data_review.md`](../methods/synthetic_data_review.md).

## Intervention

Safety alerts to caregiver, gentle redirection prompts via audio. See [Intervention agent](../agents/intervention_agent.md).

KB: [`code/kb_loader/data/clinical/bpsd/wandering.json`](../../code/kb_loader/data/clinical/bpsd/wandering.json). Umbrella: [BPSD](bpsd.md).
