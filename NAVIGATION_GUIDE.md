# 🧭 FIND EVIL! Navigation Guide

**Your Complete Guide to Understanding and Exploring the Self-Correcting IR Agent**

---

## 🎯 What Does This Do? (High-Level Overview)

### The Problem It Solves

Imagine you're a security analyst investigating a hacked computer. You have:
- A disk image (all the files)
- A memory dump (what was running)
- Event logs (what happened when)
- Registry hives (system settings)

**Traditionally:** You manually run 20+ forensic tools, cross-reference findings, look for contradictions, and piece together what happened. This takes **hours to days**.

**Protocol SIFT (baseline):** An AI agent runs tools automatically, but it:
- ❌ Hallucinates (makes up findings)
- ❌ Can't self-correct when wrong
- ❌ Uses dangerous shell execution

### What FIND EVIL! Does

**FIND EVIL! is a self-correcting AI agent that investigates incidents automatically AND catches its own mistakes.**

**Real Demo Example:**

```
🔍 Agent's First Guess (Iteration 1):
"This is a RANSOMWARE attack!"
Why? Found suspicious.exe running

⚠️ Agent Checks Its Work:
Runs file system analysis → NO mass file encryption found
Gap detected: "Wait, ransomware should encrypt files..."

🔄 Agent CORRECTS Itself (Iteration 2):
"Actually, this is CREDENTIAL THEFT!"
Why? Found:
  - 47 failed login attempts
  - LSASS process injection (credential dumping)
  - Registry persistence mechanism

✅ Final Answer: Credential theft via mimikatz
   Confidence: 88%
   MITRE ATT&CK: T1003.001
```

**Key Innovation:** The agent **makes a mistake, detects it, and fixes itself** - all automatically, with full audit trail.

---

## 📂 How to Navigate This Project

### Quick File Tour

```
find-evil-agent/
│
├── 🎬 run_demo.py              ← START HERE! Run the demo
│
├── 🧠 agent/                   ← The "brain" that self-corrects
│   ├── self_correcting_agent.py    (500 lines - the iteration loop)
│   └── evidence_validator.py       (hallucination detector)
│
├── 🔧 mcp_server/              ← The "hands" that run forensic tools
│   └── sift_mcp_server.py          (600 lines - 6 typed tools)
│
├── 📊 observability/           ← The "memory" that logs everything
│   └── logger.py                   (structured audit trail)
│
├── 📁 execution_logs/          ← What happened (demo results)
│   ├── DEMO-001_*.json             (full execution trace)
│   └── DEMO-001_final_report.json  (final incident report)
│
├── 🎨 docs/                    ← Visual guides
│   ├── architecture.png            (diagram for submission)
│   ├── architecture.html           (interactive visualization)
│   └── architecture_diagram.md     (text explanation)
│
├── 📖 README.md                ← Project overview
├── 📋 DEMO_RESULTS.md          ← Demo output explained
└── 🧭 NAVIGATION_GUIDE.md      ← YOU ARE HERE!
```

---

## 🚶 Guided Tour: Let's Explore!

### STEP 1: See It in Action (5 minutes)

**Run the demo:**
```bash
cd /Users/kulraj/find-evil-agent
python3 run_demo.py
```

**What you'll see:**
```
Iteration 1: "Ransomware!" (70% confidence) ❌ WRONG
  ↓
Gap detected: No encryption activity
  ↓
Self-correction triggered
  ↓
Iteration 2-5: "Credential theft!" (88% confidence) ✅ CORRECT
  ↓
Final report with MITRE ATT&CK mapping
```

**Watch for these key moments:**
1. 🔴 **"HALLUCINATION DETECTED"** - the validator catching fake findings
2. 🔄 **"SELF-CORRECTION"** - the agent revising its hypothesis
3. ✅ **"CONVERGED"** - the agent is confident it's right

---

### STEP 2: Understand the Architecture (10 minutes)

**Open the visual diagram:**
```bash
open docs/architecture.png
# or interactive version:
open docs/architecture.html
```

**Follow the data flow:**

