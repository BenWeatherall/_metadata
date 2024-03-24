#!/usr/bin/env python3
from typing import List
from pathlib import Path

def get_project_directories(base_path: Path, is_include_venv = False) -> List[Path]:
    setup_files = base_path.glob("**/setup.py")
    required_files = base_path.glob("**/requirements.txt")

    all_paths = set(list(setup_files) + list(required_files))

    results = []

    for project_path in all_paths:
        if is_include_venv:
            results.append(project_path.parent)
        elif ".venv" not in str(project_path.parent):
            results.append(project_path.parent)

    return sorted(results)
