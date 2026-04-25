---
title: Voice — acoustic and linguistic features
type: concept
last_updated: 2026-04-25
sources:
  - code/kb_loader/data/sensors/audio_markers.json
  - wiki/concepts/_source_sensor_signal_principles.md
status: settled
---

# Voice — acoustic and linguistic features

The microphone is the only modality that captures *language* directly, which is where some of the earliest AD-related changes show up (potentially decades pre-clinical).

## Acoustic features

- F0 (pitch), jitter, shimmer, harmonics-to-noise ratio.
- MFCCs.
- Speech rate, pause rate, voiced/unvoiced ratio.

## Linguistic features (from ASR transcript)

- TTR (type-token ratio) — vocabulary diversity.
- Pause rate, filler rate.
- Semantic coherence (sentence-to-sentence cosine similarity).
- Information density (proposition count per utterance).
- Syntactic complexity (parse depth, dependency length).

## AD relevance

- **Speech rate decline** is an early marker — >15% slowdown vs. personal baseline is an SCD-stage signal; >25% indicates MCI-level change (Luz 2020 ADReSS, TAUKADIAL 2024).
- Cookie-Theft-equivalent picture description: AUC >0.85 for AD detection in English (ADReSS), 0.78–0.85 in Chinese (TAUKADIAL 2024).
- Mechanism: temporal-lobe atrophy → word retrieval; frontal → organization; hippocampus → working memory.
- Window: language changes can be detectable up to **10 years pre-diagnosis**.

## Pipeline

ASR: Whisper large-v3 + 讯飞 ASR fallback for Chinese / dialect.
Linguistic feature extraction: [`code/src/sensors/`](../../code/src/sensors/) (in progress).

## Caveats

- Privacy: continuous audio is the most invasive modality. The plan is **on-device feature extraction only** — raw audio never leaves the glove. Consent flow handles this explicitly — see [`wiki/deliverables/ethics/imperial_data_management.md`](../deliverables/ethics/imperial_data_management.md).
- Chinese/dialect ASR error rates remain higher than English; affects linguistic features more than acoustic.

## Used by

[Language-cognitive agent](../agents/language_cognitive_agent.md), [Emotion-behavior agent](../agents/emotion_behavior_agent.md) (prosody for emotion).

## Source

[`code/kb_loader/data/sensors/audio_markers.json`](../../code/kb_loader/data/sensors/audio_markers.json).
