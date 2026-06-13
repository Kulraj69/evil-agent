# 🚀 START HERE - Quick Navigation

**Welcome to FIND EVIL! - Self-Correcting IR Agent**

---

## ⚡ Quick Start (5 Minutes)

### Option 1: Interactive Explorer (Recommended)
```bash
python3 explore.py
```

**This gives you a menu to:**
- ✅ Run the demo
- ✅ View results
- ✅ Explore the code
- ✅ See diagrams
- ✅ Read explanations

### Option 2: Run Demo Directly
```bash
python3 run_demo.py
```

Watch for:
- 🔴 **HALLUCINATION DETECTED**
- 🔄 **SELF-CORRECTION**
- ✅ **CONVERGED**

### Option 3: View Architecture
```bash
open docs/architecture.png
# or interactive:
open docs/architecture.html
```

---

## 🎯 What Does This Do?

**Simple explanation:**
An AI agent investigates security incidents, makes a mistake, detects the mistake, and corrects itself automatically.

**Demo example:**
1. Agent thinks: "This is ransomware!" ❌
2. Agent checks: "Wait, no file encryption found..."
3. Agent corrects: "Actually, this is credential theft!" ✅
4. Final answer: LSASS credential dumping (88% confidence)

---

## 📂 Key Files

| File | What It Does |
|------|--------------|
| `explore.py` | Interactive menu (START HERE!) |
| `run_demo.py` | Run the self-correction demo |
| `NAVIGATION_GUIDE.md` | Complete explanation (read this!) |
| `docs/architecture.png` | Visual diagram |
| `agent/self_correcting_agent.py` | The brain (500 lines) |
| `mcp_server/sift_mcp_server.py` | The tools (600 lines) |
| `execution_logs/` | Demo results |

---

## 🎬 Three Ways to Explore

### 1. Interactive Menu
```bash
python3 explore.py
```
Choose from 9 options to navigate the project.

### 2. Read the Guide
```bash
cat NAVIGATION_GUIDE.md | less
# or in browser:
open NAVIGATION_GUIDE.md
```
Comprehensive explanation of everything.

### 3. Run and Inspect
```bash
# Run demo
python3 run_demo.py

# View results
cat execution_logs/DEMO-001_final_report.json | jq .

# Read the code
cat agent/self_correcting_agent.py | less
```

---

## 🧠 Core Concept: Self-Correction

```
Initial Hypothesis → Evidence → Contradiction Found
         ↓                              ↓
    WRONG GUESS              GAP DETECTED
         ↓                              ↓
         └──────────> SELF-CORRECT ─────┘
                            ↓
                     New Hypothesis → Evidence → Validated!
                                                      ↓
                                                 CONVERGED ✅
```

**In the demo:**
- Ransomware (70%) → No encryption found → REVISE
- Credential Theft (88%) → All evidence checks out → DONE!

---

## 📊 Demo Statistics

**What you'll see:**
- **5 iterations** - agent refined hypothesis 5 times
- **11 tool executions** - ran 11 forensic tools
- **11 hallucinations caught** - blocked 11 fake findings
- **1 validated finding** - only 1 of 3 passed validation
- **88% confidence** - final answer confidence

---

## 🏆 Why This Wins SANS Hackathon

**Criterion #1 (TIEBREAKER): Autonomous Execution**
✅ Self-correction loop with 5 iterations
✅ Visible reasoning at each step
✅ Gap-driven refinement

**Criterion #2: IR Accuracy**
✅ Hallucination detector catches 11 fakes
✅ Evidence validation layer
✅ Citation-mismatch checking

**Criterion #4: Architectural Constraints**
✅ Custom MCP server (6 typed functions)
✅ No shell execution capability
✅ Whitelist enforcement

**Criterion #5: Audit Trail**
✅ Full trace: finding → tool → evidence
✅ Structured JSON logs
✅ Execution IDs for everything

---

## 🎯 Quick Commands

```bash
# Interactive explorer (recommended)
python3 explore.py

# Run demo
python3 run_demo.py

# View results
cat execution_logs/DEMO-001_final_report.json

# See architecture
open docs/architecture.png

# Read guide
cat NAVIGATION_GUIDE.md

# View logs
ls -lh execution_logs/
```

---

## 🆘 Need Help?

**Read in order:**
1. ✅ This file (START_HERE.md) - you are here!
2. ✅ Run `python3 explore.py` - interactive navigation
3. ✅ Read `NAVIGATION_GUIDE.md` - detailed guide
4. ✅ View `docs/architecture.png` - visual overview

**Or just:**
```bash
python3 explore.py
# Choose option 9: "How does self-correction work?"
```

---

## 🚀 Next Steps

1. **Run the explorer:** `python3 explore.py`
2. **Choose option 1:** Run the demo
3. **Choose option 9:** Learn how self-correction works
4. **Choose option 8:** Read the full guide

---

**Ready to explore? Run:** `python3 explore.py` 🎯
