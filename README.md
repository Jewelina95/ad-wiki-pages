# AD WIKI — Public mirror

📊 **Live dashboard:** https://jewelina95.github.io/ad-wiki-pages/

A public, curated mirror of the AD wearable glove research wiki. Internal documents (entities with personal names, meeting notes, funding/ethics drafts, raw data, code) live in a separate private repo and are not mirrored here.

## What this is

A research project on Alzheimer's disease early detection using a multi-sensor wearable glove (EDA + PPG + IMU + microphone) and a multi-agent reasoning system. The wiki captures the project's clinical reasoning, sensor methodology, agent architecture, and synthesis essays in a [Karpathy-style](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) three-layer wiki.

## What's in this mirror

- ✅ **`wiki/concepts/`** — domain knowledge: AD staging, AT(N), BPSD (7 symptoms), MCR, sensor signals (EDA / PPG / IMU / voice), gait norms, medications
- ✅ **`wiki/methods/`** — data pipeline, preprocessing, agent data interface, synthetic data v0 + review, methods landscape
- ✅ **`wiki/agents/`** — 7-specialist + 1-coordinator architecture
- ✅ **`wiki/synthesis/`** — cross-cutting essays: project overview, why glove, clinical-to-sensor mapping, innovation thesis, what we don't know
- ✅ **`wiki/datasets/`** — descriptions of data corpora structure (no patient data)
- ✅ **`schema.md` / `log.md`** — wiki governance and timeline

## What's not in this mirror

- ❌ Personal entities (clinical collaborators, study participants by name)
- ❌ Internal meeting notes
- ❌ Unsubmitted funding / ethics application drafts
- ❌ Raw sensor data, clinical xlsx, paper PDFs (copyright + privacy)
- ❌ Implementation code

## Auto-update

The dashboard at https://jewelina95.github.io/ad-wiki-pages/ regenerates **automatically** on every push via GitHub Actions. Modify any `wiki/**/*.md` and the live site reflects within ~1 minute.

## Browse locally

```bash
./view.sh
```

Starts a local HTTP server and opens the dashboard with inline markdown rendering (links open in modal panels).

## Status flags on pages

- `settled` — claims are stable, validated by sources
- `draft` — provisional, page incomplete
- `working_hypothesis` — model/design that may be wrong; links to corresponding open question
- `open_question` — unresolved; lives in [`wiki/synthesis/what_we_dont_know.md`](wiki/synthesis/what_we_dont_know.md)

The synthetic data pipeline (v0) is registered as an **open question** as of 2026-04-25 — see [`wiki/methods/synthetic_data_review.md`](wiki/methods/synthetic_data_review.md).