```
Evidence Sources (disk, memory, logs)
    ↓
Custom MCP Server (6 safe forensic tools)
    ↓
Self-Correcting Agent (5-step iteration loop)
    ├─→ 1. Generate hypothesis
    ├─→ 2. Gather evidence (run tools)
    ├─→ 3. Validate findings (check citations)
    ├─→ 4. Identify gaps (contradictions?)
    └─→ 5. Decide: converge or refine?
         ↓ (if gaps found, loop back!)
    ↓
Audit Trail (structured logs)
```

**Key Innovation:** The loop between steps 4 and 1 is the **self-correction**!

---

### STEP 3: Read the Code (The Brain) (15 minutes)

**Start here:** `agent/self_correcting_agent.py`

**Key function to read:**
```python
def analyze_case(self, case_data):
    """The main loop that makes the agent smart."""

    # Step 1: Make initial guess
    hypothesis = self._initial_triage(case_data)

    # Step 2-5: Iterative refinement (up to 5 times)
    for iteration in range(1, 5):
        # Gather evidence
        evidence = self._gather_evidence(hypothesis)

        # Generate findings
        findings = self._generate_findings(evidence)

        # CRITICAL: Validate against evidence
        validation = self._validate_findings(findings, evidence)

        # Identify gaps/contradictions
        gaps = self._identify_gaps(hypothesis, validation)

        # Decide what to do
        if no_gaps and high_confidence:
            break  # Done!
        else:
            hypothesis = self._refine_hypothesis(gaps)  # Self-correct!

    return final_report
```

**Read in this order:**
1. Line 90: `analyze_case()` - the main loop
2. Line 150: `_initial_triage()` - first guess
3. Line 280: `_validate_findings()` - hallucination detector
4. Line 350: `_identify_gaps()` - contradiction finder
5. Line 410: `_refine_hypothesis()` - self-correction logic

---

### STEP 4: See the Tools (The Hands) (10 minutes)

**Open:** `mcp_server/sift_mcp_server.py`

**What's inside:** 6 forensic tools as **typed Python functions** (not shell commands!)

```python
def analyze_prefetch(image_path, time_range):
    """Shows which programs were executed."""
    # Returns: execution history with timestamps

def extract_mft_timeline(image_path):
    """Shows file creation/modification times."""
    # Returns: file system activity timeline

def parse_event_logs(log_path, event_ids):
    """Shows authentication events."""
    # Returns: login attempts, privilege changes

def analyze_memory_dump(dump_path, plugin):
    """Analyzes memory for malicious processes."""
    # Returns: process injection, credential dumping

def search_registry_hive(hive_path, key_pattern):
    """Finds persistence mechanisms."""
    # Returns: startup programs, scheduled tasks

def get_amcache(registry_hive):
    """Shows application execution artifacts."""
    # Returns: program execution history
```

**Why this is important:**
- ✅ Agent can ONLY call these 6 functions
- ✅ Agent CANNOT run `rm -rf` or any shell command
- ✅ This is an **architectural guardrail** (judges love this!)

**Read in this order:**
1. Line 50: `analyze_prefetch()` - see the structured output format
2. Line 220: `_validate_path()` - see input validation
3. Line 250: Mock implementations - see what real tools would return

---

### STEP 5: See the Hallucination Detector (15 minutes)

**Open:** `agent/evidence_validator.py`

**What it does:** Catches when the agent makes up findings

```python
def validate_finding(claim, cited_artifacts, available_evidence):
    """Check if a finding is real or hallucinated."""

    # Check 1: Do the cited artifacts exist?
    for citation in cited_artifacts:
        if citation not in available_evidence:
            return HALLUCINATION  # Fake citation!

    # Check 2: Does the claim align with artifact content?
    score = check_claim_alignment(claim, available_evidence)
    if score < 0.3:
        return HALLUCINATION  # Claim not supported!

    # Check 3: Are timestamps consistent across artifacts?
    if timeline_inconsistent(cited_artifacts):
        return WEAK_SUPPORT  # Contradictory evidence

    return SUPPORTED  # Finding is valid!
```

**Try this:** Open the demo logs and find hallucination detections:
```bash
cat execution_logs/DEMO-001_final_report.json | grep -A 3 "hallucination"
```

**Read in this order:**
1. Line 30: `validate_finding()` - main validation logic
2. Line 80: `_check_claim_alignment()` - content matching
3. Line 150: `HallucinationDetector` - pattern recognition

---

