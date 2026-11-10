#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Snapshot a frozen task set: compute its SHA-256 lock and write manifest.json.

This is an ASSISTIVE tool, NOT a gate and NOT an RSI / RSIFlow implementation.
It only records the hash that `gate_min.py` later checks, so a frozen baseline
cannot be silently edited. It never runs the gate and never edits task content.

To change the frozen set, edit tasks.json through an authorized change chain
(human review + recorded from->to + recomputed hash), then re-run this snapshot.

Exit codes: 0 = ok; 2 = bad input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

NOTICE = "frozen baseline; any edit requires an authorized change chain and a recomputed hash"

DEFAULT_OUT_NAME = "manifest.json"


def _canonical(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def _sha256(obj: object) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()


def snapshot(tasks_path: Path, out_path: Path) -> str:
    if not tasks_path.is_file():
        raise FileNotFoundError(f"missing tasks file: {tasks_path}")
    try:
        tasks = json.loads(tasks_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {tasks_path.name}: {exc.msg}") from exc
    if not isinstance(tasks, dict) or not tasks.get("tasks"):
        raise ValueError(f"{tasks_path.name} must contain a non-empty 'tasks' list")
    digest = _sha256(tasks)
    manifest = {
        "suite": str(tasks.get("suite", "")),
        "tasks_sha256": digest,
        "notice": NOTICE,
    }
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return digest


def self_test() -> int:
    sample = {
        "suite": "selftest-suite",
        "version": "1.0.3",
        "tasks": [
            {"id": "T01", "name": "guard", "expected": "pass"},
            {"id": "T02", "name": "consistency", "expected": "pass"},
        ],
    }
    ok = True

    def check(name, cond):
        nonlocal ok
        ok = ok and cond
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")

    with tempfile.TemporaryDirectory(prefix="freeze_selftest_") as tmp:
        root = Path(tmp)
        tasks_file = root / "tasks.json"
        tasks_file.write_text(json.dumps(sample, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest_file = root / DEFAULT_OUT_NAME

        digest1 = snapshot(tasks_file, manifest_file)
        check("S1 manifest written", manifest_file.is_file())
        loaded = json.loads(manifest_file.read_text(encoding="utf-8"))
        check("S2 hash matches _sha256(tasks)", loaded.get("tasks_sha256") == digest1)
        check("S3 deterministic recompute", _sha256(sample) == digest1)

        # changing content changes the hash
        mutated = json.loads(json.dumps(sample))
        mutated["tasks"].append({"id": "T03", "name": "extra", "expected": "pass"})
        check("S4 content change alters hash", _sha256(mutated) != digest1)

    print(f"SELFTEST: {'1/1' if ok else '0/1'} PASS")
    return 0 if ok else 3


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description="Freeze a task set: write its SHA-256 lock (assistive).")
    ap.add_argument("--tasks", required=True, help="path to tasks.json")
    ap.add_argument("--out", default=None, help=f"output manifest (default: <tasks dir>/{DEFAULT_OUT_NAME})")
    ap.add_argument("--self-test", action="store_true", help="run built-in cases")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    tasks_path = Path(args.tasks)
    out_path = Path(args.out) if args.out else tasks_path.parent / DEFAULT_OUT_NAME
    try:
        digest = snapshot(tasks_path, out_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2
    print(f"[OK] wrote {out_path}")
    print(f"     tasks_sha256 = {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
