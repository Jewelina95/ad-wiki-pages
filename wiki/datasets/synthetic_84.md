---
title: Synthetic 4.8 — 81 stage-overlay CSVs
type: dataset
last_updated: 2026-04-25
status: working_hypothesis
sources:
  - raw/sensor_data/synthetic_4.8/
  - raw/sensor_data/synthetic_4.8/synthetic_manifest.json
  - code/scripts/legacy/baseline48_generate_synthetic_ad.py
see_also:
  - wiki/methods/synthetic_data_v0_rules.md
  - wiki/methods/synthetic_data_review.md
  - wiki/synthesis/what_we_dont_know.md
---

# Synthetic 4.8 — stage-overlay corpus

> ⚠️ **Status: working hypothesis. The methodology that produced this dataset is under review — see [`synthetic_data_review.md`](../methods/synthetic_data_review.md).**

## What's in it

- **Files:** 81 CSVs + 1 manifest in [`raw/sensor_data/synthetic_4.8/`](../../raw/sensor_data/synthetic_4.8/)
- **Total rows:** 435,513
- **Generation method:** rule-based degradation overlay on the [baseline subjects S01–S04](../entities/baseline_subjects.md) cleaned recordings.
- **Generator script:** [`code/scripts/legacy/baseline48_generate_synthetic_ad.py`](../../code/scripts/legacy/baseline48_generate_synthetic_ad.py)

## Schema (per file)

Filename: `S0{1,2,3,4}_{name}_{MCI|mild_AD|moderate_AD}_{task}.csv`

Columns: same 13-column sensor schema as baseline (`gsr, ppg_ir, hr, imu_ax/ay/az, steps, env_*`).

Per-file summary stats in `synthetic_manifest.json`:

```json
{
  "subject": "S01_zewei",
  "stage": "MCI",
  "task": "walking_dual_task",
  "n_rows": 1968,
  "svm_cv_pct": 19.21,
  "jerk_mean": 0.8165,
  "gsr_mean": 1884.2,
  "hr_mean": 80.4
}
```

## Coverage

| Subject (4) × Stage (3) × Task (~7) | = 81 files (some subject×task combinations skipped where source recording was unavailable) |

Tasks present: `walking_dual_task`, `walking_normal`, `turning`, `balance_standing`, `wandering_simulate`, `sit_to_stand`, `hand_fine_motor`. (`writing` and `phone_using` are not in the synthetic set.)

## Caveats

- Sample size is **N=4 source subjects** — this is not a 4-times-bigger dataset, it's the same 4 people with degradation overlays.
- Source population is **healthy young adults**, not the AD demographic.
- Stage labels are **synthetic constructions**, not validated against any real AD wearable corpus.
- See [`synthetic_data_review.md`](../methods/synthetic_data_review.md) for the full open-questions ledger.

## Use

OK for: pipeline integration tests, agent-system stress-testing.
Not OK for: training any classifier intended for clinical inference.

## Related

- [Baseline 4.8 (real source)](baseline_4.8.md)
- [Synthetic v0 (older small-set generator)](../../raw/sensor_data/synthetic_v0/) — predecessor; 12 single-purpose CSVs.
