# -*- coding: utf-8 -*-
"""
enterprise_client.py
====================
INVARIANT SAT Platform — Zero-IP Enterprise REST API & GitHub Action CLI Client
-----------------------------------------------------------------------------
Zero-IP HTTP Client that sends circuit constraints to your secure private 
Invariant SAT API Server endpoint and formats security verification reports.

Zero solver algorithms, Zero C++ DLLs, Zero internal secrets contained.
"""

import sys
import os
import argparse
import json
import time
import urllib.request
import urllib.parse
from typing import Dict, Any


def query_api_endpoint(url: str, payload: Dict[str, Any], api_key: str = None) -> Dict[str, Any]:
    """Sends JSON request payload to private Invariant SAT API server."""
    data_bytes = json.dumps(payload).encode('utf-8')
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "InvariantSAT-ZeroIP-Client/2.0"
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res_body = response.read().decode('utf-8')
            res_json = json.loads(res_body)
            res_json["client_latency_ms"] = round((time.time() - t0) * 1000, 2)
            return res_json
    except Exception as e:
        return {
            "status": "ERROR",
            "error": f"Failed to reach Invariant SAT API server: {str(e)}",
            "url": url
        }


def format_markdown_pr_comment(report: Dict[str, Any], target_file: str = "Circuit") -> str:
    """Formats verification findings into GitHub PR Markdown."""
    verdict = report.get("verdict_label", report.get("status", "COMPLETED"))
    status_icon = "❌" if "BUG" in verdict or "FAILED" in verdict else "✅"
    
    md = []
    md.append(f"## {status_icon} Invariant SAT ZK Security Scan — `{target_file}`")
    md.append("")
    md.append(f"| Metric | Value |")
    md.append(f"| :--- | :--- |")
    md.append(f"| **Verdict** | `{verdict}` |")
    if "num_variables" in report:
        md.append(f"| **Circuit Signals (N)** | `{report.get('num_variables', 0):,}` |")
    if "num_constraints" in report:
        md.append(f"| **Constraints (M)** | `{report.get('num_constraints', 0):,}` |")
    if "under_constrained_count" in report:
        md.append(f"| **Under-Constrained Signals** | `{report.get('under_constrained_count', 0)}` |")
    if "solve_time_ms" in report:
        md.append(f"| **Proof Execution Time** | `{report.get('solve_time_ms')} ms` |")
    if "certificate_hash" in report:
        md.append(f"| **Proof Certificate** | `{report.get('certificate_hash')}` |")

    md.append("")

    if report.get("under_constrained_count", 0) > 0:
        md.append("### ⚠️ Under-Constrained Signal Vulnerabilities Detected")
        md.append("The circuit contains signals without sufficient algebraic constraint bounds. This may allow malicious provers to forge zero-knowledge proofs under identical public inputs.")
        md.append("")

    if report.get("exploit_vector"):
        exp = report["exploit_vector"]
        md.append("#### 🚨 Concrete Counterexample Exploit Witness Pair:")
        md.append("```json")
        md.append(json.dumps(exp, indent=2))
        md.append("```")
        md.append("")

    md.append("---")
    md.append("*Scanned automatically by [Invariant SAT Zero-IP Enclave](https://invariantsat.com)*")
    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="Invariant SAT Zero-IP API & GitHub Action CLI Client")
    parser.add_argument("--api-url", type=str, default="http://localhost:8080", help="Base URL of private Invariant SAT API server")
    parser.add_argument("--api-key", type=str, help="Optional SaaS API auth key")
    parser.add_argument("--r1cs", type=str, help="Path to ZK R1CS circuit file")
    parser.add_argument("--cnf", type=str, help="Path to Hardware CNF miter file")
    parser.add_argument("--zk-demo", action="store_true", help="Run ZK circuit verification check")
    parser.add_argument("--markdown", type=str, help="File path to write GitHub PR Markdown comment output")
    parser.add_argument("--json", type=str, help="File path to write JSON report output")
    parser.add_argument("--quiet", action="store_true", help="Suppress console stdout output")

    args = parser.parse_args()

    base_url = args.api_url.rstrip('/')

    if args.r1cs or args.zk_demo:
        endpoint = f"{base_url}/api/v1/verify_zk"
        payload = {"num_signals": 100, "is_buggy": True}
        target_name = os.path.basename(args.r1cs) if args.r1cs else "ZK Circuit Demo"
        if args.r1cs and os.path.exists(args.r1cs):
            with open(args.r1cs, "r", encoding="utf-8", errors="ignore") as f:
                payload["circuit_content"] = f.read()

        report = query_api_endpoint(endpoint, payload, api_key=args.api_key)

    elif args.cnf:
        endpoint = f"{base_url}/api/v1/verify"
        target_name = os.path.basename(args.cnf)
        payload = {}
        if os.path.exists(args.cnf):
            with open(args.cnf, "r", encoding="utf-8", errors="ignore") as f:
                payload["cnf_content"] = f.read()
        report = query_api_endpoint(endpoint, payload, api_key=args.api_key)
    else:
        # Default health check query
        endpoint = f"{base_url}/health"
        req = urllib.request.Request(endpoint)
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                report = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            report = {"status": "ERROR", "error": str(e)}
        target_name = "Health Check"

    if not args.quiet:
        print(json.dumps(report, indent=2))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        if not args.quiet:
            print(f"[+] JSON report saved to: {args.json}")

    if args.markdown:
        md_text = format_markdown_pr_comment(report, target_file=target_name)
        with open(args.markdown, "w", encoding="utf-8") as f:
            f.write(md_text)
        if not args.quiet:
            print(f"[+] GitHub PR Markdown comment saved to: {args.markdown}")


if __name__ == "__main__":
    main()
