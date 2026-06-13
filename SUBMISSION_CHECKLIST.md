# FIND EVIL! — Submission Checklist

A self-audit of submission completeness for the SANS Cybersecurity + AI
Hackathon. Update the right-hand column before submitting.

> **Note:** Confirm each item against the *official* SANS/Devpost rules page —
> the list below is our best reconstruction from `README.md` and the project's
> stated criteria, not a copy of the official rubric.

## Required deliverables

| # | Deliverable | Status | Where / Notes |
|---|-------------|:------:|---------------|
| 1 | Public code repository | ✅ | github.com/Kulraj69/evil-agent |
| 2 | Open-source license (Apache 2.0) | ✅ | `LICENSE` |
| 3 | Architecture diagram | ✅ | `docs/architecture.png` (+ svg/html/mermaid) |
| 4 | Working demo / try-it instructions | ✅ | `SETUP.md`, `README.md` quick start, `run_demo.py`, `explore.py` |
| 5 | Dataset + documentation | ✅ | `datasets/benchmark_cases.json`, `datasets/README.md` (incl. real NIST CFReDS provenance) |
| 6 | Accuracy / evaluation evidence | ✅ | `ACCURACY_REPORT.md`, `benchmark.py`, `execution_logs/benchmark_results.json` |
| 7 | 5-minute video | ⬜ **TODO** | Script ready in `VIDEO_SCRIPT.md` — record + upload (must show real case data) |
| 8 | Written project description (Devpost) | ✅ draft | `PROJECT_DESCRIPTION.md` — paste into Devpost |
| — | Agent execution logs (timestamps + token usage) | ✅ | `execution_logs/*_final_report.json` `audit_trail.token_usage`; per-call `llm_call` entries |
| — | Evidence integrity / spoliation section | ✅ | `ACCURACY_REPORT.md` §7 |
| — | Real case-data path | ✅ scaffold | `run_real_sift.py` + `mcp_server/real_sift_tools.py` (read-only) |

## Judging criteria coverage

| Criterion | Status | Evidence |
|-----------|:------:|----------|
| #1 Autonomous Execution (tiebreaker) | ✅ | Self-correction loop; `run_demo.py` (1 correction) and `run_all_scenarios.py` (8/8 across 6 types, starting from wrong decoy) |
| #2 IR Accuracy / anti-hallucination | ✅ | `EvidenceValidator` (6 layered checks incl. pattern + numeric grounding); 8/8 accuracy vs 0/8 baseline; 100%→0% hallucination rate |
| #3 Breadth & Depth | ✅ | 6 incident types, 6 artifact types (prefetch, MFT, event logs, memory, registry, amcache) |
| #4 Architectural constraints | ✅ | Typed MCP server, no shell execution, input validation, whitelisted plugins |
| #5 Audit trail | ✅ | `observability/logger.py`; structured JSON in `execution_logs/`; finding→tool→evidence tracing |
| #6 Usability | ✅ | One-command setup, interactive `explore.py`, thorough docs |

## Reproducibility (run before recording / submitting)

```bash
pip install -r requirements.txt
python3 run_demo.py            # single live self-correction (expect: 2 iterations, 1 correction, 88%)
python3 run_all_scenarios.py   # all 6 types (expect: 8/8 converged correctly)
python3 benchmark.py           # accuracy (expect: 8/8 vs 0/8, 0% hallucination rate)
```

All three should exit 0 and print the expected numbers above.

## Pre-submission polish (optional but recommended)

- [ ] Record the video (`VIDEO_SCRIPT.md`)
- [ ] Write the Devpost description
- [ ] (Stretch) Wire one MCP tool to a real parser on a CFReDS image
- [x] Live LLM client (Azure OpenAI) wired via `--live` (`agent/llm_client.py`)
- [x] `pytest` suite (23 tests) + GitHub Actions CI (`.github/workflows/ci.yml`)
- [ ] Final read-through of `README.md` for broken links / stale claims

## Known limitations (state these honestly in the writeup)

- Forensic tool outputs are currently produced by the MCP scenario engine
  (`_mock_*` methods); real-SIFT integration is scaffolded but not wired.
- Agent reasoning in the offline runners is a deterministic stand-in for the LLM
  to keep results reproducible; the Bedrock client is pluggable.
- The benchmark set is small (8 synthetic cases); real CFReDS cases are
  referenced with provenance but require the tool integration above to score.
