"""Module responsible for moving files according to rules."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .rules_engine import RulesEngine, Rule
from .logger import get_logger


@dataclass
class OrganizeResult:
    """Result returned after attempting to organize a file."""

    source: Path
    destination: Optional[Path]
    action: str  # moved/skipped/failed
    success: bool
    reason: Optional[str] = None


class FileOrganizer:
    """Handles organizing individual files and directories."""

    def __init__(self, config: Dict[str, Any], dry_run: bool = False) -> None:
        """Initialize the organizer.

        Args:
            config: Configuration dictionary from config.yaml.
            dry_run: If ``True`` actions are logged but not executed.
        """
        self.config = config
        output_dir = Path(config.get("output_directory", "Organized")).expanduser()
        self.rules_engine = RulesEngine(
            [Rule(**r) for r in config.get("rules", [])], output_dir
        )
        self.dry_run = dry_run
        self.logger = get_logger(__name__)

    def organize_file(self, file_path: Path) -> OrganizeResult:
        """Organize a single file according to the rules.

        Args:
            file_path: Path to the file to process.

        Returns:
            :class:`OrganizeResult` describing the outcome.
        """
        dest = self.rules_engine.match(file_path)
        if dest is None:
            self.logger.debug("No matching rule for %s", file_path)
            return OrganizeResult(file_path, None, "skipped", True, "no rule")

        dest_full = dest
        try:
            dest_full.parent.mkdir(parents=True, exist_ok=True)
            if self.dry_run:
                self.logger.info("[DRY RUN] Would move %s -> %s", file_path, dest_full)
                return OrganizeResult(file_path, dest_full, "moved", True, "dry run")

            self.logger.info("Moving %s -> %s", file_path, dest_full)
            file_path.rename(dest_full)
            return OrganizeResult(file_path, dest_full, "moved", True)
        except Exception as e:
            self.logger.error("Error moving %s to %s: %s", file_path, dest_full, e)
            return OrganizeResult(file_path, dest_full, "failed", False, str(e))

    def organize_directory(
        self, directory: Path, recursive: bool = False
    ) -> List[OrganizeResult]:
        """Process all files within a directory.

        Args:
            directory: Directory to scan.
            recursive: Whether to descend into subdirectories.

        Returns:
            List of :class:`OrganizeResult` for each file processed.
        """
        results: List[OrganizeResult] = []
        if recursive:
            iterator = directory.rglob("*")
        else:
            iterator = directory.iterdir()
        for item in iterator:
            if item.is_file():
                results.append(self.organize_file(item))
        return results
