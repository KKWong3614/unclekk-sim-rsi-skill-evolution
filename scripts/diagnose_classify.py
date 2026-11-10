#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline bottleneck classifier for skill-evolution diagnosis (ASSISTIVE only).

This is the "轨道 A 分类诊断器" referenced in SKILL.md \u00a72, shipped as a runnable
helper. It reads failure traces and groups each into one of six bottleneck
buckets (guard / consistency / model-budget / capability / brittleness /
compression). It ONLY produces SUGGESTIONS — it never auto-selects a workflow,
never edits a verdict, and never writes back. A human must confirm the next step.

Input: JSON file with {"traces":[{id,stage,message}]} or a bare list of
{"id","message"} objects. Keyword-based, deterministic, stdlib only.

Exit codes: 0 = all traces classified; 1 = some traces unclassified; 2 = bad input.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

BUCKETS = {
    "guard": {
        "keywords": [r"guard", r"permission", r"权限", r"access", r"token", r"auth", r"守卫", r"授权"],
        "advice": "检查守卫/权限/凭证链路；确认 SHEGuard 账户与 ACL 是否完整（详见 references/four-stage-status.md）。",
    },
    "consistency": {
        "keywords": [r"hash", r"哈希", r"mismatch", r"checksum", r"integrity", r"一致性", r"完整", r"漂移"],
        "advice": "跑冻结任务集哈希锁，确认无未授权改动；用 freeze_snapshot.py 重新登记基线。",
    },
    "model_budget": {
        "keywords": [r"budget", r"预算", r"max_metric_calls", r"quota", r"rate limit", r"限流", r"timeout", r"超时", r"token limit", r"额度"],
        "advice": "检查 GEPA 预算硬停（max_metric_calls）；拆分任务或降低反思轮次，不要为过闸而改判据。",
    },
    "capability": {
        "keywords": [r"capability", r"能力", r"cannot", r"不支持", r"not implemented", r"未实现", r"unsupported", r"做不到"],
        "advice": "确认是否超出当前方法论内核范围；属 T1/T2 后续课题的，登记为「下一步」而非当前能力。",
    },
    "brittleness": {
        "keywords": [r"brittle", r"flaky", r"脆", r"随机", r"non-deterministic", r"非确定", r"order", r"顺序", r"偶发"],
        "advice": "固定随机种子/排序，隔离非确定性来源；回归门禁要求输出逐字节稳定。",
    },
    "compression": {
        "keywords": [r"compress", r"压缩", r"truncate", r"截断", r"too long", r"过长", r"length", r"长度", r"size", r"体积"],
        "advice": "精简 SKILL.md 时保留要点、细节下沉 references；用文档地图降低主文档篇幅。",
    },
}


def classify(message: str) -> str | None:
    low = (message or "").lower()
    for name, spec in BUCKETS.items():
        for kw in spec["keywords"]:
            if re.search(kw, low, re.IGNORECASE):
                return name
    return None


def run_classify(traces: list[dict]) -> tuple[dict, list]:
    grouped: dict[str, list] = {k: [] for k in BUCKETS}
    grouped["unclassified"] = []
    unclassified = []
    for t in traces:
        if not isinstance(t, dict):
            continue
        tid = str(t.get("id", "?"))
        msg = str(t.get("message", ""))
        bucket = classify(msg)
        if bucket is None:
            grouped["unclassified"].append(tid)
            unclassified.append(tid)
        else:
            grouped[bucket].append(tid)
    return grouped, unclassified


def _render(grouped: dict, human: bool) -> list[str]:
    lines = []
    total = sum(len(v) for k, v in grouped.items() if k != "unclassified")
    uncl = grouped.get("unclassified", [])
    if human:
        lines.append(f"DIAGNOSE: {total} classified, {len(uncl)} unclassified")
        for name, spec in BUCKETS.items():
            ids = grouped.get(name, [])
            lines.append(f"[{name}] {len(ids)}: {', '.join(ids) if ids else '(none)'}")
            if ids:
                lines.append(f"    advice: {spec['advice']}")
        if uncl:
            lines.append(f"[unclassified] {len(uncl)}: {', '.join(uncl)} -> 人工补充分类关键词")
    return lines


def self_test() -> int:
    traces = [
        {"id": "T01", "message": "guard permission denied for SHEGuard account"},
        {"id": "T02", "message": "frozen task set hash mismatch detected"},
        {"id": "T03", "message": "GEPA exceeded max_metric_calls budget"},
        {"id": "T04", "message": "capability not implemented for this workflow"},
        {"id": "T05", "message": "flaky non-deterministic output order"},
        {"id": "T06", "message": "SKILL.md truncated, too long to fit"},
        {"id": "T07", "message": "mysterious failure with no known keyword"},
    ]
    grouped, uncl = run_classify(traces)
    checks = [
        ("guard", "T01" in grouped["guard"]),
        ("consistency", "T02" in grouped["consistency"]),
        ("model_budget", "T03" in grouped["model_budget"]),
        ("capability", "T04" in grouped["capability"]),
        ("brittleness", "T05" in grouped["brittleness"]),
        ("compression", "T06" in grouped["compression"]),
        ("unclassified", "T07" in grouped["unclassified"]),
    ]
    ok = all(v for _, v in checks)
    for name, cond in checks:
        print(f"[{'PASS' if cond else 'FAIL'}] classify {name}")
    print(f"SELFTEST: {sum(1 for _,v in checks if v)}/{len(checks)} PASS")
    return 0 if ok else 3


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description="Offline bottleneck classifier (assistive, zero dependencies).")
    ap.add_argument("--input", help="JSON file: {\"traces\":[{id,message}]} or a list")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in cases")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    if not args.input:
        print("error: provide --input <json> (or --self-test)", file=sys.stderr)
        return 2
    path = Path(args.input)
    if not path.is_file():
        print(f"[ERROR] missing file: {path}", file=sys.stderr)
        return 2
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[ERROR] invalid JSON: {exc.msg}", file=sys.stderr)
        return 2
    traces = doc.get("traces") if isinstance(doc, dict) else doc
    if not isinstance(traces, list):
        print("[ERROR] input must be a list or {\"traces\":[...]}", file=sys.stderr)
        return 2

    grouped, uncl = run_classify(traces)
    if args.json:
        print(json.dumps({"grouped": grouped}, ensure_ascii=False, indent=2))
    else:
        for line in _render(grouped, human=True):
            print(line)
    return 1 if uncl else 0


if __name__ == "__main__":
    raise SystemExit(main())
