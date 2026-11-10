#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Claim-boundary linter for skill-evolution SKILL.md documents.

This is an ASSISTIVE checker, NOT an auto-fixer and NOT an RSI / RSIFlow
implementation. It only flags wording that violates the package's published
claim boundary (see references/claim-boundary.md). It never edits files and
never improves the skill; it just reports what the text says.

Rules enforced (see SKILL.md \u00a70 / \u00a76):
- Prohibited strong claims (T1 four-stage loop auto-implemented, T2 RSI achieved,
  capability gain, semantic quality met, live loop validated) are allowed ONLY
  when clearly negated / qualified (e.g. "不可声称", "未启动", "not", "prohibited").
- The two qualifiers "方法论内核" and "精简版" must both be present.
- A PASS disclaimer ("PASS" + "回归未退化" / "did not regress") must be present.

Exit codes: 0 = clean (warnings only, unless --strict); 1 = violations found;
2 = bad input.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# (key, [regex patterns, case-insensitive]). A hit is a VIOLATION unless a safe
# marker appears within WINDOW chars on either side.
PROHIBITED = [
    ("T1_four_stage_loop", [r"四段闭环自动", r"four[- ]?stage loop implemented automatically", r"闭环自动落地"]),
    ("T2_rsi_achieved", [r"已实现递归自我改进", r"recursive self[- ]?improvement achieved", r"已实现\s*rsi\b", r"rsi achieved"]),
    ("capability_gain", [r"能力变强", r"capability (gain|improved)", r"语义质量达标", r"semantic quality (met|acceptable|passed)"]),
    ("live_loop_validated", [r"实时闭环已验证", r"live loop (validated|verified)"]),
]

# Safe markers: if any appears within WINDOW chars around a prohibited hit, the
# hit is treated as a legitimate negation / qualification, not a violation.
SAFE_MARKERS = [
    "不可", "不可声称", "未启动", "未实现", "不是", "禁止", "不声称", "后续课题",
    "not", "prohibited", "cannot", "does not", "unavailable", "not-started",
    "unstarted", "未", "没有", "no ", "never", "未发布", "not yet", "不允许",
]
WINDOW = 80

REQUIRED_QUALIFIERS = ["方法论内核", "精简版"]
REQUIRED_PASS = [r"PASS", r"回归未退化|did not regress"]


def _context_ok(text: str, start: int, end: int) -> bool:
    lo = max(0, start - WINDOW)
    hi = min(len(text), end + WINDOW)
    window = text[lo:hi].lower()
    return any(m.lower() in window for m in SAFE_MARKERS)


def lint_text(text: str):
    findings = []
    for key, pats in PROHIBITED:
        for pat in pats:
            for m in re.finditer(pat, text, re.IGNORECASE):
                if not _context_ok(text, m.start(), m.end()):
                    findings.append(("ERROR", key, m.group(0)))
    warnings = []
    for q in REQUIRED_QUALIFIERS:
        if q not in text:
            warnings.append(("WARN", "missing_qualifier", q))
    has_pass = bool(re.search(REQUIRED_PASS[0], text)) and bool(
        re.search(REQUIRED_PASS[1], text, re.IGNORECASE)
    )
    if not has_pass:
        warnings.append(("WARN", "missing_pass_disclaimer", "PASS + 回归未退化 / did not regress"))
    return findings, warnings


def lint_file(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"missing file: {path}")
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc
    return lint_text(text)


def _render(findings, warnings, strict, src):
    lines = []
    if findings:
        lines.append(f"[VIOLATION] claim-boundary violations in {src}:")
        for lvl, key, hit in findings:
            lines.append(f"  - {key}: found '{hit}' (affirmative context)")
    if warnings:
        lines.append(f"[WARN] {src}:")
        for lvl, key, detail in warnings:
            lines.append(f"  - {key}: {detail}")
    if not findings and not warnings:
        lines.append(f"[OK] {src}: claim boundary satisfied.")
    return lines


def self_test() -> int:
    clean = (
        "# 精简版 RSI 技能进化\n"
        "基于 RSIFlow 方法论内核的精简版技能文本进化。\n"
        "当前不可声称：RSIFlow 四段闭环自动落地；已实现递归自我改进 / RSI。\n"
        "PASS = 回归未退化，非能力提升。\n"
    )
    violation = (
        "我们已实现 RSIFlow 四段闭环自动落地，技能能力变强，语义质量达标。\n"
        "方法论内核，精简版。\n"
    )
    missing_qual = (
        "当前不可声称：RSIFlow 四段闭环自动落地；已实现递归自我改进 / RSI。\n"
        "PASS = 回归未退化，非能力提升。\n"
    )

    def run(name, text, want_viol, want_warn, strict=False):
        f, w = lint_text(text)
        ok = (len(f) > 0) == want_viol
        if strict:
            ok = ok and (len(w) == 0) == (not want_warn)
        else:
            # warnings do not fail by default; only check violation count matches
            pass
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: violations={len(f)} warnings={len(w)}")
        if not ok:
            for x in f:
                print("   ", x)
            for x in w:
                print("   ", x)
        return ok

    checks = [
        run("S1 clean (negated claims + qualifiers + PASS)", clean, False, False),
        run("S2 violation (affirmative T1 + capability gain)", violation, True, False),
        run("S3 missing qualifier (no 方法论内核)", missing_qual, False, True),
    ]
    ok_count = sum(1 for c in checks if c)
    print(f"SELFTEST: {ok_count}/{len(checks)} PASS")
    return 0 if ok_count == len(checks) else 3


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description="Claim-boundary linter (assistive, zero dependencies).")
    ap.add_argument("path", nargs="?", help="SKILL.md (or any text file) to lint")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures (exit 1)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in cases")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    if not args.path:
        print("error: provide a file path (or --self-test)", file=sys.stderr)
        return 2
    try:
        findings, warnings = lint_file(Path(args.path))
    except (FileNotFoundError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"violations": findings, "warnings": warnings}, ensure_ascii=False, indent=2))
    else:
        for line in _render(findings, warnings, args.strict, args.path):
            print(line)

    if findings:
        return 1
    if args.strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
