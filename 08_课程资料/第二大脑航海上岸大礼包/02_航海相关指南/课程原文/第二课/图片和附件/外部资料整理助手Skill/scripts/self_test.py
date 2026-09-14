#!/usr/bin/env python3
"""Run a dependency-free end-to-end test of the bundled helper scripts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def run(*args: str) -> None:
    command = [sys.executable, *args]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(
            f"Command failed: {' '.join(command)}\n{result.stdout}\n{result.stderr}"
        )


def run_expect_failure(*args: str) -> None:
    command = [sys.executable, *args]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        raise RuntimeError(f"Command unexpectedly passed: {' '.join(command)}")


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="organize-knowledge-sources-") as temp:
        root = Path(temp)
        sources = root / "sources"
        materials = root / "materials"
        sources.mkdir()
        materials.mkdir()

        (sources / "guide.txt").write_text(
            "A reusable workflow should state the scenario, steps, and evidence.",
            encoding="utf-8",
        )
        (sources / "notes.md").write_text(
            "# Notes\n\nUse validation to identify unsupported conclusions.",
            encoding="utf-8",
        )
        (materials / "material.md").write_text(
            """---
material_id: MAT-0001
record_kind: atomic_material
title: 可复用流程
type: method
status: ready
created: 2026-01-01
summary: 说明如何形成可复用流程
source_ids: [SRC-0001]
applicable_scenarios: [资料整理]
related_tools: []
target_users: [知识工作者]
timeliness: stable
verification_status: verified
keywords: [流程, 验证]
---

## 内容

