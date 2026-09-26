"""
AutoHeal Validation Hub
========================
This script is the core orchestrator of the IBM Bob AutoHeal workflow.

It performs the following steps:
  1. Runs the full pytest test suite against the current app.py
  2. Generates a code coverage report (XML + terminal)
  3. Parses and displays a structured failure report
  4. Signals whether the AutoHeal agent needs to intervene

Usage:
    python scripts/run_validation.py [--healed]

Flags:
    --healed   Run tests against app_healed.py instead of app.py (to verify fixes)
"""

import subprocess
import sys
import os
import argparse
import json
from pathlib import Path


def run_tests(api_dir: Path, target: str = "buggy") -> dict:
    """Run the pytest suite and return structured results."""
    env = os.environ.copy()

    # If testing healed version, swap the import temporarily
    if target == "healed":
        # Rename trick: point tests to healed app
        env["AUTOHEAL_TARGET"] = "healed"
        extra_args = ["--override-ini=python_files=test_healed.py"]
    else:
        extra_args = []

    result = subprocess.run(
        [
            sys.executable, "-m", "pytest", "tests/",
            "-v",
            "--tb=short",
            "--cov=.",
            "--cov-config=.coveragerc",
            "--cov-report=xml",
            "--cov-report=term-missing",
            "-q",
        ] + extra_args,
        cwd=api_dir,
        capture_output=True,
        text=True,
        env=env,
    )
    # Parse summary line like: "3 failed, 5 passed, 1 warning in 6.37s"
    passed = 0
    failed = 0
    errors = 0
    import re
    for line in result.stdout.splitlines():
        if " passed" in line or " failed" in line or " error" in line:
            m = re.search(r"(\d+) failed", line)
            if m:
                failed = int(m.group(1))
            m = re.search(r"(\d+) passed", line)
            if m:
                passed = int(m.group(1))
            m = re.search(r"(\d+) error", line)
            if m:
                errors = int(m.group(1))

    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "passed": passed,
        "failed": failed,
        "errors": errors,
    }


def print_section(title: str, char: str = "=", width: int = 70):
    print(f"\n{char * width}")
    print(f"  {title}")
    print(f"{char * width}")


def main():
    parser = argparse.ArgumentParser(description="AutoHeal Validation Hub")
    parser.add_argument("--healed", action="store_true", help="Test against healed app")
    args = parser.parse_args()

    api_dir = Path(__file__).parent.parent / "demo_ecommerce_api"

    print_section("IBM Bob AutoHeal — Validation Hub")
    print(f"  Target : {'HEALED' if args.healed else 'BUGGY (original)'} version")
    print(f"  Suite  : {api_dir / 'tests'}")
    print(f"  Coverage threshold: 80%")

    print_section("Running Test Suite...", char="-")
    results = run_tests(api_dir, target="healed" if args.healed else "buggy")

    print(results["stdout"])
    if results["stderr"]:
        print(results["stderr"], file=sys.stderr)

    print_section("AutoHeal Summary", char="=")
    total = results["passed"] + results["failed"] + results["errors"]
    print(f"  Total Tests  : {total}")
    print(f"  Passed       : {results['passed']}")
    print(f"  Failed       : {results['failed']}")
    print(f"  Errors       : {results['errors']}")

    if results["returncode"] == 0:
        print("\n  [PASS] All tests passed! Application is healthy.")
        print("  No action required from the AutoHeal Agent.")
    else:
        print(f"\n  [FAIL] {results['failed']} test(s) failed!")
        print()
        print("  ACTION REQUIRED:")
        print("  Load 'bob_skills/AutoHealer_Skill.md' in IBM Bob IDE.")
        print("  Run: 'Heal the application using the AutoHeal workflow'")
        print()
        print("  The Bob Agent will:")
        print("    1. Spawn a Research Subagent to analyse the stack traces above")
        print("    2. Spawn parallel Coder Subagents to fix each bug simultaneously")
        print("    3. Re-run this script to verify all tests pass")
        sys.exit(1)


if __name__ == "__main__":
    main()
