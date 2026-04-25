---
title: Autonomic agent
type: agent
last_updated: 2026-04-25
sources:
  - code/src/agents/autonomic_agent.py
  - wiki/concepts/ppg_hrv.md
  - wiki/concepts/eda_signal.md
status: draft
---

# Autonomic agent

Clinical role: neurology.

## Inputs

PPG (HR, HRV, SpO₂) + EDA (SCL, SCR, NS-SCR).

## Core capabilities

- HRV time- and frequency-domain analysis (SDNN, RMSSD, LF/HF) per Task Force 1996.
- Sympathovagal balance assessment.
- Indirect cholinergic-system function readout.
- Sleep-wake rhythm inference (PPG + IMU activity).
- Circadian-rhythm disruption detection.

## Outputs

Autonomic-function assessment, sleep-quality report, circadian state.

## KB used

- [PPG markers](../concepts/ppg_hrv.md) — [`code/kb_loader/data/sensors/ppg_markers.json`](../../code/kb_loader/data/sensors/ppg_markers.json)
- [EDA markers](../concepts/eda_signal.md) — [`code/kb_loader/data/sensors/eda_markers.json`](../../code/kb_loader/data/sensors/eda_markers.json)

## Differential

- AD: moderate HRV decline.
- DLB: severe HRV decline (helps distinguish).
- See [PPG/HRV concept page](../concepts/ppg_hrv.md).

## Code

[`code/src/agents/autonomic_agent.py`](../../code/src/agents/autonomic_agent.py) — stub.

## Status

Stub.
