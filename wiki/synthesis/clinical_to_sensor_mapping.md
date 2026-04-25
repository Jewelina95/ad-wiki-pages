---
title: Clinical-to-sensor mapping (stage transitions)
type: synthesis
last_updated: 2026-04-25
sources:
  - raw/source_docs/plan_2026-03-13.md
  - wiki/concepts/ad_staging.md
  - wiki/concepts/eda_signal.md
  - wiki/concepts/ppg_hrv.md
  - wiki/concepts/imu_gait.md
  - wiki/concepts/voice_acoustic_linguistic.md
  - wiki/concepts/mcr_criteria.md
status: settled
---

# Clinical-to-sensor mapping — the four key transitions

Each clinical stage transition corresponds to a *combination* of sensor signatures. None is single-modality; all require multimodal fusion + temporal context.

## 1. Normal → SCD: individual baseline drift

| Modality | Signal                                    |
|----------|-------------------------------------------|
| IMU      | Stride variability rises >1 SD vs. personal baseline |
| Voice    | Pause rate gradually increases; vocabulary diversity (TTR) gradually drops |
| PPG      | Slow HRV decline (week- to month-scale)    |

Detection requires **personal baseline** (not group thresholds). The first 2–4 weeks of glove wear establishes baseline.

## 2. SCD → MCI: scale-blind window — biggest project value

| Modality | Signal                                                            |
|----------|-------------------------------------------------------------------|
| IMU+Voice | Dual-task cost (DTC) significantly increases — gait change while talking |
| Multi    | MCR composite: slow gait + subjective complaint → see [MCR criteria](../concepts/mcr_criteria.md) |
| Multi    | Composite Cognitive Index (CCI) deviates from baseline by >2 SD   |

Conventional scales (MMSE, MoCA) miss most of this window. This is where wearable monitoring contributes the most novel signal.

## 3. MCI → Mild AD

| Modality | Signal                                                            |
|----------|-------------------------------------------------------------------|
| IMU      | Hand fine-motor degradation; activity pattern becomes less varied |
| Voice    | Semantic error rate ↑; syntactic complexity ↓                     |
| PPG+EDA  | Persistent HRV worsening + EDA baseline anomalies                 |

ADL (activities-of-daily-living) capability begins to drop and is detectable in activity-pattern features.

## 4. Moderate AD + BPSD

| Modality | Signal                                                            |
|----------|-------------------------------------------------------------------|
| EDA+HR   | Joint forewarning of agitation episodes (target window: 1–2 hr)   |
| Multi    | Sundowning pattern recognition (4–6 PM physiological drift) — see [bpsd_sundowning](../concepts/bpsd_sundowning.md) |
| PPG+IMU  | Sleep–wake rhythm fragmentation                                   |

This is where the [Emotion-behavior agent](../agents/emotion_behavior_agent.md) and [Intervention agent](../agents/intervention_agent.md) carry the most weight.

## Why this is in synthesis/, not concepts/

This page is a *cross-cutting essay* that reads multiple concept pages together. It is the one-paragraph version of the project's clinical thesis: *which signal-combinations correspond to which clinical transitions*. It is the spine of the [Clinical diagnosis agent](../agents/clinical_diagnosis_agent.md)'s reasoning prompt.