### STEP 6: Explore the Demo Results (10 minutes)

**Open the final report:**
```bash
cat execution_logs/DEMO-001_final_report.json
```

**Key sections to look for:**

```json
{
  "summary": {
    "hypothesis": "credential_theft",  // ← Final answer
    "confidence": 0.88,                // ← 88% confident
    "total_iterations": 5              // ← Took 5 tries
  },

  "findings": [                        // ← Only validated findings
    {
      "finding_id": "F-002",
      "claim": "Credential dumping via LSASS",
      "mitre_attack": "T1003.001",    // ← Industry standard mapping
      "validated": true                // ← Passed validation!
    }
  ],

  "audit_trail": {
    "total_tools_executed": 11,       // ← 11 forensic tools ran
    "self_corrections": 5,            // ← 5 hypothesis revisions
    "hallucinations_caught": 11       // ← 11 fake findings blocked!
  }
}
```

**Now look at the full execution log:**
```bash
cat execution_logs/DEMO-001_20260613_174809.json | head -100
```

**Find these events:**
- `"event_type": "initial_hypothesis"` - first guess
- `"event_type": "tool_execution"` - tool runs
- `"event_type": "hallucination_detected"` - validator catches fake
- `"event_type": "self_correction"` - hypothesis revision
- `"event_type": "convergence"` - final answer

---

## 🔍 Deep Dive: How Self-Correction Works

### The Magic Moment (Iteration 1 → 2)

**Let's trace through the demo:**

#### Iteration 1: Wrong Hypothesis
```
Agent thinks: "RANSOMWARE"
  ↓
Runs: extract_mft_timeline()
  ↓
Result: "12 file modifications (normal activity)"
  ↓
Gap detector activates:
  "CONTRADICTION: Ransomware should show mass file encryption,
   but MFT timeline shows normal activity!"
  ↓
Decision: REFINE (too many gaps)
```

#### Iteration 2: Self-Correction
```
Agent revises: "CREDENTIAL_THEFT"
  ↓
Runs:
  - parse_event_logs() → 47 failed logins
  - analyze_memory_dump() → LSASS injection
  - search_registry_hive() → persistence via Run key
  ↓
Validator checks:
  ✓ All evidence exists
  ✓ Claims align with artifacts
  ✓ Timelines consistent
  ↓
Gap detector: "No contradictions found"
  ↓
Decision: CONVERGE (high confidence, no gaps)
```

**Code location:** `agent/self_correcting_agent.py` line 410 `_refine_hypothesis()`

---

## 🎯 Key Concepts Explained

### 1. What is "Citation-Mismatch"?

**Bad (hallucination):**
```
Finding: "Registry key HKLM\Software\Malware found"
Citation: "registry_analysis.txt"
Evidence available: ["event_logs.json", "memory_dump.txt"]
                     ↑ registry_analysis.txt doesn't exist!
Result: HALLUCINATION ❌
```

**Good (validated):**
```
Finding: "LSASS injection detected"
Citation: "memory_dump"
Evidence available: ["memory_dump", "event_logs"]
                     ↑ citation exists!
Content check: "lsass_injection: true" ✓
Result: VALIDATED ✅
```

### 2. What is "Gap Analysis"?

The agent asks itself:
- "What evidence am I missing?"
- "Do any findings contradict each other?"
- "Are there unexplained events?"

**Example from demo:**
```
Hypothesis: Ransomware
Expected evidence: Mass file encryption
Actual evidence: 12 normal file modifications
Gap: "Where's the encryption?!"
Action: Revise hypothesis
```

### 3. What is "Architectural Guardrail"?

**Bad approach (Protocol SIFT):**
```python
def execute_shell_cmd(cmd):
    os.system(cmd)  # ← Agent can run ANY command!

# Agent could run: "rm -rf /" 💥
```

**Good approach (FIND EVIL!):**
```python
ALLOWED_TOOLS = {
    "analyze_prefetch": analyze_prefetch_func,
    "extract_mft": extract_mft_func,
    # Only 6 functions allowed!
}

def execute_tool(tool_name):
    if tool_name not in ALLOWED_TOOLS:
        raise Error("Not allowed!")  # ← Agent physically cannot run rm
```

### 4. What is "Audit Trail"?

