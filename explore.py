#!/usr/bin/env python3
"""
Interactive Explorer for FIND EVIL!

Navigate and understand the codebase interactively.
"""

import os
import sys
import json
from pathlib import Path


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')


def show_menu():
    """Display main menu."""
    clear_screen()
    print("="*80)
    print("🔍 FIND EVIL! Interactive Explorer")
    print("="*80)
    print()
    print("What would you like to explore?")
    print()
    print("  1. 🎬 Run the demo (see self-correction in action)")
    print("  2. 📊 View demo results (what happened)")
    print("  3. 🧠 Explore the agent brain (self-correction logic)")
    print("  4. 🔧 Explore the MCP tools (forensic functions)")
    print("  5. 🛡️ Explore the validator (hallucination detector)")
    print("  6. 📋 View execution logs (full audit trail)")
    print("  7. 🎨 View architecture diagram")
    print("  8. 📖 Read the navigation guide")
    print("  9. ❓ How does self-correction work?")
    print("  0. 🚪 Exit")
    print()
    return input("Enter your choice (0-9): ").strip()


def run_demo():
    """Run the demo."""
    clear_screen()
    print("="*80)
    print("🎬 Running Demo - Watch for Self-Correction!")
    print("="*80)
    print()
    print("Key moments to watch:")
    print("  🔴 HALLUCINATION DETECTED - validator catching fakes")
    print("  🔄 SELF-CORRECTION - agent revising hypothesis")
    print("  ✅ CONVERGED - agent found the answer")
    print()
    input("Press Enter to start...")
    os.system("python3 run_demo.py")
    input("\nPress Enter to continue...")


def view_results():
    """Show demo results summary."""
    clear_screen()
    print("="*80)
    print("📊 Demo Results Summary")
    print("="*80)
    print()

    report_path = Path("execution_logs/DEMO-001_final_report.json")
    if report_path.exists():
        with open(report_path) as f:
            report = json.load(f)

        summary = report.get("summary", {})
        print(f"Final Hypothesis: {summary.get('hypothesis', 'N/A').upper()}")
        print(f"Confidence: {summary.get('confidence', 0):.1%}")
        print(f"Total Iterations: {summary.get('total_iterations', 0)}")
        print(f"Converged: {'Yes' if summary.get('converged') else 'No'}")
        print()

        print("Validated Findings:")
        for finding in report.get("findings", []):
            print(f"  • [{finding['finding_id']}] {finding['claim']}")
            print(f"    Confidence: {finding['confidence']:.1%}")
            print(f"    MITRE ATT&CK: {finding.get('mitre_attack', 'N/A')}")
            print()

        audit = report.get("audit_trail", {})
        print("Audit Trail Statistics:")
        print(f"  Tools executed: {audit.get('total_tools_executed', 0)}")
        print(f"  Self-corrections: {audit.get('self_corrections', 0)}")
        print(f"  Hallucinations caught: {audit.get('hallucinations_caught', 0)}")

    else:
        print("No demo results found. Run the demo first (option 1).")

    print()
    input("Press Enter to continue...")


def explore_agent():
    """Explain the agent's self-correction logic."""
    clear_screen()
    print("="*80)
    print("🧠 Agent Brain - Self-Correction Loop")
    print("="*80)
    print()
    print("Location: agent/self_correcting_agent.py")
    print()
    print("Main Loop (line 90 - analyze_case):")
    print()
    print("  for iteration in range(1, MAX_ITERATIONS):")
    print("      ┌─────────────────────────────────────┐")
    print("      │ 1. Generate/Refine Hypothesis       │")
    print("      │    - LLM generates theory           │")
    print("      └─────────────────┬───────────────────┘")
    print("                        ↓")
    print("      ┌─────────────────────────────────────┐")
    print("      │ 2. Gather Evidence                  │")
    print("      │    - Run MCP tools                  │")
    print("      └─────────────────┬───────────────────┘")
    print("                        ↓")
    print("      ┌─────────────────────────────────────┐")
    print("      │ 3. Validate Findings                │")
    print("      │    - Check citations exist          │")
    print("      │    - Verify claims match evidence   │")
    print("      └─────────────────┬───────────────────┘")
    print("                        ↓")
    print("      ┌─────────────────────────────────────┐")
    print("      │ 4. Identify Gaps                    │")
    print("      │    - Missing evidence?              │")
    print("      │    - Contradictions?                │")
    print("      └─────────────────┬───────────────────┘")
    print("                        ↓")
    print("      ┌─────────────────────────────────────┐")
    print("      │ 5. Decide Action                    │")
    print("      │    - Converge (done!)               │")
    print("      │    - Refine (loop back to step 1)   │")
    print("      └─────────────────────────────────────┘")
    print("                        │")
    print("          if gaps found │")
    print("                ┌───────┘")
    print("                └───────> SELF-CORRECTION!")
    print()
    print("Key functions to read:")
    print("  - Line 150: _initial_triage() - first guess")
    print("  - Line 280: _validate_findings() - hallucination check")
    print("  - Line 350: _identify_gaps() - find contradictions")
    print("  - Line 410: _refine_hypothesis() - self-correction logic")
    print()
    choice = input("Open the file? (y/n): ").strip().lower()
    if choice == 'y':
        os.system("cat agent/self_correcting_agent.py | less")


