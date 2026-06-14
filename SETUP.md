# FIND EVIL! — Setup & Try-It-Out

Two ways to run: **offline (zero setup)** to see the agent self-correct, and
**real case data on the SIFT Workstation** for genuine forensic analysis.

---

## A. Quick start — offline (no creds, no downloads)

```bash
git clone https://github.com/Kulraj69/evil-agent.git
cd evil-agent
pip install -r requirements.txt          # optional for offline; stdlib-only runners

python3 run_demo.py            # one live self-correction (ransomware -> credential theft)
python3 run_all_scenarios.py   # self-correction across all 6 incident types (expect 8/8)
python3 benchmark.py           # accuracy: 8/8 vs 0/8 baseline, 0% hallucination rate
python3 explore.py             # interactive menu
pytest                         # 23 tests (validator, guardrails, spoliation, self-correction)
```

Expected: `run_demo.py` ends with `CREDENTIAL_THEFT` at 88%; `run_all_scenarios.py`
prints `converged correctly on 8/8`; `benchmark.py` prints `8/8 = 100%`.

> If your system Python is broken (e.g. a `pip` / `pyexpat` error), use a venv
> from a working interpreter:
> `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
> then run with `.venv/bin/python ...`.

---

## B. Live LLM reasoning (Azure OpenAI)

1. Copy the env template and fill in your Azure values:

   ```bash
   cp .env.example .env
   # edit .env:
   #   AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
   #   AZURE_OPENAI_API_KEY=...
   #   AZURE_OPENAI_DEPLOYMENT=<your deployment name>
   #   AZURE_OPENAI_API_VERSION=2024-10-21
   ```

2. Install deps (includes `openai`):

   ```bash
   pip install -r requirements.txt
   ```

3. Run with `--live`:

   ```bash
   python3 run_demo.py --live
   python3 run_real_sift.py --live --disk <image> --memory <dump> --logs <evtx>
   ```

`.env` is gitignored — credentials are never committed. If `--live` is passed but
credentials are missing, the agent prints a notice and falls back to offline
reasoning so the run still completes.

---

## C. Real case data on the SANS SIFT Workstation

The forensic tools (`mcp_server/real_sift_tools.py`) wrap real SIFT binaries
**read-only**. To run against genuine evidence:

1. **Download the SIFT Workstation** from
   <https://www.sans.org/tools/sift-workstation/> and boot it.

2. **(Optional) Install Protocol SIFT** for comparison:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/teamdfir/protocol-sift/main/install.sh | bash
   ```

3. **Get a sample image.** Use the helper script to download, **SHA1-verify**,
   extract, and read-only-mount the NIST CFReDS Data Leakage PC image in one step:

   ```bash
   bash scripts/fetch_cfreds.sh /evidence/cfreds
   # prints the raw read-only path, e.g. /evidence/cfreds/ewf_mount/ewf1
   ```

   (Or download manually from
   <https://cfreds-archive.nist.gov/data_leakage_case/data-leakage-case.html>;
   provenance + hashes are in `datasets/README.md`.)

4. **Confirm the read-only SIFT binaries are on PATH** (`vol`, `fls`,
   `evtx_dump.py`, `rip.pl`). They ship with the SIFT Workstation.

5. **Run the agent** against the raw read-only path from step 3:

   ```bash
   python3 run_real_sift.py --live \
       --disk   /evidence/cfreds/ewf_mount/ewf1 \
       --case   CFREDS-LEAK
   ```

   Every evidence file is SHA-256 hashed before first read and re-verified after
   each tool call. The final report records `evidence_integrity.files_hashed` and
   `spoliation_events` (expected: `0`). If a binary is missing the run still
   completes and tells you exactly what to install.

---

## Where to look

| Want to see... | File |
|----------------|------|
| The self-correction loop | `agent/self_correcting_agent.py` |
| Anti-hallucination validation | `agent/evidence_validator.py` |
| Typed read-only tool surface + integrity | `mcp_server/sift_mcp_server.py` |
| Real SIFT binary adapter | `mcp_server/real_sift_tools.py` |
| Audit log + token usage | `observability/logger.py`, `execution_logs/*_final_report.json` |
| Accuracy + spoliation report | `ACCURACY_REPORT.md` |
| Architecture + trust boundaries | `docs/architecture_diagram.md`, `docs/architecture.png` |
