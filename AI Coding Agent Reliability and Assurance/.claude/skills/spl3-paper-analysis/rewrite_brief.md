Rewrite one existing paper analysis so a 4th-year student who has NEVER read a research paper can understand it on first reading. Language: simple, friendly Bangla (Bengali script; English technical terms stay English). Edit the file in place: `{md_path}`.

**Read:** the whole file `{md_path}` once. If something in it is unclear and you need the paper to explain it simply, grep the PDF text only (`pdftotext -layout "<pdf>" -` piped to grep; PDF path is in the file's top blockquote). Do not open other analyses.

**1. Add a new section** right after section ০ (before section ১), heading exactly:
`## ★ সহজ ভাষায় পুরো Paper (প্রথমবার পড়ার জন্য)`
with these 5 subsections, all mandatory, each in plain words, short sentences, no unexplained jargon, one everyday analogy where it helps:
- `### ক. Paper-টা কী নিয়ে?` — what kind of paper (benchmark / new tool / survey / empirical study), who made it, in 4–6 lines.
- `### খ. সমস্যাটা কী ছিল?` — the real problem before this paper, why it hurt, with one concrete example.
- `### গ. Paper কী solve করেছে?` — what they built/found, 3–5 bullets, the 2–3 most important numbers with a one-line meaning of each ("মানে ১০০টার মধ্যে মাত্র ২টা").
- `### ঘ. কীভাবে solve করেছে?` — the method as numbered steps (4–8), each step 1–2 lines, like explaining to a friend.
- `### ঙ. এরপর কী করা যায়?` — future work: what the authors say + what remains open + what WE could do in SPL3, 4–6 bullets.
End the section with a 3-line `> **মনে রাখো:**` blockquote.

**2. Simplify the rest of the file, section by section.** Keep every existing section, heading, table, number, formula, citation and fact — delete nothing. Change only the prose:
- Break long sentences; one idea per sentence.
- First time a technical term appears, explain it in a few words in brackets, unless section ২ already explains it.
- After each dense part (a formula, a results table, a methodology step list, the gap table), add one line `**সহজ কথায়:** …` saying what it means in plain words.
- In section ৬ (Math), after each formula say in words what it calculates, before the symbol list.
- Keep the tone of a helpful senior explaining, not a textbook.
Expected growth: about +25–40% lines.

**Markdown rules (custom Word converter):** `-` bullets (2-space nested), `1.` lists, pipe tables with `|---|` row and no `|` inside cells, `**bold**`, a literal `*` must be "∗", no ASCII diagrams, no `$` for money. Math: `$$` alone on its lines, inline `$..$`; do not change existing LaTeX.

**Check once:** `python -I "E:\Course Book and Slide\4th Year\SPL3\Papers\AI Coding Agent Reliability and Assurance\Analysis\_tools\md2docx.py" "{md_path}" "{scratch}\test_{tag}.docx"` and fix any `[warn]`. Do not build the final Word file.

**Reply in ≤ 6 lines:** path, old → new line count, any [warn] left, anything you could not simplify.
