---
title: Synthetic data — review and open questions
type: method
last_updated: 2026-04-25
status: open_question
sources:
  - wiki/methods/synthetic_data_v0_rules.md
  - wiki/methods/synthetic_data_methods_landscape.md
  - raw/sensor_data/synthetic_4.8/
  - raw/sensor_data/synthetic_v0/
  - code/scripts/legacy/baseline48_generate_synthetic_ad.py
  - code/scripts/legacy/generate_synthetic_sensors_v0.py
see_also:
  - wiki/synthesis/what_we_dont_know.md
---

# Synthetic data — review and open questions

> **Status: open question. Registered 2026-04-25 by user.**
> *"关于这个合成数据你也可以重新去思考不一定就是正确的。"*

This page is the open-questions ledger for the synthetic AD wearable data pipeline. The CSVs themselves (84 files in `raw/sensor_data/synthetic_4.8/` plus 12 in `raw/sensor_data/synthetic_v0/`) are preserved as v0 artifacts. The *narrative* about whether they are valid is here, and is provisional.

## What v0 currently does

A rule-based degradation engine ([`code/scripts/legacy/baseline48_generate_synthetic_ad.py`](../../code/scripts/legacy/baseline48_generate_synthetic_ad.py)) takes each cleaned recording from [baseline subjects S01–S04](../entities/baseline_subjects.md) (healthy young adults, N=4) and overlays parameterized degradations to produce three AD-stage variants per subject per task:

| Stage       | Degradation knobs (representative)                         |
|-------------|------------------------------------------------------------|
| MCI         | mild `svm_noise_mult`, mild `stride_jitter`, slight `tremor_amp` |
| mild_AD     | moderate values of all three                               |
| moderate_AD | aggressive values + `gsr_drift`, `hr_offset`               |

Output: 4 subjects × 3 stages × 7 tasks = 84 CSVs, plus a `synthetic_manifest.json` with summary stats (`svm_cv_pct`, `jerk_mean`, `gsr_mean`, `hr_mean` per file).

The detailed design rationale is in [`wiki/methods/synthetic_data_v0_rules.md`](synthetic_data_v0_rules.md).

## Why this might not be right

1. **No real AD-stage labeled wearable corpus to validate against.** The degradation parameters are extrapolated from cross-sectional gait studies (Buracchio 2010, Montero-Odasso 2019) and physiological reasoning, not from within-subject longitudinal AD recordings. There is no TSTR (train-synthetic, test-real) score because there is no comparable real test set.
2. **Source population mismatch.** Baselines are healthy young adults (S01–S04), not age-matched older adults. Overlaying AD-progression deltas on a young baseline implicitly assumes the disease degrades in the same *direction* a healthy elder differs from a healthy young adult — which is not obviously true.
3. **Cross-modal coupling is hand-engineered.** Real AD progression has *correlated* degradations across EDA / PPG / IMU (e.g., autonomic decline + gait slowing + sleep disruption co-occur). The v0 generator parameterizes each modality somewhat independently. Di Martino 2025 (cited in the methods landscape) explicitly warns that cross-modal consistency is the core challenge of multimodal synthetic biosignal data.
4. **Stage discreteness.** The generator emits MCI / mild / moderate as three discrete labels. Real AD is a continuum and the boundaries between stages are graded, not categorical.
5. **BPSD events are templated, not learned.** The BPSD overlays use mean-shift parameters derived from Iaboni 2022 and Valenza 2018 — both Western nursing-home cohorts, both small (n=48). Whether agitation in Chinese community-dwelling AD has the same EDA/HR signature is unknown.
6. **No face-validity review yet.** [李医生](../entities/li_doctor.md) has not yet inspected sample synthetic recordings. Until that happens, the synthetic data has no clinical sign-off.

## What we'd need to verify it

- **TSTR score** against any held-out real AD wearable dataset. Candidates if accessible: TIHM, ContinUse, or any open-share AD wearable corpus. None are currently in `raw/`.
- **Expert face-validity** with [李医生](../entities/li_doctor.md): show a small sample of synthetic + real recordings, ask for blind plausibility scoring.
- **Statistical parity** against published distributional summaries from real AD studies (where individual data isn't available, summary stats often are — gait variability, HRV ranges, etc.).
- **Cross-modal coherence checks** — do the degradations co-vary across modalities the way real disease progression does?

## Candidate next directions

Listed without ranking; the choice is the user's:

a. **Demote v0 to placeholder.** Use v0 only as plumbing for pipeline development (testing agent code, integration tests). Do not train any classifier on it. Replace before any clinical inference.

b. **Restrict to negative / control samples.** Use the *baseline* portions only (no AD-stage overlays) as healthy controls; abandon the synthetic AD-stage variants until a real labeled corpus is available.

c. **Replace with literature-derived priors.** Use distributional priors from published AD wearable studies (e.g., Iaboni 2022, Buracchio 2010 for gait) as informed Bayesian priors on a smaller set of generated samples — not as point-estimate degradations.

d. **Phase-up to a learned approach.** Once real data exists (even small), use TimeGAN / diffusion models conditioned on real samples; current methods landscape page tracks the relevant literature: [`wiki/methods/synthetic_data_methods_landscape.md`](synthetic_data_methods_landscape.md).

e. **Keep the pipeline, change the framing.** Present v0 as a *stress-test generator for the agent system* (does the multi-agent reasoning hold up under noisy, parameterized inputs?), not as training data.

## Decision

**Open. Owner: user. Deadline: TBD.**

Until this is closed, all pages derived from v0 carry `status: working_hypothesis` and link back here.

## Log

- **2026-04-25** — registered as open question by user during AD/ → AD WIKI/ migration. No decision made.