Every action gets logged with:
- Timestamp (when it happened)
- Execution ID (unique identifier)
- Tool name + arguments
- Result + evidence artifacts

**Example trace:**
```
Finding: "LSASS injection"
  ↓ came from
Evidence: "memory_dump"
  ↓ produced by
Tool execution: analyze_memory_dump(plugin=mimikatz)
  ↓ logged as
Execution ID: exec-0004
  ↓ timestamp
2026-06-13T17:48:09Z
```

Judges can trace **any finding** back to the **exact tool execution** that found it!

---

## 🧪 Interactive Exploration

### Try These Commands:

**1. Run demo and watch terminal:**
```bash
python3 run_demo.py | grep "SELF-CORRECTION"
```

**2. Count hallucinations caught:**
```bash
python3 run_demo.py | grep "HALLUCINATION DETECTED" | wc -l
```

**3. See all tool executions:**
```bash
cat execution_logs/DEMO-001_final_report.json | jq '.audit_trail.iterations[].tools_executed'
```

**4. Extract hypothesis evolution:**
```bash
cat execution_logs/DEMO-001_final_report.json | jq '.audit_trail.iterations[].hypothesis.type'
```

**5. View the self-correction moment:**
```bash
cat execution_logs/DEMO-001_20260613_174809.json | jq '.entries[] | select(.event_type == "self_correction")'
```

---

## 📊 Understanding the Numbers

**From the demo:**
- **5 iterations** = Agent revised hypothesis 5 times
- **11 tool executions** = Ran 11 forensic tools total
- **5 self-corrections** = Changed hypothesis 5 times
- **11 hallucinations caught** = Blocked 11 fake findings
- **1 validated finding** = Only 1 of 3 findings passed validation
- **88% confidence** = Final answer confidence score

**What this means:**
- Agent was careful (rejected weak findings)
- Agent was thorough (tried multiple hypotheses)
- Agent was accurate (caught its own mistakes)

---

## 🎓 Learning Path

### Beginner (30 minutes)
1. ✅ Run demo - see it work
2. ✅ Read this guide - understand concepts
3. ✅ Open architecture diagram - see big picture

### Intermediate (2 hours)
4. Read `self_correcting_agent.py` - understand the loop
5. Read `evidence_validator.py` - understand hallucination detection
6. Trace through demo logs - follow the data flow

### Advanced (4+ hours)
7. Read `sift_mcp_server.py` - understand tool implementations
8. Modify the demo - add your own test case
9. Build a new tool - add to MCP server
10. Write accuracy benchmarks - compare to Protocol SIFT

---

## 🆘 Troubleshooting

**Demo won't run:**
```bash
# Install dependencies
pip3 install boto3 python-dotenv

# Check Python version
python3 --version  # Should be 3.10+
```

**Want to see more detail:**
```bash
# Enable debug logging
export DEBUG=1
python3 run_demo.py
```

**Diagrams won't open:**
```bash
# Use relative path
open ./docs/architecture.png

# Or absolute path
open /Users/kulraj/find-evil-agent/docs/architecture.png
```

---

## 🎯 Quick Reference

**Files by Purpose:**

| I want to... | Open this file |
|--------------|---------------|
| See the demo run | `run_demo.py` |
| Understand self-correction | `agent/self_correcting_agent.py` |
| See hallucination detection | `agent/evidence_validator.py` |
| See available tools | `mcp_server/sift_mcp_server.py` |
| View demo results | `execution_logs/DEMO-001_final_report.json` |
| See architecture | `docs/architecture.png` |
| Read overview | `README.md` |
| Understand demo output | `DEMO_RESULTS.md` |

---

## 💡 Key Takeaways

**What makes this win:**

1. **Self-Correction** - Agent makes mistake (ransomware) → detects contradiction → fixes itself (credential theft)

2. **Hallucination Detection** - Catches 11 fake findings in one demo run

3. **Architectural Guardrails** - Agent physically cannot run dangerous commands (typed functions only)

4. **Full Audit Trail** - Every finding traces back to specific tool execution with timestamp

5. **Visible Reasoning** - Can watch agent "think" through terminal output

---

**Now you understand what FIND EVIL! does and how to explore it!** 🎉

**Next:** Run the demo and watch the self-correction happen live! 🚀
