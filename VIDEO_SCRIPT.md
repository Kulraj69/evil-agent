# FIND EVIL! — 5-Minute Demo Video Script

**Target length:** 5:00 | **Audience:** SANS hackathon judges
**Goal:** Prove Criterion #1 (Autonomous Execution / self-correction) and
Criterion #2 (IR Accuracy / anti-hallucination), with the audit trail and
architectural guardrails visible.

Each section lists **[on screen]**, **[say]**, and the **command** to run.

---

## 0:00 – 0:30 · Hook + problem

**[on screen]** Title slide: "FIND EVIL! — A Self-Correcting IR Triage Agent."

**[say]**
> "AI triage agents are fast, but they make a confident first guess and run with
> it — and they hallucinate findings. FIND EVIL! does the opposite: it makes a
> guess, *checks itself against the evidence*, catches its own mistake, and
> corrects course. Let me show you."

---

## 0:30 – 1:00 · Architecture (15s glance)

**[on screen]** Open `docs/architecture.png` (or `docs/architecture.html`).

**[say]**
> "Evidence flows in through a **custom MCP server** that exposes only typed
> forensic functions — there's no shell execution, so the agent physically
> can't run a destructive command. The self-correcting agent loops over
> hypothesize → gather → **validate** → find gaps → refine. Everything is logged
> for a full audit trail."

```bash
open docs/architecture.png
```

Point at: MCP guardrails (red) → agent loop (blue) → validation (green) → audit (yellow).

---

## 1:00 – 3:00 · The live self-correction demo (the money shot)

**[on screen]** Terminal, run:

```bash
python3 run_demo.py
```

**[say] — narrate as it scrolls:**

- **Iteration 1 / initial hypothesis:**
  > "It opens with a **ransomware** hypothesis at 70% — suspicious.exe ran five
  > times, looks bad."
- **Evidence gathering:**
  > "It runs prefetch and the **MFT timeline** through the MCP tools."
- **Contradiction:**
  > "Here's the key moment — the MFT shows **no mass file encryption**. That
  > directly contradicts ransomware. The agent flags the gap."
- **SELF-CORRECTION:**
  > "So it **revises**: this isn't ransomware, it's **credential theft**. Watch
  > the hypothesis change live."
- **Iteration 2 / corroboration:**
  > "Now it pulls event logs — 47 failed logins then a success — and a memory
  > dump showing **LSASS injection**, plus a registry Run key for persistence."
- **Validation / hallucination catch:**
  > "Every finding is validated against the evidence. Findings that cite
  > evidence that isn't there are **dropped as hallucinations** — you can see the
  > count in the audit stats."
- **Convergence:**
  > "It converges at **88% confidence** on LSASS credential dumping, with a clean
  > audit trail: finding → tool → evidence."

**[on screen]** Optionally `cat execution_logs/DEMO-001_final_report.json` and
scroll the `audit_trail` block.

---

## 3:00 – 4:15 · Accuracy benchmark (the proof it generalizes)

**[say]**
> "One demo is a story. Here's the data. I ran it across eight labeled cases."

**[on screen]** Run:

```bash
python3 benchmark.py
```

**[say] — point at the results block:**
> "A naive single-shot baseline that trusts its first guess gets **0 of 8** —
> every case has a plausible decoy that traps it. The self-correcting agent gets
> **8 of 8**, macro-F1 of 1.0. And on hallucinations: the baseline emits
> unsupported findings **100%** of the time; FIND EVIL!'s validation layer brings
> that to **0%**."

**[on screen]** Briefly show `ACCURACY_REPORT.md` — the confusion matrix
diagonal and the hallucination-reduction table.

---

## 4:15 – 4:45 · Guardrails + audit trail recap

**[say]**
> "Why is this trustworthy? Three architectural choices: the MCP server only
> exposes **typed tools** — no shell. Every finding must **cite evidence** or
> it's rejected. And every step is **logged** so an analyst can trace any
> conclusion back to the tool and artifact that produced it."

**[on screen]** Flash `mcp_server/sift_mcp_server.py` (the typed function list)
and one `execution_logs/*.json` audit entry.

---

## 4:45 – 5:00 · Close

**[say]**
> "FIND EVIL! is an IR agent that thinks like a good analyst: it doubts its first
> answer, checks the evidence, and shows its work. Self-correcting, grounded, and
> auditable. Thanks for watching."

**[on screen]** End slide: repo URL `github.com/Kulraj69/evil-agent`, Apache 2.0.

---

## Pre-recording checklist

- [ ] `python3 run_demo.py` runs clean (self-correction visible)
- [ ] `python3 benchmark.py` prints 0/8 baseline, 8/8 self-correcting
- [ ] `docs/architecture.png` open and ready in a tab
- [ ] `ACCURACY_REPORT.md` open for the confusion matrix
- [ ] Terminal font large enough to read on video
- [ ] Total runtime under 5:00
