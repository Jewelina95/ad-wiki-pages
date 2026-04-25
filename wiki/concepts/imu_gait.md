---
title: IMU — gait, dual-task cost, hand tremor
type: concept
last_updated: 2026-04-25
sources:
  - code/kb_loader/data/sensors/imu_markers.json
  - wiki/concepts/_source_sensor_signal_principles.md
  - wiki/concepts/gait_norms.md
status: settled
---

# IMU — gait, dual-task cost, hand tremor, fine motor

Tri-axial accelerometer + gyroscope at the wrist / dorsum of the hand. Despite being a hand-mounted IMU, gait can be inferred from arm-swing kinematics.

## Features

- **Gait speed** (Weinberg integration model from arm-swing).
- **Stride variability** (CV of stride duration).
- **Dual-task cost (DTC)** — change in gait while concurrent cognitive load.
- **Hand tremor** — frequency-band power (4–6 Hz physiological; 4–6 Hz rest-tremor PD; AD has finer fine-motor degradation).
- **Fine motor index** — jerk, smoothness during writing / phone-use tasks.

## AD relevance — the strongest single early marker

> Gait-speed inflection point appears **12.1 years before clinical MCI diagnosis** (Buracchio 2010, n=204).
> Meta-analysis: gait analysis predicts MCI→AD conversion with >78% accuracy (Montero-Odasso 2019).

This is the project's earliest detection window and the anchor signal for the [Motor-cognitive agent](../agents/motor_cognitive_agent.md). Combined with subjective cognitive complaint, it implements [MCR criteria](mcr_criteria.md) with sensors only.

## Thresholds (from KB)

| Marker        | SCD          | MCI (Buracchio) | Mild AD       |
|---------------|--------------|-----------------|---------------|
| Gait speed Δ  | −0.05 m/s/yr | −0.023 m/s/yr (inflection) | −0.05 m/s/yr |

Compare against age × sex norms — see [gait norms](gait_norms.md).

## Caveats

- Wrist IMU gait is less direct than a foot- or pelvis-mounted IMU. Validation against the project's own [baseline subjects](../entities/baseline_subjects.md) data has not been published.
- Hand tremor at the wrist can confound gait — needs activity-segmentation first.

## Sources

[`code/kb_loader/data/sensors/imu_markers.json`](../../code/kb_loader/data/sensors/imu_markers.json).
