# FIND EVIL! — Project Description

*(Devpost story format. Paste into the Devpost "Project story" fields.)*

## Inspiration

AI-powered adversaries now go from initial access to domain control in minutes —
Horizon3's agent hit full privilege escalation in 60 seconds; Anthropic's GTG-1002
writeup described an attacker running at 80–90% autonomy at request rates
"physically impossible" for humans. Meanwhile the defender is still looking up
command-line flags. Protocol SIFT showed AI agents *can* drive the SIFT
Workstation — but it hallucinates. We wanted to build the part that makes an
autonomous responder **trustworthy**: an agent that thinks like a senior analyst,
notices when its own theory doesn't fit the evidence, and **corrects itself**.

## What it does

FIND EVIL! is a **self-correcting incident-response triage agent**. Given a case
(disk image, memory dump, event logs), it:

1. Forms an initial hypothesis (e.g. "ransomware").
2. Gathers evidence through a **custom read-only SIFT MCP server**.
3. **Validates** every finding against the actual artifacts (anti-hallucination).
4. Detects contradictions ("ransomware — but the MFT shows no mass encryption").
5. **Self-corrects** to the hypothesis the evidence supports ("credential theft").
6. Converges, and emits a full audit trail: finding → tool → evidence.

It handles six incident types (credential theft, ransomware, lateral movement,
C2 beaconing, data exfiltration, benign) and ships with a reproducible accuracy
benchmark.

## How we built it

- **Architectural pattern #2 — Custom MCP Server.** Instead of `execute_shell_cmd`,
  the agent only sees typed functions: `analyze_prefetch`, `extract_mft_timeline`,
  `parse_event_logs`, `analyze_memory_dump`, `search_registry_hive`, `get_amcache`.
- **Self-correction loop** with a hard `MAX_ITERATIONS` cap and gap-driven
  refinement (`agent/self_correcting_agent.py`).
- **Anti-hallucination validator** (`agent/evidence_validator.py`): 6 layered
  checks — citation existence, citation presence, fabricated-pattern screen,
  numeric grounding, claim/evidence alignment with concept corroboration, and
  cross-citation consistency.
- **Evidence integrity:** SHA-256 hash-on-open + verify-after-every-call, with
  spoliation events logged. The real adapter (`mcp_server/real_sift_tools.py`)
  wraps Volatility3 / Sleuth Kit / python-evtx / RegRipper **read-only** (fixed
  argv, never `shell=True`).
- **Observability:** structured JSON logs with timestamps and per-call token
  usage; finding→tool→evidence tracing (`observability/logger.py`).

## Challenges we ran into

- **Convergence vs. looping.** The agent initially "refined" to the same
  hypothesis until it hit the iteration cap. We fixed it by distinguishing
  *contradiction* gaps (which should drive correction) from *soft* gaps (missing
  corroboration), so it self-corrects once and converges.
- **Validator over-rejecting real findings.** Naive keyword overlap rejected
  legitimate findings whose wording differed from JSON field names. We added
  concept-corroboration (mapping claims to the boolean signals tools emit) so
  genuine findings pass while fabricated names/counts are still caught.

## What we learned

The hard part of autonomous IR isn't running tools — it's **knowing when you're
wrong**. Making evidence protection *architectural* (no write capability exists)
rather than *prompt-based* is what makes the output something a practitioner
would actually stand behind.

## What's next

- Wire the read-only adapter to a live SIFT Workstation against the SANS sample
  images and NIST CFReDS (provenance already documented in `datasets/`).
- Swap the offline reasoning stand-in for the Bedrock Claude client and re-run
  the same benchmark for live-model accuracy.
- Multi-source correlation (disk vs. memory discrepancy detection) and a larger
  labeled benchmark.

## Which qualities of autonomous execution we address

Self-correction in real time (Criterion #1, tiebreaker); hallucination catching
and confirmed-vs-inferred separation (Criterion #2); architectural guardrails
tested for bypass (Criterion #4); finding-to-tool traceability (Criterion #5);
and one-command reproducibility (Criterion #6).

## Try it

```bash
pip install -r requirements.txt
python3 run_demo.py            # live self-correction
python3 run_all_scenarios.py   # all 6 incident types (8/8)
python3 benchmark.py           # accuracy: 8/8 vs 0/8 baseline, 0% hallucination
python3 run_real_sift.py --disk <image> --memory <dump> --logs <evtx>  # real data
```
