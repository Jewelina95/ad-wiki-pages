---
title: EDA — electrodermal activity
type: concept
last_updated: 2026-04-25
sources:
  - code/kb_loader/data/sensors/eda_markers.json
  - wiki/concepts/_source_sensor_signal_principles.md
  - raw/papers/_synthetic_methods_review.docx
status: settled
---

# EDA — electrodermal activity

Skin conductance, driven by sympathetic-cholinergic eccrine sweat-gland activity. The most direct peripheral readout of sympathetic arousal available to a wearable.

## Features

| Feature  | What it measures                                    |
|----------|-----------------------------------------------------|
| SCL      | Skin conductance level (tonic baseline)            |
| SCR      | Phasic skin conductance responses (events)          |
| NS-SCR   | Non-specific SCR rate (per minute)                 |

Decomposition typically via `cvxEDA` or `Ledalab`.

## AD relevance

- **Autonomic decline:** chronic SCL changes track autonomic dysregulation (insula / amygdala–insula circuit early Tau deposition).
- **BPSD detection:** EDA + HR + activity is the most robust multimodal signature of agitation (AUC ~0.87, Iaboni 2022 individualized models AUC 0.80–0.95).
- **Emotional reactivity:** SCR amplitude in response to triggers can be diminished in apathy, exaggerated in anxiety/agitation.

## Caveats

- Strong individual variation — group-level cutoffs are weak; **individualized baseline + relative change** outperforms population thresholds.
- Sweat-gland density on the finger is high (good signal), but motion artifacts and contact pressure matter.
- Evidence level for AD-specific EDA changes alone is C; strength comes from multimodal combinations.

## Implementation pointers

- Glove placement: finger pad. See [glove form factor](glove_form_factor.md).
- Preprocessing: [`wiki/methods/preprocessing_per_modality.md`](../methods/preprocessing_per_modality.md).
- Used by: [Autonomic agent](../agents/autonomic_agent.md), [Emotion-behavior agent](../agents/emotion_behavior_agent.md).
- KB: [`code/kb_loader/data/sensors/eda_markers.json`](../../code/kb_loader/data/sensors/eda_markers.json).
