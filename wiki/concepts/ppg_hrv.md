---
title: PPG, HR, and HRV
type: concept
last_updated: 2026-04-25
sources:
  - code/kb_loader/data/sensors/ppg_markers.json
  - wiki/concepts/_source_sensor_signal_principles.md
status: settled
---

# PPG — photoplethysmography (HR / HRV / SpO₂)

Optical pulse signal at the wrist or palm. Yields HR, HRV (time- and frequency-domain), and SpO₂.

## Features (Task Force 1996 standards)

| Domain     | Feature           | Interpretation                                  |
|------------|-------------------|--------------------------------------------------|
| Time       | SDNN              | Overall HRV (sympathetic + parasympathetic)      |
| Time       | RMSSD             | Parasympathetic (vagal) tone                    |
| Frequency  | LF (0.04–0.15 Hz) | Mixed sympathetic + parasympathetic              |
| Frequency  | HF (0.15–0.4 Hz)  | Parasympathetic                                  |
| Ratio      | LF/HF             | Sympathovagal balance                            |
| Pulse-ox   | SpO₂              | Saturation (sleep apnea screening)               |

## AD relevance

- **HRV decline:** SDNN and RMSSD persistently decrease as vagal tone drops (Collins 2012). Independent risk factor for AD.
- **Differential diagnosis:** AD shows moderate HRV decline; DLB shows severe decline — useful for AD vs. DLB.
- **Mechanism:** vagal pathway degeneration, insula early-Tau, cholinergic system peripheral readout.

## Project-specific thresholds (from KB)

| Marker             | Warning           | Critical          |
|--------------------|-------------------|-------------------|
| SDNN (vs baseline) | drop >20%         | absolute SDNN <50 ms |
| RMSSD (vs baseline)| drop >25%         | —                  |
| LF/HF             | rise >30%          | absolute >3.0     |

Source: [`code/kb_loader/data/sensors/ppg_markers.json`](../../code/kb_loader/data/sensors/ppg_markers.json).

## Caveats

- Wrist PPG is motion-sensitive; quality drops during walking. Confidence-weight HRV by motion state.
- Sleep-stage inference from PPG+IMU is inferential, not polysomnographic.

## Used by

[Autonomic agent](../agents/autonomic_agent.md), [Emotion-behavior agent](../agents/emotion_behavior_agent.md), [Clinical diagnosis agent](../agents/clinical_diagnosis_agent.md).
