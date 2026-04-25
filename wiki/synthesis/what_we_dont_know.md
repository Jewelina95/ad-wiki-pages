---
title: What we don't know — open questions ledger
type: synthesis
last_updated: 2026-04-25
status: open_question
---

# What we don't know

This page is the project's open-questions registry. Each entry has a status, an owner, and a back-link to its source page. Resolved questions move out (with a log entry); new ones come in here first.

## Open

### #1 — Synthetic data pipeline validity (registered 2026-04-25)

The rule-based degradation engine that produced the v0 synthetic AD CSVs may not faithfully model real AD progression. Source population is healthy young adults; degradation parameters are extrapolated from cross-sectional gait studies; cross-modal coupling is hand-engineered; no TSTR validation exists.

- Detail page: [`wiki/methods/synthetic_data_review.md`](../methods/synthetic_data_review.md)
- Affected: [`wiki/methods/synthetic_data_v0_rules.md`](../methods/synthetic_data_v0_rules.md), [`wiki/datasets/synthetic_84.md`](../datasets/synthetic_84.md), all model training that uses synthetic data.
- Owner: user. Deadline: TBD.

### #2 — Chinese community-dwelling BPSD prevalence and signature

Most BPSD evidence in the KB is from Western nursing-home cohorts (Iaboni 2022 n=48; Valenza 2018). Whether the EDA+HR+activity signatures generalize to Chinese community-dwelling AD is unknown.

- Affected: [BPSD pages](../concepts/bpsd.md), [Emotion-behavior agent](../agents/emotion_behavior_agent.md).
- Owner: user / 李医生 follow-up.
- Resolution path: validate against the [clinical database](../entities/clinical_database_capital_medical.md) once wearable data overlaps with the cohort.

### #3 — Agent stub → implementation gap

7 of 8 agent files in `code/src/agents/` are stubs. The `BaseAgent.assess()` scaffold and one Skill (`ad_staging`) exist; everything else is placeholder.

- Affected: all of [`wiki/agents/`](../agents/_architecture.md).
- Owner: user.
- Resolution path: incremental implementation per agent.

### #4 — Wearable+clinical data overlap is empty

The clinical database (xlsx, T0–T3 longitudinal) and the wearable data (S01–S04 baseline + synthetics) are on **disjoint patient sets**. The eventual co-recruitment phase will bridge this; until then the wearable agents cannot be trained on labeled real AD data.

- Affected: validation strategy of all agents.
- Owner: ethics + recruitment timeline.

### #5 — Glove hardware not fabricated

No physical glove unit yet. ESP32 audio prototype works; the integrated EDA+PPG+IMU+mic glove is design-only. All sensor analysis is on data captured from off-the-shelf or component-level hardware.

- Affected: [glove device entity](../entities/glove_device.md), realism of all "wearable" demos.
- Owner: hardware track.

## How to use this page

Add new entries at the bottom of "Open" with a `### #N — title (registered YYYY-MM-DD)` heading. When resolved, move to "Resolved" below with the resolution date and a one-line summary.

## Resolved

*(none yet)*
