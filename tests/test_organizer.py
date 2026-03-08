"""Tests for the organizer module."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from smartvault.organizer import FileOrganizer, OrganizeResult


def load_config() -> dict[str, Any]:
    return {
        "output_directory": "",
        "rules": [
            {"name": "txt", "extensions": [".txt"], "keywords": [], "destination": "txt"}
        ],
    }


def test_organize_file_dry_run(tmp_path: Path) -> None:
    cfg = load_config()
    organizer = FileOrganizer(cfg, dry_run=True)
    source = tmp_path / "a.txt"
    source.write_text("hello")
    result = organizer.organize_file(source)
    assert result.action == "moved"
    assert result.success
    assert source.exists()


def test_organize_file_moves_correctly(tmp_path: Path) -> None:
    cfg = load_config()
    organizer = FileOrganizer(cfg)
    source = tmp_path / "b.txt"
    source.write_text("data")
    result = organizer.organize_file(source)
    assert result.success
    assert result.destination is not None
    assert not source.exists()
    assert result.destination.exists()


def test_organize_returns_correct_result_fields(tmp_path: Path) -> None:
    cfg = load_config()
    organizer = FileOrganizer(cfg, dry_run=True)
    source = tmp_path / "c.doc"
    source.write_text("no match")
    result = organizer.organize_file(source)
    assert result.action == "skipped"
    assert result.success
    assert result.reason == "no rule"
