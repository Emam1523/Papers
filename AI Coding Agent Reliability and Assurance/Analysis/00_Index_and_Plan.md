# SPL3 Paper Analysis — Index ও Roadmap

**Domain:** AI Coding Agent Reliability and Assurance

## মোট Paper Inventory

মোট **26টা paper**, প্রতিটা একবার করে (আগে 29টা PDF ছিল; 2026-10-28-এ duplicate সরানো হয়েছে)।

| Paper | কী করা হয়েছে |
|---|---|
| SWE-bench (ICLR 2024) | Coding-Agent Evaluation folder-এর হুবহু copy Recycle Bin-এ পাঠানো হয়েছে; AI Coding Agents folder-এ একটা copy আছে |
| Human-in-the-Loop Patch Evaluation (LLM-as-a-Judge) | প্রকাশিত version (AI-SQE '26 workshop) রাখা হয়েছে এবং Patch Validation folder-এ সরানো হয়েছে; Evaluation folder-এর হুবহু copy আর Patch Validation-এর পুরনো arXiv preprint (v1, Nov 2025) Recycle Bin-এ |

## Sub-domain অনুযায়ী Paper ও পড়ার ক্রম

| # | Sub-domain | Paper (পড়ার ক্রমে) | Status |
|---|---|---|---|
| 1 | **AI Coding Agents** | 1. SWE-bench → 2. SWE-agent → 3. AutoCodeRover → 4. Agentless → Summary | ✅ সব |
| 2 | **Automated Program Repair** | 1. APR: Emerging Trends (survey) → 2. VRpilot — LLM Vulnerability Repair case study → 3. RePaCA — Reasoning LLM static APCA (Neurocomputing 2026) → Summary | ✅ সব |
| 3 | **Coding-Agent Evaluation & Reliability** | 1. SWE-rebench (NeurIPS 2025) → 2. SWE-Bench Pro → 3. Engineering Reliable Coding Agents (বড় monograph, ~133k শব্দ) → Summary | ✅ সব |
| 4 | **LLM Test Generation** | 1. UniTSyn → 2. CoverUp → 3. TestDecision → 4. ExecutionAgent ("You Name It, I Run It") → 5. Oracle-Guided Program Selection → Summary | ✅ সব |
| 5 | **Patch Validation** | 1. HITL LLM-as-a-Judge (Google) → 2. Code Representation in APCA → 3. Harden and Catch (Meta) → Summary | ✅ সব |
| 6 | **Security of AI-Generated Code** | 1. CWEval → 2. Security & Quality in LLM Code → 3. Automating correctness assessment for security (JSS 2024) → 4. Enhancing Reliability in Secure Code Gen → 5. SecureVibeBench → Summary | ✅ সব |
| 7 | **Trustworthy AI for SE** | 1. Trustworthy AI Software Engineers (vision) → 2. Proof-Carrying Code Completions → 3. AI Assurance: Comprehensive Testing Strategy → Summary | ✅ সব |
| 8 | **Final Synthesis** | সব sub-domain-এর comparison, cross-domain gap map, চূড়ান্ত research direction → `08_Final_Synthesis/Final_Synthesis.docx` | ✅ |

## প্রতিটা Paper Analysis-এর Template (২১টা section)

0. Bibliographic info · 1. TL;DR + supervisor-কে ৩০ সেকেন্ডে · 2. Background concepts · 3. Problem statement · 4. Goal & RQ · 5. Methodology · 6. Math/formula (প্রতিটা symbol + worked example) · 7. Experimental setup · 8. Results · 9. Key findings · 10. কেন অন্যদের থেকে ভালো · 11. কখন ভালো/খারাপ কাজ করে · 12. Limitations (author + আমার critique) · 13. Research gaps · 14. Improvement ideas · 15. Publication potential · 16. SPL3 implementation · 17. পরবর্তী গবেষণায় প্রভাব · 18. Supervisor-এর সম্ভাব্য প্রশ্নোত্তর · 19. Glossary · 20. Summary card · 21. বর্তমান (2026) প্রেক্ষাপট — আজকের model ও agent-দের সাথে তুলনা, gap আজও খোলা কিনা, বর্তমান model দিয়ে SPL3 idea

## প্রতিটা Sub-domain শেষে
একটা `00_Subdomain_Summary.docx` — paper-গুলোর পাশাপাশি তুলনা টেবিল, common gap, sub-domain-এর সেরা research সুযোগ।

## বর্তমান অবস্থার উৎস
- `00_Current_State_2026_Sources.md` — October 2026-এর model, agent, benchmark ও reliability তথ্যের fact sheet (প্রতিটা তথ্যের URL, কোম্পানির দাবি নাকি স্বাধীন মাপ)। Section ২১ শুধু এই file থেকে তথ্য নেয়।

## File Format
- **মূল deliverable:** প্রতিটা analysis-এর **Word (.docx)** file — সূচিপত্র, table, আর Word-এর আসল equation সহ।
- **Source:** পাশের `.md` file-টা হলো লেখার source। কিছু বদলাতে হলে `.md` বদলে আবার Word তৈরি করা হয়।
- **Word তৈরির tool:** `_tools/md2docx.py` + `_tools/finalize_docx.ps1`
