---
title: Clinical xlsx 2026-04-18 — longitudinal cohort (脱敏)
type: dataset
last_updated: 2026-04-25
sources:
  - raw/clinical_data/
  - wiki/entities/clinical_database_capital_medical.md
status: draft
---

# Clinical xlsx 2026-04-18 (脱敏 longitudinal cohort)

10 de-identified Excel files received 2026-04-18 from the clinical partner. Covers a master AD-EYE registry plus 4-timepoint repeated-measures and a TMS treatment arm.

## Files

| File                           | Timepoint(s) | Notes                          |
|--------------------------------|--------------|--------------------------------|
| AD_EYE_总库_脱敏.xlsx          | cross-section | Master AD-EYE registry         |
| RI_data_T0_脱敏.xlsx           | T0           | Baseline assessment           |
| RI_data_T1_脱敏.xlsx           | T1           | 1st follow-up                  |
| RT_data_T2_脱敏.xlsx           | T2           | 2nd follow-up                  |
| RT_data_T3_脱敏.xlsx           | T3           | 3rd follow-up                  |
| TMS_T0_脱敏.xlsx               | T0           | TMS arm baseline              |
| TMS_T1_脱敏.xlsx               | T1           | TMS arm 1st follow-up          |
| TMS_T2_脱敏.xlsx               | T2           | TMS arm 2nd follow-up          |
| TMS_随访_脱敏.xlsx             | follow-up    | TMS arm long-term follow-up    |
| 性别差异数据库_脱敏.xlsx       | cross-section | Sex-difference subset         |

Files: [`raw/clinical_data/`](../../raw/clinical_data/).

## Data dictionary

**TBD.** The columns and scoring conventions need a pass to produce a proper data dictionary on this page. Until then, treat this as the index, not the documentation.

## Use

- This is the project's only **real labeled longitudinal AD data**.
- It is *clinical scale + imaging* data, not wearable. It does not yet overlap with [baseline subjects S01–S04](../entities/baseline_subjects.md) or any wearable corpus.
- Eventual ground-truth corpus for validating the staging agents — see [open question #4](../synthesis/what_we_dont_know.md).

## Caveats

- 脱敏 ID-mapping is held by the data custodian; we do not have re-identification capability and should not.
- Data-sharing agreement scope: TBD.
- See [Clinical database entity](../entities/clinical_database_capital_medical.md).
