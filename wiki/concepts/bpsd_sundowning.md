---
title: BPSD — Sundowning
type: concept
last_updated: 2026-04-25
sources:
  - code/kb_loader/data/clinical/bpsd/sundowning.json
status: settled
---

# Sundowning (日落综合征)

Late-afternoon / early-evening (4–6 PM typical) onset of confusion, agitation, anxiety, restlessness. Classical pattern in moderate AD.

## Sensor signature

A *temporal* pattern, not a single threshold:

- Gradual EDA SCL rise across 4–6 PM window
- HR baseline drift upward
- Increased restlessness / step variability
- Possible voice tension changes

The [Master coordinator](../agents/master_coordinator.md) treats sundowning as a context flag (`is_sundowning_window`) that biases other agents' interpretation of arousal signals.

## Why this is multimodal-only

A point-in-time HR or EDA value cannot identify sundowning — only the *trajectory across the window* does. This is the canonical example of why time-of-day context is required.

## Intervention

Light therapy, environmental cues (consistent dinner / evening routine), reduced stimulation. See [Intervention agent](../agents/intervention_agent.md).

KB: [`code/kb_loader/data/clinical/bpsd/sundowning.json`](../../code/kb_loader/data/clinical/bpsd/sundowning.json). Umbrella: [BPSD](bpsd.md).
