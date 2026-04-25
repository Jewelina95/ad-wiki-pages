---
title: Motor-cognitive agent
type: agent
last_updated: 2026-04-25
sources:
  - code/src/agents/motor_cognitive_agent.py
  - wiki/concepts/imu_gait.md
  - wiki/concepts/mcr_criteria.md
  - wiki/concepts/gait_norms.md
status: future
---

> 🌙 **Status: future / 暂缓.**
> 当前阶段一个统一的 [Clinical analysis agent](unified_clinical_agent.md) 已经够用——单 prompt + 知识库查询，规模上来或要做亚专科深度时再拆成这个独立 Agent。详见 [_architecture.md](_architecture.md)。

---

# Motor-cognitive agent

Clinical role: rehab specialist + cognitive evaluator.

## Inputs

IMU features — gait params, dual-task cost, hand fine motor, hand tremor.

## Core capabilities

- Gait analysis with cognitive-function inference.
- [MCR criteria](../concepts/mcr_criteria.md) evaluation (gait + subjective complaint, no scales required).
- Dual-task paradigm scoring (DTC).
- Fall-risk assessment.
- Hand tremor characterization (AD vs PD differential support).

## Outputs

Motor-cognitive assessment, MCR risk score, fall-risk level.

## KB used

- [IMU markers](../concepts/imu_gait.md) — [`code/kb_loader/data/sensors/imu_markers.json`](../../code/kb_loader/data/sensors/imu_markers.json)
- [Gait norms](../concepts/gait_norms.md) — [`code/kb_loader/data/clinical/gait_norms.json`](../../code/kb_loader/data/clinical/gait_norms.json)
- [MCR criteria](../concepts/mcr_criteria.md)

## Code

[`code/src/agents/motor_cognitive_agent.py`](../../code/src/agents/motor_cognitive_agent.py) — stub.

## Status

Stub. The strongest published evidence is for this Agent's domain (gait pre-clinical signal up to 12 yr pre-MCI, Buracchio 2010), so it is also the most likely first implementation target.
