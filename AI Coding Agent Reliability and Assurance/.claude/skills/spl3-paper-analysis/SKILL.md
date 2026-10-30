---
name: spl3-paper-analysis
description: Analyse the student's SPL3 papers (AI Coding Agent Reliability and Assurance) into Bangla Word documents with the 22-section template, at minimum token cost. Use for "next sub-domain", "analyse these papers", or any paper analysis/summary in this project.
---

# SPL3 Paper Analysis — lean workflow

Goal: same quality as before, far fewer tokens. Every token spent must change the output.

## Paths
- Root: `E:\Course Book and Slide\4th Year\SPL3\Papers\AI Coding Agent Reliability and Assurance`
- Output: `Analysis\0N_<Subdomain>\0K_<Name>_Analysis.md` (+ `.docx`), summary `00_Subdomain_Summary.md`
- Index: `Analysis\00_Index_and_Plan.md` (reading order, status column)
- Agent brief: `brief.md` (this folder) — paste into each agent prompt, fill the `{…}` fields
- Context digest: `context.md` (this folder) — the ONLY prior-context file agents read
- Tools: `Analysis\_tools\md2docx.py`, `Analysis\_tools\finalize_docx.ps1`

## Workflow (orchestrator)
1. Extract each PDF once: copy to `<scratchpad>\tN\pK.pdf`, `pdftotext -layout` to `pK.txt`. Print only title + word count; do not read abstracts yourself.
2. Launch one agent per paper in a single message, `model: "sonnet"`, prompt = `brief.md` with fields filled. Do not add extra context.
3. On each report: verify 2–3 headline numbers with one `grep` on `pK.txt`. Render a PDF page to an image ONLY if the agent says a table was garbled AND the numbers drive a conclusion.
4. Write the sub-domain summary yourself, ≤ 150 lines, from the agent reports (not by reading the analyses). Then append the new CGs/direction change to `context.md` (keep it ≤ 80 lines).
5. Build all files in one PowerShell call: `md2docx.py <md> <docx> --toc` then `finalize_docx.ps1 -Docx <docx>` (no `-Pdf` unless a page check is needed). Fix only reported problems.
6. Update the index status row. Messages to the user: short Bangla, no repeated tables.

## Do not
- Do not read full analysis files back, re-read the template, or render pages "just to look".
- Do not re-explain concepts already covered in earlier sub-domains — agents refer back by name.
- Do not run web research again unless the user asks; section ২১ uses `context.md` §2026 only.
