Write a professor-level analysis in simple Bangla (Bengali script; English technical terms stay English) of one paper for a 4th-year SPL3 project on "AI Coding Agent Reliability and Assurance". The supervisor will read it: every number must be exact, nothing important skipped. Be efficient: read the paper once, write once.

**Paper:** {title}
- Text: `{txt_path}` (PDF copy: `{pdf_path}`; if a table is garbled, re-extract only that page with `pdftotext -raw -f N -l N`).
- Venue/year: take from the paper itself; if not stated, say so (do not guess).

**Only other file to read:** `E:\Course Book and Slide\4th Year\SPL3\Papers\AI Coding Agent Reliability and Assurance\.claude\skills\spl3-paper-analysis\context.md` (prior findings CG1–CG15, research direction, 2026 facts). Do NOT open earlier analyses or summaries; refer to them by name ("Sub-domain 1-এর Agentless দেখো") instead of re-explaining.

**Why this paper matters to us:** {lens}

**Structure (22 sections, Bangla numerals, `##` headings):**
০ Bibliographic info (table) · ১ TL;DR + "Supervisor-কে ৩০ সেকেন্ডে" · ২ Background (only concepts NEW to this project) · ৩ Problem · ৪ Goal & RQ · ৫ Methodology (step by step, exact settings) · ৬ Math (every formula the paper uses or that formalises its metrics; each symbol explained; one worked example with the paper's real numbers) · ৭ Setup (table) · ৮ Results (tables with exact numbers, cite table/figure) · ৯ Key findings (5–8) · ১০ Why better than alternatives · ১১ When it works / fails · ১২ Limitations (authors' + "আমার পর্যবেক্ষণ") · ১৩ Research gaps (table: G-id, gap, evidence, related CG / our sub-domain folder) · ১৪ Improvement ideas · ১৫ Publication potential (SPL3-feasible) · ১৬ SPL3 implementation · ১৭ Influence / link to our earlier sub-domains · ১৮ Supervisor Q&A (6–8) · ১৯ Glossary (short) · ২০ Summary card · ২১ বর্তমান (2026) প্রেক্ষাপট (২১.১ then-vs-now table, ২১.২ still true / outdated, ২১.৩ gaps open today table, ২১.৪ SPL3 idea with current models, cost-aware, ২১.৫ 3 Q&A) — 2026 facts only from context.md, keep its vendor/independent labels; if no current data, say "বর্তমান model-এর তথ্য পাওয়া যায়নি".
Target 500–750 lines. Label own calculations "আমার হিসাব".

**Output:** `{out_path}` — title line `# {title_line}`, then a `>` blockquote with "Sub-domain: {subdomain}" and the PDF path `{orig_pdf}`.

**Markdown/LaTeX (custom Word converter):** `-` bullets (2-space nested), `1.` lists, pipe tables with `|---|` row and no `|` inside cells, `**bold**`, a literal `*` must be "∗", no ASCII diagrams, no `$` for money (USD). Math: `$$` alone on its lines, inline `$..$`. Allowed LaTeX: \frac \dfrac \binom \sqrt \text{} \mathbb{} \mathcal{} \hat \bar \tilde _ ^ {} \sum \prod \int \ln \log \min \max \exp \lim \arg Greek \cdot \times \in \notin \cup \cap \subseteq \land \lor \neg \forall \exists \neq \leq \geq \approx \ll \to \oplus \mid \ldots \infty \left( \right) \quad \; \, cases. Nothing else; no straight double quotes inside \text{}.
Check once: `python -I "E:\Course Book and Slide\4th Year\SPL3\Papers\AI Coding Agent Reliability and Assurance\Analysis\_tools\md2docx.py" <md> "{scratch}\test.docx"` and fix any `[warn]`. Do not build the final Word file.

**Reply in ≤ 12 lines:** output path; 4 headline numbers with table/section; up to 4 uncertainties or paper-internal inconsistencies; new gap(s) for the CG list, if any.