def explore_tools():
    """Show MCP tools."""
    clear_screen()
    print("="*80)
    print("🔧 MCP Server - Forensic Tools")
    print("="*80)
    print()
    print("Location: mcp_server/sift_mcp_server.py")
    print()
    print("Available Tools (Architectural Guardrails):")
    print()
    print("  1. analyze_prefetch()")
    print("     Purpose: Show which programs were executed")
    print("     Returns: Execution history with timestamps")
    print()
    print("  2. extract_mft_timeline()")
    print("     Purpose: Show file creation/modification activity")
    print("     Returns: File system timeline")
    print()
    print("  3. parse_event_logs()")
    print("     Purpose: Show authentication events")
    print("     Returns: Login attempts, privilege changes")
    print()
    print("  4. analyze_memory_dump()")
    print("     Purpose: Analyze memory for malicious processes")
    print("     Returns: Process injection, credential dumping")
    print()
    print("  5. search_registry_hive()")
    print("     Purpose: Find persistence mechanisms")
    print("     Returns: Startup programs, scheduled tasks")
    print()
    print("  6. get_amcache()")
    print("     Purpose: Application execution artifacts")
    print("     Returns: Program execution history")
    print()
    print("CRITICAL: Agent can ONLY call these 6 functions!")
    print("          Agent CANNOT run shell commands like 'rm -rf'")
    print()
    choice = input("Open the file? (y/n): ").strip().lower()
    if choice == 'y':
        os.system("cat mcp_server/sift_mcp_server.py | less")


def explore_validator():
    """Show validation logic."""
    clear_screen()
    print("="*80)
    print("🛡️ Evidence Validator - Hallucination Detector")
    print("="*80)
    print()
    print("Location: agent/evidence_validator.py")
    print()
    print("How it catches hallucinations:")
    print()
    print("  Check 1: Citation Exists?")
    print("    Finding: 'Registry key found'")
    print("    Citation: 'registry_analysis.txt'")
    print("    Evidence: ['memory_dump', 'event_logs']")
    print("    Result: ❌ HALLUCINATION (citation doesn't exist)")
    print()
    print("  Check 2: Claim Alignment")
    print("    Finding: 'LSASS injection detected'")
    print("    Evidence content: 'lsass_injection: true'")
    print("    Result: ✅ SUPPORTED (claim matches evidence)")
    print()
    print("  Check 3: Timeline Consistency")
    print("    Event A: 14:23:00")
    print("    Event B: 14:23:05")
    print("    Result: ✅ CONSISTENT (same time window)")
    print()
    print("  Check 4: Pattern Detection")
    print("    Path: 'C:\\Malware\\evil.exe'")
    print("    Result: ⚠️ SUSPICIOUS (fake path pattern)")
    print()
    choice = input("Open the file? (y/n): ").strip().lower()
    if choice == 'y':
        os.system("cat agent/evidence_validator.py | less")


