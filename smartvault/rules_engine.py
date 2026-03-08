"""Rules engine for matching files to destinations."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta


@dataclass
class Rule:
    """A single rule used to classify files.

    Attributes:
        name: Human-readable name of the rule.
        extensions: List of file extensions (including dot) to match.
        keywords: List of keywords to search for in file name.
        destination: Path template relative to output directory.
        age_days: Optional number of days old for age-based rules.
    """

    name: str
    extensions: List[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    destination: str = ""
    age_days: Optional[int] = None

class RulesEngine:
    """Engine that holds rules and matches files against them."""

    def __init__(self, rules: List[Rule], output_dir: Path) -> None:
        """Initialize the rules engine.

        Args:
            rules: List of :class:`Rule` instances.
            output_dir: Base directory where files will be moved.
        """
        self.rules = rules
        self.output_dir = output_dir

    def match(self, file_path: Path) -> Optional[Path]:
        """Match a file against the configured rules.

        Matching prioritizes extension, then keyword, then age. If a rule
        applies the destination template is resolved and returned. If no
        rule matches, ``None`` is returned.

        Args:
            file_path: Path to the candidate file.

        Returns:
            A resolved destination path relative to ``output_dir`` or ``None``.
        """
        name_lower = file_path.name.lower()
        stat = file_path.stat()
        modified = datetime.fromtimestamp(stat.st_mtime)
        age = datetime.now() - modified

        for rule in self.rules:
            if rule.extensions and file_path.suffix.lower() not in [e.lower() for e in rule.extensions]:
                continue
            if rule.keywords:
                if not any(kw.lower() in name_lower for kw in rule.keywords):
                    continue
            if rule.age_days is not None:
                if age < timedelta(days=rule.age_days):
                    continue
            # matched
            dest = self.resolve_dynamic_path(rule.destination, file_path)
            return self.output_dir / dest
        return None

    def resolve_dynamic_path(self, template: str, file_path: Path) -> Path:
        """Resolve dynamic tokens in a destination template.

        Supported tokens are ``{YYYY}``, ``{MM}``, and ``{DD}``, derived from
        the file's modification time.

        Args:
            template: Destination path template.
            file_path: Path used to extract the date.

        Returns:
            Resolved :class:`Path` instance.
        """
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        substitutions = {
            "YYYY": f"{mtime.year:04d}",
            "MM": f"{mtime.month:02d}",
            "DD": f"{mtime.day:02d}",
        }
        path_str = template
        for key, val in substitutions.items():
            path_str = path_str.replace(f"{{{key}}}", val)
        return Path(path_str)
