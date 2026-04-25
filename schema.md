# AD WIKI — Schema

This document governs how the wiki is maintained. It is itself a wiki page, but
it has authority: when in doubt, follow the rules here.

## Three layers

1. **`raw/`** — immutable. Files here are sources of record. Once placed, do
   not edit; if a paper or interview is updated, place the new version with a
   new date suffix and add a [`log.md`](log.md) entry.
2. **`wiki/`** — curated. Markdown only. Pages are short, cross-linked, and
   may be rewritten freely. Each page has front-matter (see below).
3. **`code/`** — implementation. **Not part of the wiki contract.** The wiki
   may reference code paths as evidence; code lives by software-engineering
   rules, not wiki rules.

Plus `_admin/` for operational items (reimbursement, etc.) — outside the wiki.

## Two special files

- **[`index.md`](index.md)** — content catalog. Updated on every ingest.
  Organized by category, not chronology.
- **[`log.md`](log.md)** — chronological journal. Append-only. One section per
  event, starting with `## [YYYY-MM-DD] kind — slug`.

## Operations

### Ingest (new source → wiki updates)

1. Place the source into `raw/<category>/<date_or_slug>`.
2. Read it; identify entities, concepts, methods touched.
3. Update or create relevant wiki pages, linking back to the raw file.
4. Update `index.md` if a new page was created.
5. Append a log entry: `## [YYYY-MM-DD] ingest — <slug>`.

### Query (answer a question against the wiki)

1. Search wiki pages first; raw only if wiki is incomplete.
2. Synthesize with citations to wiki pages and raw files.
3. If the answer is novel and worth keeping, file it as a new wiki page (most
   likely under `synthesis/`) and add to `index.md`. Append a `## [YYYY-MM-DD]
   query — <slug>` log entry.

### Lint (health check)

Run periodically. Surface:

- Orphan pages (not linked from `index.md` or any other page).
- Dead cross-links.
- Pages with `status: working_hypothesis` older than 60 days — surface for
  review.
- Pages with `status: open_question` — re-confirm or resolve.
- Concept pages with no source citations.
- Datasets with no corresponding wiki page.

## Conventions

### Dates

`YYYY-MM-DD`. Always. No relative dates ("last Thursday") in wiki content.

### Slugs

`lower_snake_case` in English, even for Chinese-titled pages. Titles inside the
file may be in Chinese. This makes paths stable across renames and keeps
cross-link breakage low.

### Cross-links

Relative paths from the linking file. Always

```
[label](path/to/page.md)
```

— the path is resolved relative to the linking file.

### Front-matter

Every `wiki/**/*.md` file starts with a YAML front-matter block:

```yaml
---
title: <human-readable, original language ok>
type: entity | concept | method | agent | synthesis | dataset | meeting | deliverable
last_updated: YYYY-MM-DD
sources:
  - raw/papers/foo.pdf
  - wiki/concepts/bar.md
status: settled | draft | working_hypothesis | open_question
---
```

`title` is freeform. `sources` is best-effort but should not be empty.

### Status semantics

- `settled` — claims on this page are stable, validated by source(s).
- `draft` — claims are provisional, page is incomplete or recently created.
- `working_hypothesis` — page contains a model or design that *may* be wrong.
  Must link to the corresponding `open_question` page.
- `open_question` — page is itself an unresolved question. Lives in the
  open-questions ledger ([`wiki/synthesis/what_we_dont_know.md`](wiki/synthesis/what_we_dont_know.md)).

### Synthetic data special rule

Until [open question #1](wiki/synthesis/what_we_dont_know.md) resolves: any
page derived from `synthetic_data_*` carries `status: working_hypothesis` and
links to [`wiki/methods/synthetic_data_review.md`](wiki/methods/synthetic_data_review.md).

## What does not belong in the wiki

- Reimbursement, invoices, admin → `_admin/`.
- Build artifacts, caches, zips of folders that are already unzipped.
- Code-internal docstrings (those live in `code/`).
- Ephemeral conversation context, session-specific scratch.
- Translated copies of pages that already exist in another language — link
  instead, don't duplicate.

## When the original `AD/` and `AD WIKI/` diverge

The original `/Users/wenshaoyue/Desktop/research/AD/` was the source for this
wiki at migration time (2026-04-25). It is left untouched. If the user adds
new files there afterward, they should be ingested into `AD WIKI/raw/` and the
appropriate wiki pages updated. The original is *not* the live working
directory after this migration; this wiki is.