def view_logs():
    """Show execution logs."""
    clear_screen()
    print("="*80)
    print("📋 Execution Logs - Audit Trail")
    print("="*80)
    print()

    logs_dir = Path("execution_logs")
    if logs_dir.exists():
        log_files = sorted(logs_dir.glob("*.json"))
        if log_files:
            print("Available logs:")
            for i, log_file in enumerate(log_files, 1):
                size_kb = log_file.stat().st_size / 1024
                print(f"  {i}. {log_file.name} ({size_kb:.1f} KB)")

            print()
            choice = input("Enter number to view (or Enter to skip): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(log_files):
                log_file = log_files[int(choice) - 1]
                os.system(f"cat {log_file} | jq . | less")
        else:
            print("No logs found. Run the demo first (option 1).")
    else:
        print("No logs directory found. Run the demo first (option 1).")

    input("\nPress Enter to continue...")


def view_diagram():
    """Show architecture diagram."""
    clear_screen()
    print("="*80)
    print("🎨 Architecture Diagram")
    print("="*80)
    print()
    print("Available formats:")
    print("  1. PNG image (high resolution)")
    print("  2. Interactive HTML")
    print("  3. ASCII text (view in terminal)")
    print()
    choice = input("Choose format (1-3): ").strip()

    if choice == '1':
        os.system("open docs/architecture.png 2>/dev/null || echo 'File not found. Generate with: python3 docs/generate_diagram.py'")
    elif choice == '2':
        os.system("open docs/architecture.html 2>/dev/null || echo 'File not found. Generate with: python3 docs/generate_diagram.py'")
    elif choice == '3':
        os.system("cat docs/architecture_diagram.md | less")

    input("\nPress Enter to continue...")


def read_guide():
    """Show navigation guide."""
    os.system("cat NAVIGATION_GUIDE.md | less")


def explain_self_correction():
    """Explain self-correction with demo example."""
    clear_screen()
    print("="*80)
    print("❓ How Does Self-Correction Work?")
    print("="*80)
    print()
    print("DEMO EXAMPLE - Ransomware → Credential Theft")
    print()
    print("ITERATION 1: Wrong Hypothesis")
    print("─" * 40)
    print("Agent thinks: 'This is RANSOMWARE'")
    print("  Why? Found suspicious.exe executed 5 times")
    print("  Confidence: 70%")
    print()
    print("Agent runs: extract_mft_timeline()")
    print("  Result: '12 file modifications (normal activity)'")
    print()
    print("Gap Detector activates:")
    print("  ⚠️ CONTRADICTION!")
    print("  'Ransomware should show mass file encryption,")
    print("   but MFT shows normal activity!'")
    print()
    print("Decision: REFINE hypothesis (too many gaps)")
    print()
    print("="*80)
    print()
    input("Press Enter to see what happens next...")
    print()
    print("ITERATION 2: Self-Correction")
    print("─" * 40)
    print("Agent revises: 'This is CREDENTIAL THEFT'")
    print("  Why? Re-analyzing with new hypothesis")
    print("  Confidence: 88%")
    print()
    print("Agent runs:")
    print("  - parse_event_logs() → 47 failed login attempts")
    print("  - analyze_memory_dump() → LSASS injection detected")
    print("  - search_registry_hive() → Persistence via Run key")
    print()
    print("Validator checks all findings:")
    print("  ✓ All evidence artifacts exist")
    print("  ✓ Claims align with artifact content")
    print("  ✓ Timelines are consistent")
    print()
    print("Gap Detector:")
    print("  ✅ No contradictions found")
    print("  ✅ All evidence supports hypothesis")
    print()
    print("Decision: CONVERGE (high confidence, no gaps)")
    print()
    print("="*80)
    print()
    print("RESULT: Agent corrected itself!")
    print("  Initial: Ransomware ❌")
    print("  Final: Credential Theft ✅")
    print("  Confidence: 88%")
    print("  MITRE ATT&CK: T1003.001 (LSASS Memory)")
    print()
    input("Press Enter to continue...")


def main():
    """Main interactive loop."""
    while True:
        choice = show_menu()

        if choice == '1':
            run_demo()
        elif choice == '2':
            view_results()
        elif choice == '3':
            explore_agent()
        elif choice == '4':
            explore_tools()
        elif choice == '5':
            explore_validator()
        elif choice == '6':
            view_logs()
        elif choice == '7':
            view_diagram()
        elif choice == '8':
            read_guide()
        elif choice == '9':
            explain_self_correction()
        elif choice == '0':
            clear_screen()
            print("👋 Thanks for exploring FIND EVIL!")
            print()
            print("Quick commands:")
            print("  python3 run_demo.py           # Run the demo")
            print("  cat NAVIGATION_GUIDE.md       # Read the guide")
            print("  open docs/architecture.png    # View diagram")
            print()
            sys.exit(0)
        else:
            print("\nInvalid choice. Press Enter to try again...")
            input()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
        sys.exit(0)
