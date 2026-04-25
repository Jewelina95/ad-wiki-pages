# AD WIKI — Log

Append-only chronological journal. New entries go at the bottom. Format: `## [YYYY-MM-DD] kind — slug`.

---

## [2026-04-25] migration — AD/ → AD WIKI/

- Restructured `/Users/wenshaoyue/Desktop/research/AD/` into `/Users/wenshaoyue/Desktop/research/AD WIKI/` following the [Karpathy 3-layer wiki framework](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
- Layers: `raw/` (immutable sources), `wiki/` (curated markdown), plus pragmatic `code/` and `_admin/` partitions. Top-level governance: [`README.md`](README.md), [`index.md`](index.md), [`schema.md`](schema.md), this `log.md`.
- Source `AD/` directory left **untouched** — non-destructive copy.
- Migrated: ~30 authored markdown docs, 7 PDFs (deduped), 10 xlsx clinical, 81 + 12 sensor CSVs, 4 Imperial DOCX (extracted to MD via pandoc), 4 ethics docx forms (extracted), 4 funding docx + 1 PDF, IIT template, ESP32 audio prototype.
- Generated ~40 new wiki pages: 6 entities, 16 concepts (including 7 BPSD per-symptom), 9 agents, 6 synthesis, 5 datasets, 2 methods, plus README/index/schema/log.
- Front-matter retrofitted on 35 migrated markdown files; new pages already carried it.

### Open question registered

- **#1 Synthetic data pipeline validity** — flagged by user (*"关于这个合成数据你也可以重新去思考不一定就是正确的"*). The v0 rule-based degradation engine is treated as a `working_hypothesis` until validated. CSVs in `raw/sensor_data/synthetic_4.8/` and `raw/sensor_data/synthetic_v0/` are preserved as artifacts. See [`wiki/methods/synthetic_data_review.md`](wiki/methods/synthetic_data_review.md) and [`wiki/synthesis/what_we_dont_know.md`](wiki/synthesis/what_we_dont_know.md).
- 4 additional pre-existing gaps registered in the open-questions ledger: BPSD-cohort generalization (#2), agent stub→implementation gap (#3), wearable+clinical data overlap empty (#4), glove hardware not fabricated (#5).

### Skipped

- `__pycache__/`, `*.pyc`, `.DS_Store` — never copied.
- Duplicate `memory_loss…(1).pdf` — kept the non-`(1)` copy.
- `esp32-audio-ai-main.zip` and `src/sensors.zip` — folders already extracted.
- `数据库汇总2026.4.18.rar` — folder already extracted.

### Not addressed in this migration

- Resolving open question #1 — only registered.
- Translating Chinese content.
- Refactoring or implementing any agent stub.
- Recomputing analyses (`normal_reference_ranges.csv` etc.).
- No remote push, no S3, no GitHub.
