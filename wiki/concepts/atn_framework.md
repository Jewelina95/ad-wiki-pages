---
title: AT(N) biomarker framework (Jack 2024 revised)
type: concept
last_updated: 2026-04-25
sources:
  - raw/papers/jack_2024_revised_AD_criteria.pdf
  - raw/papers/biological_definition_of_AD.pdf
  - code/kb_loader/data/staging/atn_framework.json
status: settled
---

# AT(N) biomarker framework

Jack 2024 revised criteria define AD as a **biological disease** — biomarker abnormality establishes the diagnosis, with or without symptoms.

## Categories

- **A — Amyloid:** Amyloid PET, CSF Aβ42/40, plasma p-tau217.
- **T — Tau:**
  - **T1 (early tau):** p-tau217, p-tau181, p-tau231 (fluid markers).
  - **T2 (late tau):** Tau PET, MTBR-tau243, p-tau205 (used for staging extent).
- **N — Neurodegeneration (non-core):** NfL, MRI atrophy, FDG-PET.
- Other non-core: I (inflammation, GFAP), V (vascular, MRI WMH), S (synuclein, α-syn SAA).

## Biological stages (A+ population, by tau extent)

| Stage | Definition                                                           |
|-------|-----------------------------------------------------------------------|
| a     | A+ T2−: amyloid only, no tau spread                                   |
| b     | A+ T2+ limited: early tau spread (medial temporal)                    |
| c     | A+ T2+ moderate: tau spread beyond temporal lobe                      |
| d     | A+ T2+ widespread: whole-brain tau                                    |

## Why this matters for the wearable system

The wearable does **not** measure amyloid or tau. It measures *symptomatic correlates* (gait, HRV, voice, EDA). The AT(N) framework is therefore used by the [Clinical diagnosis agent](../agents/clinical_diagnosis_agent.md) for **referral logic**: when sensor patterns suggest cognitive decline, the agent recommends biomarker testing to confirm AD biology vs. other dementias.

## See also

- [AD staging](ad_staging.md) — clinical/symptomatic axis.
- [Amyloid hypothesis](amyloid_hypothesis.md) — the underlying pathological model.
- [`code/kb_loader/data/staging/atn_framework.json`](../../code/kb_loader/data/staging/atn_framework.json) — structured KB entry.
