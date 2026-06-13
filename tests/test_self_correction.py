"""End-to-end tests that the agent self-corrects across all incident types."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest

from agent.self_correcting_agent import SelfCorrectingAgent
from mcp_server.sift_mcp_server import SIFTMCPServer
from observability.logger import IterationLogger
from run_all_scenarios import ScenarioLLMClient


def load_live_cases():
    data = json.loads((ROOT / "datasets" / "benchmark_cases.json").read_text())
    return [c for c in data["cases"]
            if not c.get("status", "").startswith("real_image_reference")]


@pytest.mark.parametrize("case", load_live_cases(), ids=lambda c: c["case_id"])
def test_agent_self_corrects_to_truth(case, tmp_path):
    truth = case["ground_truth"]["incident_type"]
    decoy = case["ground_truth"]["decoy_hypothesis"]

    mcp = SIFTMCPServer(scenario=truth)
    llm = ScenarioLLMClient(decoy=decoy, truth=truth)
    logger = IterationLogger(case_id=case["case_id"], log_dir=str(tmp_path))
    agent = SelfCorrectingAgent(mcp_tools=mcp, llm_client=llm, logger=logger)

    report = agent.analyze_case({"case_id": case["case_id"], **case["evidence"]})

    # Converges on the correct incident type, starting from the wrong decoy
    assert report["summary"]["hypothesis"] == truth
    assert decoy != truth  # sanity: the decoy really is wrong
    # At least one self-correction happened
    assert report["audit_trail"]["self_corrections"] >= 1
    # Token usage was logged
    assert report["audit_trail"]["token_usage"]["llm_calls"] >= 1


def test_no_validated_hallucinations_in_final_report(tmp_path):
    case = load_live_cases()[0]
    truth = case["ground_truth"]["incident_type"]
    mcp = SIFTMCPServer(scenario=truth)
    llm = ScenarioLLMClient(decoy=case["ground_truth"]["decoy_hypothesis"], truth=truth)
    logger = IterationLogger(case_id=case["case_id"], log_dir=str(tmp_path))
    agent = SelfCorrectingAgent(mcp_tools=mcp, llm_client=llm, logger=logger)
    report = agent.analyze_case({"case_id": case["case_id"], **case["evidence"]})
    # Every finding in the final report is validated
    assert all(f["validated"] for f in report["findings"])
