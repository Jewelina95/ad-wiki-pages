---
title: Pilot 3.20 — early collection
type: dataset
last_updated: 2026-04-25
sources:
  - raw/sensor_data/pilot_3.20/
status: settled
---

# Pilot 3.20 — early sensor collection (2026-03-20)

Earliest in-house sensor data collection. Predecessor to the [Baseline 4.8](baseline_4.8.md) protocol; produced rougher data but established the pipeline.

## Contents

- `all_sensors_log_withLabel20260326_093901.csv` — multi-sensor log with task labels.
- `synthetic_dataset_summary.json` — summary of an early synthetic-generation pass.
- `patients/patient_001.json` … `patient_006.json` — 6 simulated/template patient profiles.
- `baselines/patient_00*_baseline.json` — corresponding baseline parameters.
- `real data/imu_raw&feature.rar` — raw IMU + feature archive (compressed; not extracted in raw/).

## Status

Superseded by [Baseline 4.8](baseline_4.8.md) for normative reference; kept for provenance.

## Notes

- Patient profiles here are *templates*, not real subjects.
- File path: [`raw/sensor_data/pilot_3.20/`](../../raw/sensor_data/pilot_3.20/).
