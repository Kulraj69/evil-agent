# FIND EVIL! — Accuracy Report

**Generated from:** `benchmark.py` → `execution_logs/benchmark_results.json`
**Dataset:** `datasets/benchmark_cases.json` (8 labeled IR cases)
**Reproduce:** `python3 benchmark.py`

---

## 1. What this measures

The benchmark evaluates two things judges care about for **Criterion #2 (IR Accuracy)**:

1. **Classification accuracy** — does the agent converge on the *correct* incident
   type for each case?
2. **Hallucination rate** — how many emitted findings are *not* supported by the
   underlying forensic evidence?

It compares two triage strategies on the same evidence:

| Agent | Behavior |
|-------|----------|
| **Baseline** | Single-shot. Commits to the first hypothesis the evidence superficially suggests (the *decoy*) and accepts every finding without evidence validation. Models a typical non-self-correcting LLM pass. |
| **FIND EVIL! (self-correcting)** | Gathers evidence with the SIFT MCP tools, **validates** each finding against that evidence, detects contradictions, **refines** the hypothesis, and converges. |

> **Methodology note (transparency):** Evidence is produced by the SIFT MCP
> server in *scenario mode* (`SIFTMCPServer(scenario=...)`), where each scenario
> replays artifact patterns modeled on NIST CFReDS / DFIR-style images. The
> agent's reasoning is evaluated deterministically and offline (no Bedrock
> calls) so the result is fully reproducible. The decoy hypotheses are chosen to
> be genuinely plausible from a first glance at the evidence — which is exactly
> the failure mode self-correction is designed to fix.

---

## 2. Headline results

| Metric | Baseline | FIND EVIL! |
|--------|---------:|-----------:|
| **Accuracy** | **0 / 8 (0%)** | **8 / 8 (100%)** |
| Macro Precision | — | 1.000 |
| Macro Recall | — | 1.000 |
| **Macro F1** | — | **1.000** |
| Findings emitted | 8 | 9 |
| **Hallucinated findings** | **8 (100%)** | **0 (0%)** |

**Bottom line:** Self-correction flips every decoy-driven misclassification into a
correct answer, and the evidence-validation layer suppresses 100% of the
unsupported findings the baseline would have reported.

---

## 3. Per-case results

| Case | Ground truth | Baseline (decoy) | FIND EVIL! | Corrected? |
|------|--------------|------------------|-----------|:----------:|
| BENCH-001 | credential_theft | ransomware ❌ | credential_theft ✅ | ✔ |
| BENCH-002 | ransomware | credential_theft ❌ | ransomware ✅ | ✔ |
| BENCH-003 | lateral_movement | credential_theft ❌ | lateral_movement ✅ | ✔ |
| BENCH-004 | c2_beaconing | lateral_movement ❌ | c2_beaconing ✅ | ✔ |
| BENCH-005 | data_exfiltration | ransomware ❌ | data_exfiltration ✅ | ✔ |
| BENCH-006 | benign | credential_theft ❌ | benign ✅ | ✔ |
| BENCH-007 | credential_theft | ransomware ❌ | credential_theft ✅ | ✔ |
| BENCH-008 | ransomware | data_exfiltration ❌ | ransomware ✅ | ✔ |

Note BENCH-006: the baseline raises a **false positive** on a benign IT software
push; the self-correcting agent correctly returns `benign` and emits **zero**
findings — avoiding an analyst false alarm.

---

## 4. Confusion matrix (FIND EVIL!)

Rows = ground truth, columns = predicted. A perfect diagonal means no
misclassifications.

| truth ↓ \ pred → | cred_theft | ransomware | lateral | c2 | exfil | benign |
|------------------|:----------:|:----------:|:-------:|:--:|:-----:|:------:|
| **credential_theft** | **2** | 0 | 0 | 0 | 0 | 0 |
| **ransomware**       | 0 | **2** | 0 | 0 | 0 | 0 |
| **lateral_movement** | 0 | 0 | **1** | 0 | 0 | 0 |
| **c2_beaconing**     | 0 | 0 | 0 | **1** | 0 | 0 |
| **data_exfiltration**| 0 | 0 | 0 | 0 | **1** | 0 |
| **benign**           | 0 | 0 | 0 | 0 | 0 | **1** |

---

## 5. Hallucination reduction

| | Baseline | FIND EVIL! |
|--|---------:|-----------:|
| Findings emitted | 8 | 9 |
| Findings **not** supported by evidence | 8 | 0 |
| **Hallucination rate** | **100%** | **0%** |

The baseline emits one decoy-aligned finding per case; in every case that
finding's claimed signal is absent from the cited artifact, so it is a
hallucination. The self-correcting agent's `EvidenceValidator`
(`agent/evidence_validator.py`) drops any finding whose claim is not grounded in
the cited evidence, yielding a **100% → 0% hallucination rate** reduction.

---

## 6. Why self-correction wins

For each case, the decoy is the trap a fast analyst (or a single-shot LLM) falls
into. The self-correcting loop escapes it because it:

1. **Gathers corroborating evidence** rather than acting on the first signal.
2. **Validates** each finding against the actual artifact content.
3. **Detects the contradiction** (e.g., "ransomware hypothesis but MFT shows no
   mass file modification").
4. **Refines** to the hypothesis the *whole* evidence set supports.
5. **Converges** only when findings are validated and gaps are closed.

This is the behavior described qualitatively in `README.md` and shown live in
`run_demo.py` — here it is quantified across 8 labeled cases.

---

## 7. Limitations & next steps

- The 8-case set is small and synthetic; numbers will be lower and more
  interesting on a larger, noisier corpus. The harness is dataset-driven, so
  adding real CFReDS-derived cases to `datasets/benchmark_cases.json` requires
  no code changes.
- Evidence is currently produced by the MCP server's scenario engine. Wiring the
  same typed tools to real SIFT binaries (plaso, sleuthkit, Volatility3) is the
  natural next step and is isolated behind the `_mock_*` methods in
  `mcp_server/sift_mcp_server.py`.
- Reasoning is evaluated deterministically for reproducibility; swapping in the
  Bedrock Claude client (`MockLLMClient` → real client) lets the same harness
  measure live-model accuracy.
