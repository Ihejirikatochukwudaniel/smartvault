"""Tests for the rules engine."""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timedelta

import pytest

from smartvault.rules_engine import Rule, RulesEngine


def make_file(tmp_path: Path, name: str, days_ago: int = 0) -> Path:
    p = tmp_path / name
    p.write_text("x")
    if days_ago:
        t = datetime.now() - timedelta(days=days_ago)
        p.utime((t.timestamp(), t.timestamp()))
    return p


def test_extension_match(tmp_path: Path) -> None:
    r = Rule("test", [".txt"], [], "dest")
    engine = RulesEngine([r], tmp_path)
    f = make_file(tmp_path, "a.txt")
    assert engine.match(f) == tmp_path / "dest"


def test_keyword_match_takes_priority(tmp_path: Path) -> None:
    r1 = Rule("r1", [".txt"], [], "first")
    r2 = Rule("r2", [".txt"], ["hello"], "second")
    engine = RulesEngine([r2, r1], tmp_path)
    f = make_file(tmp_path, "hello.txt")
    assert engine.match(f) == tmp_path / "second"


def test_dynamic_path_date_tokens(tmp_path: Path) -> None:
    r = Rule("r", [".txt"], [], "y/{YYYY}/{MM}")
    engine = RulesEngine([r], tmp_path)
    f = make_file(tmp_path, "a.txt")
    dest = engine.match(f)
    assert dest is not None
    assert "y/" in str(dest)


def test_no_match_returns_none(tmp_path: Path) -> None:
    r = Rule("r", [".jpg"], [], "x")
    engine = RulesEngine([r], tmp_path)
    f = make_file(tmp_path, "a.txt")
    assert engine.match(f) is None
