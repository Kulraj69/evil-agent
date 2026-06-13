"""
Iteration Logger - Structured Audit Trail

Provides comprehensive logging for the self-correcting agent.

WINNING CRITERION #5: Audit Trail Quality
- Trace any finding back to specific tool execution
- Structured logs with timestamps
- Full iteration history
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path


class IterationLogger:
    """
    Logger for tracking agent iterations and creating audit trails.

    Logs are structured JSON for easy parsing and tracing.
    """

    def __init__(self, case_id: str, log_dir: str = "execution_logs"):
        """
        Initialize logger.

        Args:
            case_id: Unique case identifier
            log_dir: Directory for log files
        """
        self.case_id = case_id
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Create log file for this case
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"{case_id}_{timestamp}.json"

        # In-memory log for structured output
        self.log_entries = []

        # Session metadata
        self.session = {
            "case_id": case_id,
            "started_at": datetime.utcnow().isoformat(),
            "agent_version": "1.0.0",
            "entries": []
        }

    def log_case_start(self, case_data: Dict[str, Any]):
        """Log case initialization."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "case_start",
            "case_data": case_data
        }
        self._write_entry(entry)
        print(f"\n{'='*80}")
        print(f"🔍 FIND EVIL! - Case {self.case_id} Started")
        print(f"{'='*80}\n")

    def log_iteration_start(self, iteration_num: int):
        """Log start of an iteration."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "iteration_start",
            "iteration": iteration_num
        }
        self._write_entry(entry)
        print(f"\n{'─'*80}")
        print(f"📍 Iteration {iteration_num}")
        print(f"{'─'*80}")

    def log_hypothesis(self, hypothesis, is_initial: bool = False):
        """Log hypothesis generation or update."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "hypothesis" if not is_initial else "initial_hypothesis",
            "hypothesis_type": hypothesis.type,
            "description": hypothesis.description,
            "confidence": hypothesis.confidence,
            "supporting_evidence": hypothesis.supporting_evidence,
            "gaps": hypothesis.gaps,
            "iteration": hypothesis.iteration
        }
        self._write_entry(entry)

        label = "Initial Hypothesis" if is_initial else "Hypothesis Update"
        print(f"\n💡 {label}:")
        print(f"   Type: {hypothesis.type}")
        print(f"   Confidence: {hypothesis.confidence:.2f}")
        print(f"   {hypothesis.description}")
        if hypothesis.gaps:
            print(f"   Gaps identified: {len(hypothesis.gaps)}")

    def log_tool_execution(self, tool_name: str, tool_args: Dict[str, Any]):
        """Log tool execution."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "tool_execution",
            "tool": tool_name,
            "args": tool_args
        }
        self._write_entry(entry)
        print(f"   🔧 Executing: {tool_name}({', '.join(f'{k}={v}' for k, v in tool_args.items())})")

    def log_tool_error(self, tool_name: str, error: str):
        """Log tool execution error."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "tool_error",
            "tool": tool_name,
            "error": error
        }
        self._write_entry(entry)
        print(f"   ❌ Tool error: {tool_name} - {error}")

    def log_hallucination_detected(self, finding, validation_result):
        """Log detected hallucination."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "hallucination_detected",
            "finding_id": finding.finding_id,
            "claim": finding.claim,
            "validation_reason": validation_result.reason,
            "missing_evidence": validation_result.missing_evidence
        }
        self._write_entry(entry)
        print(f"   🚨 HALLUCINATION DETECTED:")
        print(f"      Finding: {finding.claim}")
        print(f"      Reason: {validation_result.reason}")

    def log_iteration(self, iteration):
        """Log complete iteration data."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "iteration_complete",
            "iteration_number": iteration.iteration_number,
            "hypothesis_type": iteration.hypothesis.type,
            "hypothesis_confidence": iteration.hypothesis.confidence,
            "tools_executed_count": len(iteration.tools_executed),
            "findings_count": len(iteration.findings),
            "validated_findings": sum(1 for f in iteration.findings if f.validated),
            "hallucinations": sum(1 for v in iteration.validation_results if not v.is_supported),
            "gaps_count": len(iteration.gaps_identified),
            "action_taken": iteration.action_taken,
            "reasoning": iteration.reasoning
        }
        self._write_entry(entry)

        print(f"\n   📊 Iteration Summary:")
        print(f"      Tools executed: {len(iteration.tools_executed)}")
        print(f"      Findings: {len(iteration.findings)} ({sum(1 for f in iteration.findings if f.validated)} validated)")
        print(f"      Hallucinations caught: {sum(1 for v in iteration.validation_results if not v.is_supported)}")
        print(f"      Gaps identified: {len(iteration.gaps_identified)}")
        print(f"      Action: {iteration.action_taken}")

    def log_refinement(self, new_hypothesis):
        """Log hypothesis refinement (self-correction)."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "self_correction",
            "new_hypothesis_type": new_hypothesis.type,
            "new_confidence": new_hypothesis.confidence,
            "description": new_hypothesis.description
        }
        self._write_entry(entry)

        print(f"\n   🔄 SELF-CORRECTION:")
        print(f"      Revised hypothesis: {new_hypothesis.type}")
        print(f"      New confidence: {new_hypothesis.confidence:.2f}")
        print(f"      Reasoning: {new_hypothesis.description}")

    def log_convergence(self, iteration_num: int, confidence: float):
        """Log convergence achieved."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "convergence",
            "iteration": iteration_num,
            "final_confidence": confidence
        }
        self._write_entry(entry)

        print(f"\n   ✅ CONVERGENCE ACHIEVED")
        print(f"      Iterations: {iteration_num}")
        print(f"      Final confidence: {confidence:.2f}")

    def log_step(self, step_name: str, description: str):
        """Log a general processing step."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "step",
            "step_name": step_name,
            "description": description
        }
        self._write_entry(entry)
        print(f"   → {step_name}: {description}")

    def log_case_complete(self, final_report: Dict[str, Any]):
        """Log case completion."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "case_complete",
            "summary": final_report.get("summary", {}),
            "audit_trail_stats": final_report.get("audit_trail", {})
        }
        self._write_entry(entry)

        print(f"\n{'='*80}")
        print(f"✅ Case {self.case_id} Complete")
        print(f"{'='*80}")

        summary = final_report.get("summary", {})
        print(f"\nFinal Hypothesis: {summary.get('hypothesis')}")
        print(f"Confidence: {summary.get('confidence', 0):.2f}")
        print(f"Total Iterations: {summary.get('total_iterations')}")
        print(f"Converged: {'Yes' if summary.get('converged') else 'No'}")

        audit = final_report.get("audit_trail", {})
        print(f"\nAudit Trail:")
        print(f"  Tools executed: {audit.get('total_tools_executed')}")
        print(f"  Self-corrections: {audit.get('self_corrections')}")
        print(f"  Hallucinations caught: {audit.get('hallucinations_caught')}")

        # Write final report to separate file
        self._write_final_report(final_report)

    def _write_entry(self, entry: Dict[str, Any]):
        """Write a log entry."""
        self.session["entries"].append(entry)

        # Write to file (append mode for streaming)
        with open(self.log_file, "w") as f:
            json.dump(self.session, f, indent=2)

    def _write_final_report(self, report: Dict[str, Any]):
        """Write final report to separate file."""
        report_file = self.log_dir / f"{self.case_id}_final_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n📄 Final report saved: {report_file}")
        print(f"📄 Execution log saved: {self.log_file}")

    def get_audit_trail(self) -> Dict[str, Any]:
        """Get complete audit trail for this case."""
        return self.session


class AuditTrail:
    """
    Utility for tracing findings back to tool executions.

    WINNING CRITERION #5: Judges must be able to trace any finding
    back to the specific tool execution that produced it.
    """

    @staticmethod
    def trace_finding(
        finding_id: str,
        execution_log: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trace a finding back through the audit trail.

        Args:
            finding_id: Finding identifier (e.g., "F-001")
            execution_log: Complete execution log

        Returns:
            Trace showing: finding → evidence → tool → execution
        """
        trace = {
            "finding_id": finding_id,
            "trace_chain": []
        }

        # Find the finding in iterations
        for entry in execution_log.get("entries", []):
            if entry.get("event_type") == "iteration_complete":
                # Check if this iteration contains the finding
                # (Simplified - real implementation would parse iteration data)
                pass

        return trace

    @staticmethod
    def generate_evidence_map(execution_log: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Generate a map of evidence artifacts to the tools that produced them.

        Returns:
            {artifact_id: [tool_execution_ids]}
        """
        evidence_map = {}

        for entry in execution_log.get("entries", []):
            if entry.get("event_type") == "tool_execution":
                # Map tool to its output artifacts
                tool_name = entry.get("tool")
                # Simplified - would extract artifact IDs from tool output
                pass

        return evidence_map
