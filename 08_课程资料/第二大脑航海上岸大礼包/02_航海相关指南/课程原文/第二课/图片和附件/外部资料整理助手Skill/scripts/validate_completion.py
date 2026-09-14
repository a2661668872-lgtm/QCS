#!/usr/bin/env python3
"""Validate whether a knowledge-base workflow may claim a completion status."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


STATUS_REQUIREMENTS = {
    "round_processing_completed": {
        "purpose", "blueprint", "structure_initialization", "inventory", "ledger", "source_summaries",
    },
    "knowledge_base_initialized": {
        "purpose", "blueprint", "structure_initialization", "inventory", "ledger", "source_summaries",
        "atomic_materials", "source_relations", "retrieval_validation",
        "coverage_report",
    },
    "application_partially_validated": {
        "purpose", "blueprint", "structure_initialization", "inventory", "ledger", "source_summaries",
        "atomic_materials", "source_relations", "retrieval_validation",
        "application_validation", "coverage_report",
    },
    "application_validated": {
        "purpose", "blueprint", "structure_initialization", "inventory", "ledger", "source_summaries",
        "atomic_materials", "source_relations", "retrieval_validation",
        "application_validation", "coverage_report",
    },
    "formally_delivered": {
        "purpose", "blueprint", "structure_initialization", "inventory", "ledger", "source_summaries",
        "atomic_materials", "source_relations", "retrieval_validation",
        "application_validation", "coverage_report", "user_confirmation",
    },
}


def artifact_exists(root: Path, value: str) -> bool:
    if not value:
        return False
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    if not path.exists():
        return False
    if path.is_file():
        return path.stat().st_size > 0
    return any(item.is_file() and item.stat().st_size > 0 for item in path.rglob("*"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", help="Completion manifest JSON")
    parser.add_argument("--root", help="Knowledge-base root; defaults to manifest directory")
    parser.add_argument("--output")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    root = Path(args.root).resolve() if args.root else manifest_path.parent
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    claim = data.get("status_claim", "")
    required = STATUS_REQUIREMENTS.get(claim)
    errors = []

    if required is None:
        errors.append(f"unknown status_claim: {claim}")
        required = set()

    tasks = {item.get("id"): item for item in data.get("tasks", [])}
    artifacts = data.get("artifacts", {})
    exceptions = {
        item.get("task_id"): item.get("reason", "")
        for item in data.get("exceptions", [])
        if item.get("accepted") is True
    }

    for task_id in sorted(required):
        task = tasks.get(task_id)
        if not task:
            errors.append(f"missing task: {task_id}")
            continue
        if task.get("status") != "completed" and task_id not in exceptions:
            errors.append(f"incomplete task: {task_id}")
        if not artifact_exists(root, str(artifacts.get(task_id, ""))) and task_id not in exceptions:
            errors.append(f"missing artifact: {task_id}")

    unfinished = [
        item.get("id", "")
        for item in data.get("tasks", [])
        if item.get("required") is True and item.get("status") in {"pending", "in_progress"}
        and item.get("id") not in exceptions
    ]
    if unfinished:
        errors.append("unfinished required tasks: " + ", ".join(unfinished))

    execution_unfinished = [
        str(item.get("id", ""))
        for item in data.get("execution_tasks", [])
        if item.get("required") is True and item.get("status") in {"pending", "in_progress"}
    ]
    if execution_unfinished:
        errors.append("unfinished execution tasks: " + ", ".join(execution_unfinished))

    application_result = data.get("application_result")
    if claim == "application_validated" and application_result != "success":
        errors.append("application_validated requires application_result=success")
    if claim == "application_partially_validated" and application_result != "partial":
        errors.append("application_partially_validated requires application_result=partial")
    if claim == "formally_delivered" and data.get("user_confirmed") is not True:
        errors.append("formally_delivered requires user_confirmed=true")

    report = {
        "status_claim": claim,
        "valid": not errors,
        "errors": errors,
        "accepted_exceptions": exceptions,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).resolve().write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
