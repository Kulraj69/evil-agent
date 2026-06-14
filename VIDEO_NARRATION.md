# FIND EVIL! — Word-for-Word Video Narration + Commands

**Total target: 5:00.** Read the **SAY** lines aloud while screen-recording.
Run the **RUN** commands in a terminal large enough to read on video. Timestamps
are guides, not hard cuts.

> Recording tip: do a dry run once first. Use a big terminal font (18–22pt). On
> the SIFT Workstation, activate the venv or just use `python3` if deps are
> system-installed.

---

## PART 0 — Before you hit record (setup, off-camera)

On the **SIFT Workstation**:

```bash
git clone https://github.com/Kulraj69/evil-agent.git
cd evil-agent
pip install -r requirements.txt

# (optional, for live LLM) create .env from the template and add Azure creds
cp .env.example .env && nano .env

# Download + verify + mount the real NIST CFReDS image (~5 GB, one time)
bash scripts/fetch_cfreds.sh /evidence/cfreds
# -> prints the raw read-only path, e.g. /evidence/cfreds/ewf_mount/ewf1
```

Have two terminals (or tabs) ready and `docs/architecture.png` open in an image viewer.

---

## PART 1 — Hook (0:00–0:30)

**[ON SCREEN]** Title slide or just the terminal with the repo.

**SAY:**
> "AI-powered attackers now go from initial access to domain control in minutes —
> some autonomous agents hit full privilege escalation in under a minute.
> Meanwhile a human responder is still pulling up their toolkit. Protocol SIFT
> showed AI can drive the SIFT Workstation, but it hallucinates. I built
> **FIND EVIL!** — a self-correcting triage agent that thinks like a senior
> analyst: it makes a hypothesis, checks it against the evidence, and when the
> evidence doesn't fit, it corrects itself. Let me show you."

---

## PART 2 — Architecture (0:30–1:00)

**[ON SCREEN]** Open `docs/architecture.png`.

**SAY:**
> "The architecture is a **Custom MCP Server** — pattern two. The agent reaches
> forensic tools only through typed, read-only functions: prefetch, MFT timeline,
> event logs, memory, registry. There is **no shell command and no write
> function**, so the agent physically cannot modify evidence. That's an
> **architectural** guardrail, not a prompt. Findings then pass through a
> validation layer that rejects anything not grounded in evidence, and every step
> is logged for a full audit trail."

---

## PART 3 — The self-correction demo (1:00–2:45) — THE KEY MOMENT

**[ON SCREEN]** Terminal.

**RUN:**
```bash
python3 run_demo.py
```

**SAY (narrate as it scrolls):**
> "It opens with a **ransomware** hypothesis — about seventy percent confidence —
> because a suspicious executable ran several times.
>
> It gathers evidence through the MCP tools... and here's the turning point: the
> **MFT timeline shows no mass file encryption**. That contradicts ransomware. The
> agent flags the contradiction —
>
> — and **self-corrects**. Watch the hypothesis change: it's not ransomware, it's
> **credential theft**. Now it corroborates that theory: forty-seven failed logins
> then a success, **LSASS injection** in memory, and a **registry Run key** for
> persistence.
>
> Notice the validator is also **catching hallucinations** — findings that don't
> trace to real evidence are dropped before they reach the report.
>
> It **converges at eighty-eight percent** on credential theft — and it did it by
> noticing its own first answer was wrong."

---

## PART 4 — Real case data on the SIFT Workstation (2:45–3:45) — SATISFIES "REAL DATA"

**[ON SCREEN]** Second terminal.

**SAY:**
> "That was a guided scenario. Now the same agent against a **real NIST CFReDS
> disk image**, using real SIFT binaries — all read-only."

**RUN:**
```bash
python3 run_real_sift.py --live \
    --disk /evidence/cfreds/ewf_mount/ewf1 \
    --case CFREDS-LEAK
```

**SAY (point at the integrity lines):**
> "First, the agent records a **SHA-256 baseline** of the evidence before it reads
> anything. It runs the real Sleuth Kit and Volatility tooling — read-only — then
> **re-verifies the hash after analysis**. The image is **unchanged**, **zero
> spoliation events**. Because there's no write tool in the server, evidence
> simply *cannot* be altered — and we prove it cryptographically every run."

> *(If a tool is missing it prints exactly which binary to install — mention that
> the graceful degradation means the run always completes with an audit trail.)*

---

## PART 5 — Accuracy + audit trail (3:45–4:25)

**[ON SCREEN]** Terminal.

**RUN:**
```bash
python3 benchmark.py
```

**SAY:**
> "Across eight labeled cases, a naive single-shot baseline that trusts its first
> guess gets **zero out of eight** — every case has a plausible decoy. The
> self-correcting agent gets **eight out of eight**, and its hallucination rate is
> **zero percent** versus the baseline's hundred."

**RUN:**
```bash
cat execution_logs/DEMO-001_final_report.json | python3 -m json.tool | head -40
```

**SAY:**
> "And the audit trail: structured JSON with timestamps, **token usage per LLM
> call**, and every finding traceable back to the tool execution that produced
> it — exactly what a judge needs to verify a result."

---

## PART 6 — Guardrails recap + close (4:25–5:00)

**[ON SCREEN]** Briefly show `mcp_server/sift_mcp_server.py`.

**SAY:**
> "So — why trust it? The tool surface is **typed and read-only**: no shell, no
> writes. Every finding must **cite evidence** or it's rejected. Evidence is
> **hash-verified** against spoliation. And it's all **reproducible** — one command
> offline, or against the real SIFT Workstation.
>
> FIND EVIL! is an IR agent that doubts its first answer, checks the evidence, and
> shows its work. Self-correcting, grounded, and auditable. Thanks for watching."

**[ON SCREEN]** End slide: `github.com/Kulraj69/evil-agent` · Apache 2.0.

---

## Exact command list (copy/paste order)

```bash
# 0. setup (off camera)
bash scripts/fetch_cfreds.sh /evidence/cfreds

# 3. scripted self-correction
python3 run_demo.py

# 4. real CFReDS data, read-only, live LLM
python3 run_real_sift.py --live --disk /evidence/cfreds/ewf_mount/ewf1 --case CFREDS-LEAK

# 5. accuracy + audit
python3 benchmark.py
cat execution_logs/DEMO-001_final_report.json | python3 -m json.tool | head -40
```

## Honesty notes (so you're never caught off guard)

- The **scripted** `run_demo.py` deterministically reproduces the self-correction
  arc — it's the cleanest way to *show* the behavior. The **`--live`** flag proves
  the real Azure OpenAI model is wired in; on some cases the live model gets the
  answer right immediately (fewer corrections) — that's fine, say so.
- The CFReDS Data Leakage case is **disk + removable media (no memory dump)**, so
  memory-based findings won't apply there; the value of that segment is **real
  read-only analysis + provable evidence integrity**, which is what the rules ask
  for.
- If `--live` isn't configured on the Workstation, the run still completes with
  offline reasoning and a full audit trail.
