#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Frozen-task regression gate: a minimal, runnable reference implementation.

IMPORTANT (keep this notice with any output you quote):
- This is a teaching/reference-grade minimal loop. It is NOT a copy of any
  production harness: there is no hidden probe pool, no integrity ledger,
  no OS-level isolation, no LLM call and no external dependency.
- PASS means "frozen baselines did not regress". It does NOT mean the skill
  became more capable, does NOT mean semantic quality is acceptable, and is
  NOT evidence for RSI or for an automatic four-stage RSIFlow loop.

Exit codes: 0 = all passed; 1 = regression / prohibited item; 2 = bad input
or frozen-suite integrity error; 3 = self-test failed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

NOTICE = (
    "NOTICE: PASS = frozen baselines did not regress, NOT capability gain; "
    "not evidence of RSI or an automatic RSIFlow four-stage loop."
)
BAD_STATUSES = {"unavailable", "error", "skipped", "blocked", "unknown"}
DEFAULT_FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _canonical(obj: object) -> bytes:
    return json.dumps(
        obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")


def _sha256(obj: object) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()


def _load_json(path: Path) -> object:
    if not path.is_file():
        raise FileNotFoundError(f"missing file: {path.name}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.name}: {exc.msg}") from exc


def run_gate(fixtures: Path) -> tuple[int, list[str]]:
    """Return (exit_code, deterministic_output_lines). Never raises on bad input."""
    lines: list[str] = []
    try:
        tasks_doc = _load_json(fixtures / "tasks.json")
        results_doc = _load_json(fixtures / "results.json")
        manifest = _load_json(fixtures / "manifest.json")
    except (FileNotFoundError, ValueError, OSError) as exc:
        lines.append(f"[ERROR] input problem: {exc}")
        lines.append("[FIX] check the --fixtures directory, file names and JSON syntax.")
        lines.append("[FIX] expected: tasks.json, results.json, manifest.json")
        return 2, lines

    # 1) Frozen-suite integrity lock: never judge a suite that was edited.
    expected_hash = ""
    if isinstance(manifest, dict):
        expected_hash = str(manifest.get("tasks_sha256", ""))
    actual_hash = _sha256(tasks_doc)
    if not expected_hash or expected_hash != actual_hash:
        lines.append("[ERROR] frozen task set hash mismatch (EXIT=2, fail-closed).")
        lines.append(f"  manifest.tasks_sha256 = {expected_hash or '<empty>'}")
        lines.append(f"  recomputed            = {actual_hash}")
        lines.append("[FIX] restore tasks.json, or go through an authorized baseline change.")
        lines.append("[FIX] never edit manifest.json just to make the gate green.")
        return 2, lines

    # 2) Structure validation.
    tasks = tasks_doc.get("tasks") if isinstance(tasks_doc, dict) else None
    results = results_doc.get("results") if isinstance(results_doc, dict) else None
    if not isinstance(tasks, list) or not tasks:
        lines.append("[ERROR] tasks.json must contain a non-empty 'tasks' list.")
        return 2, lines
    if not isinstance(results, list):
        lines.append("[ERROR] results.json must contain a 'results' list.")
        return 2, lines
    task_ids = [str(t.get("id", "")) for t in tasks if isinstance(t, dict)]
    if any(not i for i in task_ids) or len(set(task_ids)) != len(tasks):
        lines.append("[ERROR] every task needs a unique non-empty 'id'.")
        return 2, lines

    suite_a = str(tasks_doc.get("suite", ""))
    suite_b = str(results_doc.get("suite", ""))
    if suite_a and suite_b and suite_a != suite_b:
        lines.append(f"[ERROR] suite mismatch: tasks='{suite_a}' results='{suite_b}'.")
        lines.append("[FIX] run the gate against the matching frozen suite.")
        return 2, lines

    # 3) Prohibited items (anti-whitewash), checked before any PASS is emitted.
    prohibited: list[str] = []
    if isinstance(results_doc, dict) and results_doc.get("bulk_approve") is True:
        prohibited.append("bulk_approve=true is forbidden: no bulk unconditional approval.")
    for r in results:
        if not isinstance(r, dict):
            continue
        status = str(r.get("status", "")).strip().lower()
        if status in BAD_STATUSES and r.get("pass") is True:
            prohibited.append(
                f"{r.get('id', '?')}: status='{status}' marked pass=true; "
                "relabelling unavailable as validated to pass a gate is forbidden."
            )
    if prohibited:
        lines.append("[PROHIBITED] whitewash attempt blocked (EXIT=1).")
        for msg in sorted(prohibited):
            lines.append(f"  - {msg}")
        lines.append("[FIX] fix the underlying failure; do not edit the verdict.")

    # 4) Coverage: a partial run can never be reported as N/N.
    result_ids = [str(r.get("id", "")) for r in results if isinstance(r, dict)]
    missing = sorted(set(task_ids) - set(result_ids))
    extra = sorted(set(result_ids) - set(task_ids))
    duplicate = len(result_ids) != len(set(result_ids))
    coverage_ok = not (missing or extra or duplicate)

    by_id = {str(r.get("id", "")): r for r in results if isinstance(r, dict)}
    passed = 0
    for tid in sorted(task_ids):
        r = by_id.get(tid)
        if r is None:
            lines.append(f"[FAIL] {tid}: no result (coverage gap)")
            continue
        ok = r.get("pass") is True
        reason = str(r.get("reason", "")).strip()
        if ok:
            passed += 1
            lines.append(f"[PASS] {tid}")
        else:
            lines.append(f"[FAIL] {tid}: {reason or 'result.pass is not true'}")

    total = len(task_ids)
    if not coverage_ok:
        lines.append("[COVERAGE] suite coverage is incomplete; N/N is not reportable.")
        if missing:
            lines.append(f"  missing results: {', '.join(missing)}")
        if extra:
            lines.append(f"  unknown results: {', '.join(extra)}")
        if duplicate:
            lines.append("  duplicate result ids found")

    all_good = (
        not prohibited
        and coverage_ok
        and passed == total
        and len(results) == total
    )
    lines.append(f"SUMMARY: {passed}/{total} passed | exit={'0' if all_good else '1'}")
    lines.append(NOTICE)
    return (0 if all_good else 1), lines


def _write_fixture(root: Path, tasks: object, results: object, hash_override: str = "") -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "tasks.json").write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (root / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    manifest = {
        "suite": "selftest-suite",
        "tasks_sha256": hash_override or _sha256(tasks),
        "notice": "frozen baseline; any edit requires an authorized change chain",
    }
    (root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def self_test() -> int:
    """Six deterministic cases: one positive, five negative. No workspace writes."""
    tasks = {
        "suite": "selftest-suite",
        "version": "1.0.3",
        "tasks": [
            {"id": "T01", "name": "guard", "expected": "pass"},
            {"id": "T02", "name": "consistency", "expected": "pass"},
        ],
    }
    good = {
        "suite": "selftest-suite",
        "results": [
            {"id": "T01", "pass": True, "status": "validated", "reason": ""},
            {"id": "T02", "pass": True, "status": "validated", "reason": ""},
        ],
    }

    def case(name: str, t: object, r: object, override: str, want_code: int, want_text: str) -> bool:
        with tempfile.TemporaryDirectory(prefix="gate_min_selftest_") as tmp:
            _write_fixture(Path(tmp), t, r, override)
            code, out = run_gate(Path(tmp))
        text = "\n".join(out)
        ok = code == want_code and want_text in text
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: exit={code} want={want_code}")
        if not ok:
            print(text)
        return ok

    checks = [
        case("S1 clean run", tasks, good, "", 0, "SUMMARY: 2/2 passed"),
        case("S2 real regression", tasks, {
            "suite": "selftest-suite",
            "results": [
                {"id": "T01", "pass": True, "status": "validated", "reason": ""},
                {"id": "T02", "pass": False, "status": "failed", "reason": "baseline changed"},
            ],
        }, "", 1, "[FAIL] T02"),
        case("S3 edited frozen suite", tasks, good, "0" * 64, 2, "hash mismatch"),
        case("S4 partial coverage", tasks, {
            "suite": "selftest-suite",
            "results": [{"id": "T01", "pass": True, "status": "validated"}],
        }, "", 1, "coverage is incomplete"),
        case("S5 unavailable relabelled", tasks, {
            "suite": "selftest-suite",
            "results": [
                {"id": "T01", "pass": True, "status": "unavailable", "reason": ""},
                {"id": "T02", "pass": True, "status": "validated", "reason": ""},
            ],
        }, "", 1, "relabelling unavailable"),
        case("S6 bulk approval", tasks, {
            "suite": "selftest-suite",
            "bulk_approve": True,
            "results": [
                {"id": "T01", "pass": True, "status": "validated", "reason": ""},
                {"id": "T02", "pass": True, "status": "validated", "reason": ""},
            ],
        }, "", 1, "bulk unconditional approval"),
    ]
    ok_count = sum(1 for c in checks if c)
    print(f"SELFTEST: {ok_count}/{len(checks)} PASS")
    print(NOTICE)
    return 0 if ok_count == len(checks) else 3


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(
        description="Minimal frozen-task regression gate (zero third-party dependencies)."
    )
    ap.add_argument("--fixtures", default=str(DEFAULT_FIXTURES), help="fixtures directory")
    ap.add_argument("--json", action="store_true", help="emit deterministic JSON")
    ap.add_argument("--self-test", action="store_true", help="run 6 built-in cases")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    code, lines = run_gate(Path(args.fixtures))
    if args.json:
        print(json.dumps(
            {"exit": code, "lines": lines},
            ensure_ascii=False, indent=2,
        ))
    else:
        for line in lines:
            print(line)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
