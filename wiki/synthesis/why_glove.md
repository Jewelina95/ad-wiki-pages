---
title: Why a glove form factor
type: synthesis
last_updated: 2026-04-25
sources:
  - wiki/concepts/glove_form_factor.md
  - wiki/concepts/_source_sensor_design_proposal.md
  - raw/papers/_synthetic_methods_review.docx
status: settled
---

# Why a glove form factor

Wristbands dominate the wearable AD literature (Apple Heart & Movement, AHA wristband cohorts, Empatica, etc.). This project chose a **textile glove** instead. The reasoning, compressed:

## What gloves enable that wristbands don't

1. **EDA quality.** Finger-pad has the highest eccrine sweat-gland density on the body. Wristband EDA is noisy by comparison. For a project where BPSD detection (esp. agitation) is a key goal, this matters — see [EDA signal](../concepts/eda_signal.md).

2. **Hand fine-motor data.** AD has hand-specific motor signatures (writing degradation, manipulation difficulty) that are invisible to a wristband. Hand-mounted IMU captures these directly — see [IMU/gait](../concepts/imu_gait.md).

3. **AD vs PD differential.** Hand tremor characteristics (frequency, posture-dependence) are diagnostically informative. A glove sees this; a wristband averages over the wrist joint and loses the signal.

4. **Near-mouth audio path.** A glove worn during phone calls or hand-to-face gestures gets a substantially cleaner audio path than a wrist mic. Voice features (esp. linguistic ones) are bottlenecked by ASR accuracy, which is bottlenecked by SNR.

## What gloves give up

- **All-day wearability is harder.** Gloves heat the hand, restrict touch sensitivity, and have stronger social acceptability friction than a wristband. The user-preference study cited in [glove_form_factor.md](../concepts/glove_form_factor.md) (PMC8072390, n=21) found that 53.8% of patients/caregivers ranked appearance first — gloves must look unobtrusive (textile, cotton-blend, half-finger) to clear that bar.
- **Battery target.** Same study: 42.9% ranked battery life second; a glove with the same per-day power budget as a wristband ends up bulkier. Target is ≥7 days.
- **Manufacturing.** A textile-integrated multi-sensor glove is harder to fabricate and certify than a sealed wristband.

## Bet

The clinical signal gain (especially for the SCD→MCI window where this project differentiates from existing wearables) outweighs the wearability cost — *if* the device hits the form-factor + battery targets. Failure modes are dominated by the hardware bet, not the clinical bet.

## See also

- [Glove form factor](../concepts/glove_form_factor.md) — the detailed user-research-grounded version.
- [Glove device entity](../entities/glove_device.md).
- [Innovation thesis](innovation_thesis.md) — broader project positioning.
