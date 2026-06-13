#!/usr/bin/env python3
"""
Generate visual architecture diagram for FIND EVIL!

This creates a PNG/SVG diagram using graphviz if available,
or a simple HTML visualization otherwise.
"""

import subprocess
import sys
from pathlib import Path


def check_graphviz():
    """Check if graphviz is installed."""
    try:
        subprocess.run(['dot', '-V'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def generate_graphviz_diagram():
    """Generate diagram using graphviz."""

    dot_content = """
digraph FindEvil {
    rankdir=TB;
    node [shape=box, style=rounded, fontname="Arial"];

    // Evidence Sources
    subgraph cluster_evidence {
        label="Evidence Sources";
        style=filled;
        color=lightgrey;

        disk [label="Disk Image\\ndisk.dd"];
        memory [label="Memory Dump\\nmemory.raw"];
        eventlogs [label="Event Logs\\nSecurity.evtx"];
        registry [label="Registry Hives\\nSYSTEM, SOFTWARE"];
    }

    // MCP Server
    subgraph cluster_mcp {
        label="Custom SIFT MCP Server\\n🔒 Architectural Guardrails";
        style=filled;
        color="#ffcccc";

        prefetch [label="analyze_prefetch()\\nExecution History"];
        mft [label="extract_mft_timeline()\\nFile System"];
        evtparse [label="parse_event_logs()\\nAuth Events"];
        memory_analyze [label="analyze_memory_dump()\\nProcess Injection"];
        registry_search [label="search_registry_hive()\\nPersistence"];
        amcache [label="get_amcache()\\nApp Execution"];

        validation [label="Input Validation\\nPath Sanitization" shape=diamond style=filled color="#ff9999"];
        whitelist [label="Whitelist\\nNo Shell Exec" shape=diamond style=filled color="#ff9999"];
    }

    // Agent
    subgraph cluster_agent {
        label="Self-Correcting Agent\\n🔄 Iteration Loop";
        style=filled;
        color="#ccccff";

        step1 [label="1. Generate/Refine\\nHypothesis" style=filled color="#9999ff"];
        step2 [label="2. Gather Evidence\\nMCP Calls"];
        step3 [label="3. Validate Findings\\nCitation-Mismatch"];
        step4 [label="4. Identify Gaps\\nContradictions"];
        step5 [label="5. Decide Action\\nConverge/Refine" style=filled color="#9999ff"];
    }

    // Validation Layer
    subgraph cluster_validation {
        label="Evidence Validation\\n🛡️ Anti-Hallucination";
        style=filled;
        color="#ccffcc";

        cite_check [label="Citation Check" style=filled color="#99ff99"];
        align_check [label="Claim Alignment" style=filled color="#99ff99"];
        xref [label="Cross-Reference" style=filled color="#99ff99"];
        pattern [label="Pattern Detection" style=filled color="#99ff99"];
    }

    // Observability
    subgraph cluster_obs {
        label="Observability & Audit\\n📊 Criterion #5";
        style=filled;
        color="#ffffcc";

        logger [label="Iteration Logger\\nStructured JSON"];
        trace [label="Execution Trace\\nFinding→Tool→Evidence"];
        audit [label="Audit Trail\\nTimestamps, IDs"];
        report [label="Final Report\\nMITRE ATT&CK"];
    }

    // LLM
    llm [label="AWS Bedrock\\nClaude Sonnet 4.5" shape=ellipse style=filled color="#ffddaa"];

    // Connections - Evidence to MCP
    disk -> prefetch;
    disk -> mft;
    memory -> memory_analyze;
    eventlogs -> evtparse;
    registry -> registry_search;

    // MCP to Validation
    prefetch -> validation;
    mft -> validation;
    evtparse -> validation;
    memory_analyze -> validation;
    registry_search -> validation;
    amcache -> validation;

    validation -> whitelist;

    // Whitelist to Agent
    whitelist -> step2;

    // Agent Loop
    step1 -> step2;
    step2 -> step3;
    step3 -> step4;
    step4 -> step5;
    step5 -> step1 [label="refine" style=dashed];
    step5 -> logger [label="converge"];

    // Validation layer
    step3 -> cite_check;
    cite_check -> align_check;
    align_check -> xref;
    xref -> pattern;
    pattern -> step4;

    // LLM connections
    llm -> step1;
    llm -> step3;

    // Observability
    step1 -> logger;
    step2 -> logger;
    step3 -> logger;
    step4 -> logger;
    step5 -> logger;

    logger -> trace;
    trace -> audit;
    audit -> report;
}
"""

    # Write DOT file
    dot_file = Path("docs/architecture.dot")
    with open(dot_file, "w") as f:
        f.write(dot_content)

    # Generate PNG
    png_file = Path("docs/architecture.png")
    subprocess.run(['dot', '-Tpng', str(dot_file), '-o', str(png_file)], check=True)

    # Generate SVG
    svg_file = Path("docs/architecture.svg")
    subprocess.run(['dot', '-Tsvg', str(dot_file), '-o', str(svg_file)], check=True)

    print(f"✅ Generated diagrams:")
    print(f"   PNG: {png_file.absolute()}")
    print(f"   SVG: {svg_file.absolute()}")
    print(f"   DOT: {dot_file.absolute()}")

    return True


def generate_html_diagram():
    """Generate simple HTML visualization."""

    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>FIND EVIL! Architecture</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .layer {
            margin: 20px 0;
            padding: 20px;
            border-radius: 8px;
            border: 2px solid #ddd;
        }
        .evidence { background: #e8f5e9; border-color: #4CAF50; }
        .mcp { background: #ffebee; border-color: #f44336; }
        .agent { background: #e3f2fd; border-color: #2196F3; }
        .validation { background: #f1f8e9; border-color: #8BC34A; }
        .observability { background: #fff9c4; border-color: #FFC107; }

        .component {
            display: inline-block;
            margin: 10px;
            padding: 15px 20px;
            background: white;
            border-radius: 5px;
            border: 1px solid #ccc;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .flow-arrow {
            text-align: center;
            font-size: 24px;
            color: #666;
            margin: 10px 0;
        }
        .highlight {
            background: #ffeb3b;
            padding: 2px 6px;
            border-radius: 3px;
        }
        .metric {
            display: inline-block;
            margin: 10px 20px 10px 0;
            padding: 10px 15px;
            background: #e0e0e0;
            border-radius: 5px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 FIND EVIL! Architecture</h1>
        <p><strong>Self-Correcting IR Triage Agent</strong></p>

        <div class="layer evidence">
            <h2>📁 Evidence Sources</h2>
            <div class="component">Disk Image<br/><small>disk.dd</small></div>
            <div class="component">Memory Dump<br/><small>memory.raw</small></div>
            <div class="component">Event Logs<br/><small>Security.evtx</small></div>
            <div class="component">Registry Hives<br/><small>SYSTEM, SOFTWARE</small></div>
        </div>

        <div class="flow-arrow">↓</div>

        <div class="layer mcp">
            <h2>🔒 Custom SIFT MCP Server</h2>
            <p><span class="highlight">Criterion #4: Architectural Guardrails</span></p>
            <div class="component">analyze_prefetch()<br/><small>Execution History</small></div>
            <div class="component">extract_mft_timeline()<br/><small>File System</small></div>
            <div class="component">parse_event_logs()<br/><small>Auth Events</small></div>
            <div class="component">analyze_memory_dump()<br/><small>Process Injection</small></div>
            <div class="component">search_registry_hive()<br/><small>Persistence</small></div>
            <div class="component">get_amcache()<br/><small>App Execution</small></div>
            <p style="margin-top: 15px;">
                ✓ Input Validation &nbsp; ✓ Whitelist Enforcement &nbsp; ✓ No Shell Execution
            </p>
        </div>

        <div class="flow-arrow">↓ MCP Protocol</div>

        <div class="layer agent">
            <h2>🔄 Self-Correcting Agent</h2>
            <p><span class="highlight">Criterion #1: Autonomous Execution (TIEBREAKER)</span></p>
            <div class="component" style="background: #bbdefb;">1. Generate/Refine<br/>Hypothesis</div>
            <div class="flow-arrow" style="display: inline;">→</div>
            <div class="component">2. Gather Evidence<br/>MCP Calls</div>
            <div class="flow-arrow" style="display: inline;">→</div>
            <div class="component">3. Validate Findings<br/>Citation-Mismatch</div>
            <div class="flow-arrow" style="display: inline;">→</div>
            <div class="component">4. Identify Gaps<br/>Contradictions</div>
            <div class="flow-arrow" style="display: inline;">→</div>
            <div class="component" style="background: #bbdefb;">5. Decide Action<br/>Converge/Refine</div>
            <p style="margin-top: 15px;">
                ↺ Loop: Refine hypothesis based on gaps (max 5 iterations)
            </p>
        </div>

        <div class="layer validation">
            <h2>🛡️ Evidence Validation Layer</h2>
            <p><span class="highlight">Criterion #2: Anti-Hallucination</span></p>
            <div class="component">Citation Check<br/><small>Do artifacts exist?</small></div>
            <div class="component">Claim Alignment<br/><small>Evidence supports?</small></div>
            <div class="component">Cross-Reference<br/><small>Timeline consistency</small></div>
            <div class="component">Pattern Detection<br/><small>Fake paths/names</small></div>
        </div>

        <div class="flow-arrow">↓</div>

        <div class="layer observability">
            <h2>📊 Observability & Audit</h2>
            <p><span class="highlight">Criterion #5: Audit Trail Quality</span></p>
            <div class="component">Iteration Logger<br/><small>Structured JSON</small></div>
            <div class="component">Execution Trace<br/><small>Finding→Tool→Evidence</small></div>
            <div class="component">Audit Trail<br/><small>Timestamps, IDs</small></div>
            <div class="component">Final Report<br/><small>MITRE ATT&CK</small></div>
        </div>

        <hr style="margin: 30px 0;"/>

        <h2>📈 Demo Results</h2>
        <div class="metric">5 Iterations</div>
        <div class="metric">11 Tool Executions</div>
        <div class="metric">5 Self-Corrections</div>
        <div class="metric">11 Hallucinations Caught</div>
        <div class="metric">88% Final Confidence</div>

        <h3>Self-Correction Sequence:</h3>
        <p>
            <strong>Iteration 1:</strong> Hypothesis = <span style="color: red;">RANSOMWARE</span> (70% confidence) ❌ WRONG<br/>
            <strong>Gap Found:</strong> MFT timeline shows NO mass file encryption<br/>
            <strong>Iteration 2-5:</strong> Hypothesis = <span style="color: green;">CREDENTIAL_THEFT</span> (88% confidence) ✅ CORRECT
        </p>

        <hr style="margin: 30px 0;"/>

        <h2>🏆 Why This Wins</h2>
        <ul>
            <li><strong>#1 Autonomous Execution:</strong> Self-correction loop with visible iterations</li>
            <li><strong>#2 IR Accuracy:</strong> Evidence validation layer catches hallucinations</li>
            <li><strong>#4 Constraints:</strong> Architectural guardrails (typed functions, no shell)</li>
            <li><strong>#5 Audit Trail:</strong> Full trace from finding → tool → evidence</li>
        </ul>
    </div>
</body>
</html>"""

    html_file = Path("docs/architecture.html")
    with open(html_file, "w") as f:
        f.write(html_content)

    print(f"✅ Generated HTML diagram:")
    print(f"   {html_file.absolute()}")
    print(f"\nOpen in browser: file://{html_file.absolute()}")

    return True


if __name__ == "__main__":
    print("🎨 Generating FIND EVIL! Architecture Diagram...\n")

    if check_graphviz():
        print("✓ Graphviz detected - generating PNG/SVG diagrams\n")
        try:
            generate_graphviz_diagram()
        except Exception as e:
            print(f"❌ Graphviz generation failed: {e}")
            print("Falling back to HTML...\n")
            generate_html_diagram()
    else:
        print("⚠ Graphviz not found (install with: brew install graphviz)")
        print("Generating HTML diagram instead...\n")
        generate_html_diagram()

    print("\n✅ Diagram generation complete!")
    print("\n📄 Also see: docs/architecture_diagram.md (Mermaid + ASCII)")
