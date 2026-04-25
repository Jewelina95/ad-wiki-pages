---
title: Master Coordinator
type: agent
last_updated: 2026-04-25
sources:
  - code/src/agents/master_coordinator.py
  - wiki/agents/_architecture.md
status: draft
---

# Master Coordinator

Role: MDT chair. Integrates specialist assessments, resolves conflicts, produces the final reasoning chain.

## Inputs

All specialist `AgentAssessment` outputs + `PatientProfile` + `ContextInfo` + recent history.

## Outputs

Integrated assessment + auditable reasoning chain. Final alert level is the coordinator's, not any specialist's.

## Conflict-arbitration heuristics

When specialists disagree, prompt encodes (TBD, will follow MDT meeting practice from [李医生 interview](../entities/li_doctor.md)):

- Higher-confidence specialist wins on their domain (autonomic agent on HRV).
- Cross-domain conflicts (e.g., autonomic says decline, emotion says agitation) → resolve via context (`is_sundowning_window`, recent activity, medication taken today).
- Yellow + Yellow ≠ Red unless context corroborates.
- Red from any agent escalates unless specifically downgraded by clinical diagnosis agent.

## Code

[`code/src/agents/master_coordinator.py`](../../code/src/agents/master_coordinator.py) — stub.

## Status

Stub. See [open question #3](../synthesis/what_we_dont_know.md).
