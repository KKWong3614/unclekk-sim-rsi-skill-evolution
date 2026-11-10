#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run every script's built-in self-test in this package (ASSISTIVE harness).

Imports each sibling module and calls its self_test(); exits non-zero if any
fails. This is the "expand test coverage" item from the TRACE review. Stdlib
only, no network, no side effects beyond console output.

Exit codes: 0 = all self-tests pass; 1 = at least one self-test failed.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

MODULES = [
    "gate_min",
    "claim_lint",
    "freeze_snapshot",
    "diagnose_classify",
    "coverage_diff",
]


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    print("=== test_all: running built-in self-tests ===")
    all_ok = True
    for name in MODULES:
        try:
            mod = importlib.import_module(name)
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] import {name}: {exc}")
            all_ok = False
            continue
        if not hasattr(mod, "self_test"):
            print(f"[SKIP] {name}: no self_test()")
            continue
        try:
            rc = mod.self_test()
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] {name}.self_test raised: {exc}")
            all_ok = False
            continue
        status = "PASS" if rc == 0 else "FAIL"
        if rc != 0:
            all_ok = False
        print(f"[{status}] {name}.self_test -> exit={rc}")
    print("===========================================")
    print(f"ALL: {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
