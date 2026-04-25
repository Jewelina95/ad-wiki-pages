---
title: AD staging — SCD / MCI / mild / moderate / severe
type: concept
last_updated: 2026-04-25
sources:
  - raw/papers/jack_2024_revised_AD_criteria.pdf
  - raw/papers/atri_2024_AA_practice_guideline.pdf
  - raw/papers/biological_definition_of_AD.pdf
  - code/kb_loader/data/staging/gds_stages.json
  - code/kb_loader/data/staging/atn_framework.json
  - wiki/concepts/_source_ad_staging_seed.md
status: settled
---

# AD staging — SCD / MCI / mild / moderate / severe AD

Two parallel staging frameworks are used in this project: the **clinical/symptomatic** progression (SCD → MCI → mild → moderate → severe AD, GDS 1–7) and the **biological** AT(N) framework. They are complementary, not redundant — biology can be positive years before symptoms.

## Clinical stages (GDS-based, simplified)

| Stage         | GDS | MMSE   | CDR | Functional status                | Where this project's sensors add the most |
|---------------|-----|--------|-----|----------------------------------|-------------------------------------------|
| Normal        | 1   | 30     | 0   | Independent                      | Baseline establishment                    |
| SCD (主观认知下降) | 2 | 27–30  | 0   | Subjective concerns only         | Personal-baseline drift detection         |
| MCI (轻度认知障碍) | 3 | 24–27  | 0.5 | Mild objective deficit, ADL ok   | **Largest gap vs. scales — biggest value here** |
| Mild AD       | 4   | 19–23  | 1   | Some ADL impairment              | Multimodal CCI, BPSD onset                |
| Moderate AD   | 5–6 | 10–18  | 2   | Major ADL impairment             | BPSD prediction (esp. agitation, sundowning) |
| Severe AD     | 7   | <10    | 3   | Total dependence                 | Comfort + safety monitoring               |

Full per-stage descriptions in [`code/kb_loader/data/staging/gds_stages.json`](../../code/kb_loader/data/staging/gds_stages.json) (Reisberg 1982).

## Biological staging (Jack 2024 AT(N))

See [`wiki/concepts/atn_framework.md`](atn_framework.md) for A/T/N biomarkers and the four biological stages a/b/c/d.

## How the two frameworks are used together

- The **biological** framework defines whether AD is present (binary, biomarker-driven).
- The **clinical** framework defines how far it has progressed *symptomatically*.
- The system's wearable signals correlate primarily with the *clinical* axis (gait slowdown, HRV decline, BPSD) — they do not directly measure amyloid or tau.
- The [Clinical diagnosis agent](../agents/clinical_diagnosis_agent.md) is responsible for the synthesis and for flagging when biomarker testing (PET / CSF / plasma p-tau217) is indicated.

## Stage transitions this project tries to detect

The four key transitions and their sensor signatures are written up as a standalone page: [`wiki/synthesis/clinical_to_sensor_mapping.md`](../synthesis/clinical_to_sensor_mapping.md).
