---
title: Language-cognitive agent
type: agent
last_updated: 2026-04-25
sources:
  - code/src/agents/language_cognitive_agent.py
  - wiki/concepts/voice_acoustic_linguistic.md
status: draft
---

# Language-cognitive agent

Clinical role: cognitive evaluator + speech-language therapist.

## Inputs

Microphone — acoustic features (F0, jitter, shimmer, MFCC, speech rate) + linguistic features (TTR, pause rate, semantic coherence, information density).

## Core capabilities

- Acoustic feature extraction and analysis.
- Linguistic feature analysis (TTR, pause rate, semantic coherence, information density).
- Chinese / dialect ASR (Whisper large-v3 + 讯飞 fallback).
- Cookie-Theft-equivalent picture description scoring.
- Longitudinal language-change tracking — cross-session deltas.

## Outputs

Language-cognitive assessment, semantic-memory decline indicators, language-functional staging.

## KB used

- [Audio markers](../concepts/voice_acoustic_linguistic.md) — [`code/kb_loader/data/sensors/audio_markers.json`](../../code/kb_loader/data/sensors/audio_markers.json)
- TAUKADIAL 2024 / ADReSS baseline references in [related work positioning](../synthesis/related_work_positioning.md).

## Privacy posture

On-device feature extraction only. Raw audio is not stored or transmitted. See [imperial_data_management.md](../deliverables/ethics/imperial_data_management.md).

## Code

[`code/src/agents/language_cognitive_agent.py`](../../code/src/agents/language_cognitive_agent.py) — stub.

## Status

Stub. ASR pipeline prototype exists in [`raw/code_archives/esp32-audio-ai-main/`](../../raw/code_archives/esp32-audio-ai-main/).