明确场景、步骤与证据，并通过验证发现缺口。
""",
            encoding="utf-8",
        )

        inventory = root / "inventory.json"
        fingerprints = root / "fingerprints.json"
        ledger = root / "ledger.json"
        validation = root / "validation.json"
        corpus = root / "corpus.json"
        tests = root / "tests.json"
        vocabulary = root / "vocabulary.json"
        retrieval = root / "retrieval.json"
        knowledge_base = root / "knowledge-base"
        structure_blueprint = root / "structure.json"
        structure_report = root / "structure-report.json"
        write_json(
            structure_blueprint,
            {
                "version": 1,
                "knowledge_base_name": "test",
                "directories": [
                    {"id": "overview", "path": "00_overview", "purpose": "overview", "required": True},
                    {"id": "materials", "path": "01_materials", "purpose": "materials", "required": True},
                ],
            },
        )
        run(
            str(SCRIPT_DIR / "initialize_knowledge_base.py"),
            str(knowledge_base),
            str(structure_blueprint),
            "--report",
            str(root / "initialization-report.json"),
        )
        run(
            str(SCRIPT_DIR / "validate_structure.py"),
            str(knowledge_base),
            str(structure_blueprint),
            "--output",
            str(structure_report),
        )

        run(str(SCRIPT_DIR / "inventory_sources.py"), str(sources), "--output", str(inventory))
        run(
            str(SCRIPT_DIR / "fingerprint_sources.py"),
            str(inventory),
            "--output",
            str(fingerprints),
        )
        run(str(SCRIPT_DIR / "build_ledger.py"), str(inventory), "--output", str(ledger))
        run(
            str(SCRIPT_DIR / "validate_materials.py"),
            str(materials),
            "--output",
            str(validation),
        )

        write_json(
            corpus,
            [
                {
                    "id": "MAT-0001",
                    "title": "可复用流程",
                    "body": "明确场景、步骤与证据，并通过验证发现缺口。",
                    "metadata": {"keywords": ["流程", "验证"]},
                }
            ],
        )
        write_json(
            tests,
            [{"id": "TEST-0001", "query": "验证", "expected_ids": ["MAT-0001"]}],
        )
        write_json(
            vocabulary,
            {
                "concepts": {
                    "验证": {
                        "strict_synonyms": ["核验"],
                        "user_expressions": ["检查结果"],
                        "related_terms": ["证据"],
                    }
                },
                "intents": {},
            },
        )
        run(
            str(SCRIPT_DIR / "retrieval_test.py"),
            "--materials",
            str(corpus),
            "--tests",
            str(tests),
            "--vocabulary",
            str(vocabulary),
            "--output",
            str(retrieval),
        )

        artifact_paths = {}
        for task_id in [
            "purpose", "blueprint", "structure_initialization", "inventory", "ledger", "source_summaries",
            "atomic_materials", "source_relations", "retrieval_validation",
            "application_validation", "coverage_report", "user_confirmation",
        ]:
            path = knowledge_base / f"{task_id}.md"
            path.write_text(f"# {task_id}\n", encoding="utf-8")
            artifact_paths[task_id] = path.name

        task_ids = list(artifact_paths)
        incomplete_manifest = knowledge_base / "incomplete-manifest.json"
        write_json(
            incomplete_manifest,
            {
                "version": 1,
                "status_claim": "knowledge_base_initialized",
                "tasks": [
                    {
                        "id": task_id,
                        "required": task_id not in {"application_validation", "user_confirmation"},
                        "status": "completed"
                        if task_id in {"purpose", "blueprint", "structure_initialization", "inventory", "ledger", "source_summaries"}
                        else "pending",
                    }
                    for task_id in task_ids
                ],
                "artifacts": {
                    task_id: artifact_paths[task_id]
                    if task_id in {"purpose", "blueprint", "structure_initialization", "inventory", "ledger", "source_summaries"}
                    else ""
                    for task_id in task_ids
                },
                "exceptions": [],
            },
        )
        run_expect_failure(
            str(SCRIPT_DIR / "validate_completion.py"),
            str(incomplete_manifest),
            "--root",
            str(knowledge_base),
        )

        complete_manifest = knowledge_base / "complete-manifest.json"
        write_json(
            complete_manifest,
            {
                "version": 1,
                "status_claim": "application_validated",
                "tasks": [
                    {
                        "id": task_id,
                        "required": task_id != "user_confirmation",
                        "status": "completed" if task_id != "user_confirmation" else "pending",
                    }
                    for task_id in task_ids
                ],
                "artifacts": artifact_paths,
                "application_result": "success",
                "user_confirmed": False,
                "execution_tasks": [],
                "exceptions": [],
            },
        )
        completion_report = knowledge_base / "completion-report.json"
        run(
            str(SCRIPT_DIR / "validate_completion.py"),
            str(complete_manifest),
            "--root",
            str(knowledge_base),
            "--output",
            str(completion_report),
        )

        formal_manifest = knowledge_base / "formal-manifest.json"
        formal_data = json.loads(complete_manifest.read_text(encoding="utf-8"))
        formal_data["status_claim"] = "formally_delivered"
        write_json(formal_manifest, formal_data)
        run_expect_failure(
            str(SCRIPT_DIR / "validate_completion.py"),
            str(formal_manifest),
            "--root",
            str(knowledge_base),
        )
        formal_data["user_confirmed"] = True
        for task in formal_data["tasks"]:
            if task["id"] == "user_confirmation":
                task["status"] = "completed"
        write_json(formal_manifest, formal_data)
        run(
            str(SCRIPT_DIR / "validate_completion.py"),
            str(formal_manifest),
            "--root",
            str(knowledge_base),
        )

        partial_manifest = knowledge_base / "partial-manifest.json"
        partial_data = json.loads(complete_manifest.read_text(encoding="utf-8"))
        partial_data["status_claim"] = "application_partially_validated"
        partial_data["application_result"] = "partial"
        write_json(partial_manifest, partial_data)
        run(
            str(SCRIPT_DIR / "validate_completion.py"),
            str(partial_manifest),
            "--root",
            str(knowledge_base),
        )

        bad_materials = root / "bad-materials"
        bad_materials.mkdir()
        (bad_materials / "legacy.md").write_text("# Legacy material\n", encoding="utf-8")
        run_expect_failure(str(SCRIPT_DIR / "validate_materials.py"), str(bad_materials))

        duplicate_blueprint = root / "duplicate-structure.json"
        write_json(
            duplicate_blueprint,
            {
                "directories": [
                    {"id": "a", "path": "05_reports", "required": True},
                    {"id": "b", "path": "05_results", "required": True},
                ]
            },
        )
        run_expect_failure(
            str(SCRIPT_DIR / "initialize_knowledge_base.py"),
            str(root / "duplicate-kb"),
            str(duplicate_blueprint),
        )

        assertions = [
            json.loads(inventory.read_text(encoding="utf-8"))["file_count"] == 2,
            len(json.loads(fingerprints.read_text(encoding="utf-8"))["items"]) == 2,
            len(json.loads(ledger.read_text(encoding="utf-8"))["sources"]) == 2,
            json.loads(validation.read_text(encoding="utf-8"))["valid"] is True,
            json.loads(structure_report.read_text(encoding="utf-8"))["valid"] is True,
            json.loads(retrieval.read_text(encoding="utf-8"))["recall"] == 1.0,
            json.loads(completion_report.read_text(encoding="utf-8"))["valid"] is True,
        ]
        if not all(assertions):
            raise RuntimeError("Self-test assertions failed")

    print("All bundled workflow tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
