# UGHN-Y3-E-L

Group coursework repository — **UESTC-Hainan (格拉斯哥海南学院), CW1HN015 *Engineering & Law*, Coursework 1**.

## What this repository is

This repository holds the team's working materials for the **Product Development & Marketing** assignment: a Product Requirements Document (PRD) plus business and marketing analysis for **ID-Coo**, a cow-identification verification and anomaly-diversion system for dairy farms in the North of England (target breed: Holstein Friesian).

The report follows the course template (Cadmus Steps 1–15, sections R1–R13, ≈5,600 words + 2 A3 canvases + 3 tables + IEEE references) and is assessed against the published marking criteria (100 marks total, split evenly across five parts of 20 marks each).

## Team structure (5 members × 20%)

| Part | Scope | Sections | Owner |
|---|---|---|---|
| Part 1 | Problem & customer (DISCOVER) | R1 EID/LIS constraints · R2 consequences of misidentification · R3 Value Proposition Canvas | Member 1 |
| Part 2 | Differentiation (DEFINE) | R4 POP/POD · R5 competitive analysis (2 tools) · R6 USP | Member 2 |
| Part 3 | Business model & market (MODEL) | R7 Business Model Canvas · R8 critical analysis | Member 3 |
| Part 4 | Design & requirements (DESIGN) | R9 user requirements (MoSCoW) · R10 technical description | Member 4 |
| Part 5 | Validation & delivery (VALIDATE + DELIVER) | R11 sustainability · R12 affordability · R13 references (IEEE) + final assembly | Member 5 |

Cross-roles: Member 1 — project coordination & minutes; Member 2 — competitor evidence; Member 3 — single source of truth for all numbers; Member 4 — figures & diagrams; Member 5 — editing, IEEE referencing, declarations.

## Repository layout

```
01_课程要求/      Assignment brief, marking criteria, report template (originals)
02_参考模板/      Reference materials (VPC/BMC templates, lecture resources)
03_方案与报告/     Earlier plans (superseded by the current ID-Coo concept, kept for record)
06_图表/          Figure scripts and outputs
07_待归档/        Archived materials unrelated to the current assignment
08_组员资料/       Team charter: requirements & work split, cattle diversion scheme,
                 full report draft, and Member 4 deliverables (R9/R10 finals + figures
                 + Cadmus entry worksheet + handover notes)
文献调研/         Reference library (verified downloads + index with R13 mapping)
翻译/             Chinese translations of course materials
build_*.py        Figure/report generation scripts (run from repo root)
ID-Coo_Cadmus录入工作稿_完整模板.md / .docx   Full team entry template (see below)
```

## Key artefacts

- **`08_组员资料/ID-Coo_项目要求与五人分工.md`** — the authoritative team charter: hard constraints from the brief, section-to-marks mapping, division of labour, gates and submission checklist.
- **`08_组员资料/牛只分流方案(1).md`** — the current technical scheme: single-file race → single-animal buffer → detection section → dual-exit diversion, LF-RFID + ultrasonic occupancy sensing, rule-based state machine, review pen.
- **`08_组员资料/成员4_Part4_交付/`** — Member 4's finished sections: R9 (10 Must-have user requirements) and R10 (technical description, ≈1,500 words + 2 figures), each in English final + Chinese reading copy, plus a per-section Cadmus entry worksheet with rewrite prompts.
- **`ID-Coo_Cadmus录入工作稿_完整模板.md` / `.docx`** — the full-team entry template extending Member 4's worksheet format to all sections R1–R13 and both declarations: word/page limits, hard format rules, structural scaffolds and self-check lists per section.

## Working conventions (agreed in the team charter)

1. **Type directly into Cadmus.** Report body text must be entered directly in Cadmus by its owner — pasting from Word/Google Docs (or depositing pre-written text via auto-typing tools) is a red line. The entry template is a scaffold to type from, not a source to paste.
2. **AI as critical friend only.** AI may challenge assumptions, find logic gaps and check structure; it must not produce substantive writing. Any AI assistance is declared truthfully in the Declaration of Originality.
3. **Single source of truth for numbers.** All market data, unit prices and cost figures follow Part 3. The three price points — **£18,500 installation / £720 annual service / £60 annual energy** — must be identical everywhere they appear.
4. **References.** IEEE numeric style, 15–30 entries, R13 list maintained by Member 5; new sources are registered there first and then cited by number.
5. **Alignment chain.** R9 traces to R2/R3 pains → R10 aligns with the USP (R6) and pricing (R7/R12) → R11 reviews the R10 design → R12 uses the R10 cost model. A break in any link costs marks in 2–3 sections.

## Current status (2026-10-14)

- R9 and R10 (Member 4) are complete in English final form with verified citations (Tru-Test XRP2 guide, Arrowquip specifications, CIGR Holstein-Friesian body dimensions, Dairy Roadmap).
- Reference library verified: XRP2 quickstart guide re-downloaded after the Tru-Test site migration (R13 entry [12] URL needs updating to the new resource page).
- R1–R8, R11–R13 are in progress by their owners using the full entry template.

## Notes

- Course lecture decks (`08_组员资料/E&L_PPT/`) are excluded from version control (copyright + file-size limits); they are kept locally by each member.
- The repository is private and shared among the five team members.
