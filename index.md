# AD WIKI Public — Index

Last updated: 2026-04-25 · Public-facing index. Catalog of every page in this mirror, by category. ⚠ marks `working_hypothesis` or `open_question` status.

## Concepts

### Disease

- [AD staging](wiki/concepts/ad_staging.md)
- [AT(N) framework](wiki/concepts/atn_framework.md)
- [Amyloid hypothesis](wiki/concepts/amyloid_hypothesis.md)
- [BPSD](wiki/concepts/bpsd.md) — umbrella; per-symptom pages below
  - [Agitation](wiki/concepts/bpsd_agitation.md), [Anxiety](wiki/concepts/bpsd_anxiety.md), [Apathy](wiki/concepts/bpsd_apathy.md), [Depression](wiki/concepts/bpsd_depression.md), [Sleep disorder](wiki/concepts/bpsd_sleep_disorder.md), [Sundowning](wiki/concepts/bpsd_sundowning.md), [Wandering](wiki/concepts/bpsd_wandering.md)
- [MCR criteria](wiki/concepts/mcr_criteria.md)
- [Gait norms](wiki/concepts/gait_norms.md)
- [AD medications](wiki/concepts/medications_ad.md)

### Sensor

- [EDA signal](wiki/concepts/eda_signal.md)
- [PPG / HRV](wiki/concepts/ppg_hrv.md)
- [IMU / gait](wiki/concepts/imu_gait.md)
- [Voice — acoustic + linguistic](wiki/concepts/voice_acoustic_linguistic.md)
- [Glove form factor](wiki/concepts/glove_form_factor.md)

## Methods

- [Data pipeline](wiki/methods/data_pipeline.md)
- [Preprocessing per modality](wiki/methods/preprocessing_per_modality.md)
- [Agent data loader interface](wiki/methods/agent_data_loader_interface.md)
- [Synthetic data v0 rules](wiki/methods/synthetic_data_v0_rules.md) ⚠ working hypothesis
- [Synthetic data review](wiki/methods/synthetic_data_review.md) ⚠ open question
- [Synthetic methods landscape](wiki/methods/synthetic_data_methods_landscape.md)
- [Claude CLI inference pattern](wiki/methods/claude_cli_inference_pattern.md)

## Agents

- [Architecture overview](wiki/agents/_architecture.md)
- [Master coordinator](wiki/agents/master_coordinator.md)
- [Motor-cognitive](wiki/agents/motor_cognitive_agent.md)
- [Language-cognitive](wiki/agents/language_cognitive_agent.md)
- [Autonomic](wiki/agents/autonomic_agent.md)
- [Emotion-behavior](wiki/agents/emotion_behavior_agent.md)
- [Clinical diagnosis](wiki/agents/clinical_diagnosis_agent.md)
- [Intervention](wiki/agents/intervention_agent.md)
- [Care management](wiki/agents/care_management_agent.md)

## Synthesis

- [Project overview](wiki/synthesis/project_overview.md)
- [Why glove](wiki/synthesis/why_glove.md)
- [Clinical → sensor mapping](wiki/synthesis/clinical_to_sensor_mapping.md)
- [Innovation thesis](wiki/synthesis/innovation_thesis.md)
- [Related work positioning](wiki/synthesis/related_work_positioning.md)
- [Expert KB report](wiki/synthesis/expert_kb_report.md)
- [KB optimization report](wiki/synthesis/kb_optimization_report.md)
- [What we don't know](wiki/synthesis/what_we_dont_know.md) ⚠

## Datasets (structure only — no patient data)

- [Baseline 4.8](wiki/datasets/baseline_4.8.md)
- [Synthetic 4.8](wiki/datasets/synthetic_84.md) ⚠
- [Pilot 3.20](wiki/datasets/pilot_3.20.md)
- [Pilot 3.30](wiki/datasets/pilot_3.30.md)
- [Clinical xlsx 2026-04-18](wiki/datasets/clinical_xlsx_2026-04-18.md)

## Governance

- [README](README.md), [schema](schema.md), [log](log.md)

## Not in this public mirror

The following sections live only in the private source repo:

- `entities/` — clinical collaborators and study participants by name
- `meetings/` — internal meeting records
- `deliverables/` — funding and ethics application drafts
- `raw/` — papers (copyright), patient xlsx, sensor CSVs, interview transcripts
- `code/` — implementation
