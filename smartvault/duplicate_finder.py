"""Detect and manage duplicate files within a directory."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from .logger import get_logger


def compute_hash(file_path: Path, algorithm: str = "sha256") -> str:
    """Compute a hash for a file reading in chunks.

    Args:
        file_path: Path to the file to hash.
        algorithm: Hash algorithm to use (default: sha256).

    Returns:
        Hexadecimal digest string.
    """
    h = hashlib.new(algorithm)
    with file_path.open("rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class DuplicateSummary:
    total_files: int
    duplicate_groups: int
    duplicate_count: int
    wasted_bytes: int
    largest_duplicate_group: int


class DuplicateFinder:
    """Scan a directory for duplicate files based on hash."""

    def __init__(self, directory: Path) -> None:
        """Initialize with a base directory to scan.

        Args:
            directory: Path to scan for duplicates.
        """
        self.directory = directory
        self.logger = get_logger(__name__)

    def scan(self) -> Dict[str, List[Path]]:
        """Perform a scan and return hash to paths map.

        Returns:
            Dictionary where keys are hash strings and values are lists of
            paths that share that hash.
        """
        hashes: Dict[str, List[Path]] = {}
        for path in self.directory.rglob("*"):
            if path.is_file():
                try:
                    h = compute_hash(path)
                except Exception as e:
                    self.logger.error("Failed hashing %s: %s", path, e)
                    continue
                hashes.setdefault(h, []).append(path)
        return {k: v for k, v in hashes.items() if len(v) > 1}

    def get_summary(self) -> DuplicateSummary:
        """Generate summary statistics after a scan.

        Returns:
            :class:`DuplicateSummary` with counts and bytes wasted.
        """
        groups = self.scan()
        total_files = sum(len(v) for v in groups.values())
        duplicate_groups = len(groups)
        duplicate_count = total_files - duplicate_groups
        wasted = 0
        largest = 0
        for paths in groups.values():
            sizes = [p.stat().st_size for p in paths]
            wasted += sum(sizes) - max(sizes)
            largest = max(largest, len(paths))
        return DuplicateSummary(
            total_files=total_files,
            duplicate_groups=duplicate_groups,
            duplicate_count=duplicate_count,
            wasted_bytes=wasted,
            largest_duplicate_group=largest,
        )

    def handle_duplicates(self, action: str, dry_run: bool) -> List[str]:
        """Take action on detected duplicates.

        Args:
            action: ``report`` | ``delete`` | ``move``.
            dry_run: If true, simulate only.

        Returns:
            List of messages summarizing the performed actions.
        """
        results: List[str] = []
        groups = self.scan()
        for h, paths in groups.items():
            # keep newest (largest mtime)
            paths_sorted = sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)
            keep = paths_sorted[0]
            to_handle = paths_sorted[1:]
            if action == "report":
                results.append(f"Hash {h}: keep {keep}, duplicates {to_handle}")
            elif action == "delete":
                for p in to_handle:
                    if dry_run:
                        results.append(f"[DRY RUN] Would delete {p}")
                    else:
                        try:
                            p.unlink()
                            results.append(f"Deleted {p}")
                        except Exception as e:
                            results.append(f"Failed to delete {p}: {e}")
            elif action == "move":
                for p in to_handle:
                    dest = p.with_name(p.name + ".dup")
                    if dry_run:
                        results.append(f"[DRY RUN] Would move {p} -> {dest}")
                    else:
                        try:
                            p.rename(dest)
                            results.append(f"Moved {p} -> {dest}")
                        except Exception as e:
                            results.append(f"Failed to move {p}: {e}")
            else:
                raise ValueError("Invalid action")
        return results
