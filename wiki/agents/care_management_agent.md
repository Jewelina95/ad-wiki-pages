---
title: Care management agent
type: agent
last_updated: 2026-04-25
sources:
  - code/src/agents/care_management_agent.py
status: draft
---

# Care management agent

Clinical role: GP + care coordinator + nursing + social work.

## Inputs

All other agents' outputs + patient profile + caregiver profile.

## Core capabilities

- Daily / weekly report assembly for caregivers and clinicians.
- Caregiver alert triage (what is urgent vs. trend-worthy?).
- Care-plan adherence tracking (medications taken, appointments attended).
- Resource routing (when to escalate to in-person clinic).
- Caregiver-burden monitoring (long-running stress indicators).

## Outputs

Caregiver-facing reports (plain language), clinician-facing summaries (clinical), alert escalations.

## Code

[`code/src/agents/care_management_agent.py`](../../code/src/agents/care_management_agent.py) — stub.

## Status

Stub. Closest to a "product" agent — its output is what end users see, so prompt engineering for tone and clarity matters more here than for internal specialist agents.
