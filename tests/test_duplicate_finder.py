"""Tests for duplicate finder utilities."""

from __future__ import annotations

from pathlib import Path

import pytest

from smartvault.duplicate_finder import compute_hash, DuplicateFinder


def test_no_duplicates_returns_empty_dict(tmp_path: Path) -> None:
    df = DuplicateFinder(tmp_path)
    assert df.scan() == {}


def test_identical_files_detected_as_duplicates(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_bytes(b"hello")
    b.write_bytes(b"hello")
    df = DuplicateFinder(tmp_path)
    res = df.scan()
    assert len(res) == 1
    for paths in res.values():
        assert set(paths) == {a, b}


def test_compute_hash_consistency(tmp_path: Path) -> None:
    f = tmp_path / "f.bin"
    f.write_bytes(b"data")
    h1 = compute_hash(f)
    h2 = compute_hash(f)
    assert h1 == h2
