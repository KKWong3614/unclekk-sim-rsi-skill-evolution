#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare two result sets and report regressions / improvements (ASSISTIVE).

This is the "batch compare" helper referenced by the TRACE review as missing.
It takes a BEFORE and AFTER result set and shows, per task id: regressed
(True->False), improved (False->True), stable, new (only in AFTER), removed
(only in BEFORE). It NEVER judges quality and NEVER edits anything — it only
reports what changed between two frozen snapshots.

Input: each file is {"results":[{id,pass,...}]} or a bare list of {id,pass}.
Stdlib only. Output is deterministic.

Exit codes: 0 = ok (always; this is a reporter, not a gate).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_results(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"missing file: {path}")
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.name}: {exc.msg}") from exc
    results = doc.get("results") if isinstance(doc, dict) else doc
    if not isinstance(results, list):
        raise ValueError(f"{path.name} must contain a 'results' list")
    out = {}
    for r in results:
        if not isinstance(r, dict):
            continue
        rid = str(r.get("id", ""))
        if rid:
            out[rid] = bool(r.get("pass") is True)
    return out


def diff(before: dict, after: dict) -> dict:
    ids = sorted(set(before) | set(after))
    regressed, improved, stable, new, removed = [], [], [], [], []
    for i in ids:
        b = before.get(i)
        a = after.get(i)
        if b is None and a is not None:
            new.append(i)
        elif b is not None and a is None:
            removed.append(i)
        elif b is True and a is False:
            regressed.append(i)
        elif b is False and a is True:
            improved.append(i)
        else:
            stable.append(i)
    return {
        "regressed": regressed, "improved": improved, "stable": stable,
        "new": new, "removed": removed,
    }


def self_test() -> int:
    before = {"T01": True, "T02": True, "T03": False, "T04": True}
    after = {"T01": True, "T02": False, "T03": True, "T05": True}
    d = diff(before, after)
    checks = [
        ("regressed", d["regressed"] == ["T02"]),
        ("improved", d["improved"] == ["T03"]),
        ("stable", d["stable"] == ["T01"]),
        ("new", d["new"] == ["T05"]),
        ("removed", d["removed"] == ["T04"]),
    ]
    ok = all(v for _, v in checks)
    for name, cond in checks:
        print(f"[{'PASS' if cond else 'FAIL'}] {name}: {d[name]}")
    print(f"SELFTEST: {sum(1 for _,v in checks if v)}/{len(checks)} PASS")
    return 0 if ok else 3


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description="Compare two result sets (assistive, zero dependencies).")
    ap.add_argument("--before", required=True, help="BEFORE results JSON")
    ap.add_argument("--after", required=True, help="AFTER results JSON")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in cases")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    try:
        before = _load_results(Path(args.before))
        after = _load_results(Path(args.after))
    except (FileNotFoundError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    d = diff(before, after)
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
    else:
        print(f"REGRESSED ({len(d['regressed'])}): {', '.join(d['regressed']) or 'none'}")
        print(f"IMPROVED  ({len(d['improved'])}): {', '.join(d['improved']) or 'none'}")
        print(f"STABLE    ({len(d['stable'])}): {', '.join(d['stable']) or 'none'}")
        print(f"NEW       ({len(d['new'])}): {', '.join(d['new']) or 'none'}")
        print(f"REMOVED   ({len(d['removed'])}): {', '.join(d['removed']) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
