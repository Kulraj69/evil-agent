# FIND EVIL! — Datasets

This folder holds the labeled cases used by `benchmark.py` and
`run_all_scenarios.py`.

## `benchmark_cases.json`

Two kinds of cases:

### 1. Synthetic scenario cases (`BENCH-001` … `BENCH-008`)
Self-contained cases whose evidence is generated deterministically by the SIFT
MCP server's scenario engine (`SIFTMCPServer(scenario=...)`). They run offline
with no downloads and power the reproducible accuracy numbers in
`ACCURACY_REPORT.md`. Each spans a distinct incident type and ships with a
plausible **decoy** hypothesis that a single-shot triage would fall for.

Incident types covered: `credential_theft`, `ransomware`, `lateral_movement`,
`c2_beaconing`, `data_exfiltration`, `benign`.

### 2. Real public-image cases (`REAL-CFREDS-*`)
These reference **real, downloadable NIST forensic images**. They are *skipped*
by the synthetic harness (marked `status: real_image_reference_pending_tool_integration`)
because evaluating them requires wiring the MCP tools to real forensic parsers.
They are included to document provenance and provide a ready target for the
real-SIFT integration milestone.

| Case | Source | Maps to |
|------|--------|---------|
| `REAL-CFREDS-LEAK` | [NIST CFReDS Data Leakage Case](https://cfreds-archive.nist.gov/data_leakage_case/data-leakage-case.html) | `data_exfiltration` |
| `REAL-CFREDS-HACK` | [NIST CFReDS Hacking Case](https://cfreds-archive.nist.gov/) | `lateral_movement` |

## Fetching the real images (optional)

The NIST CFReDS images are large (PC image ~5 GB compressed). They are **not**
committed to this repo. To use them:

1. Download from the CFReDS archive linked above.
2. Verify integrity with the published SHA1 hashes
   (e.g. PC image `72432916933F5A309A8C456B40C9601D1F8D2A4F`,
   full list at the [hash page](https://cfreds-archive.nist.gov/data_leakage_case/hash_values.html)).
3. Place them under `/evidence/cfreds/` (or update the paths in
   `benchmark_cases.json`).
4. Wire the MCP server's `_mock_*` methods to real parsers (plaso, sleuthkit,
   Volatility3) so the tools read the actual images.

The official answer key for the Data Leakage case is published by NIST
([leakage-answers.pdf](https://cfreds-archive.nist.gov/data_leakage_case/leakage-answers.pdf)),
which provides ground truth for scoring.

## Adding your own cases

The harness is fully dataset-driven — add an object to the `cases` array with an
`evidence` block and a `ground_truth.incident_type`. No code changes required
for synthetic scenarios that reuse an existing incident type.
