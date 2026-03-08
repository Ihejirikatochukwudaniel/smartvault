"""Reporting utilities for SmartVault."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Any

from jinja2 import Environment, FileSystemLoader, select_autoescape


@dataclass
class ReportData:
    run_timestamp: datetime
    duration_seconds: float
    files_processed: int
    files_moved: int
    files_skipped: int
    errors: int
    duplicate_summary: Optional[Any]
    organize_results: List[Any]
    space_saved_bytes: int


class Reporter:
    """Generates HTML and CSV reports from run data."""

    def __init__(self, template_dir: Path, output_dir: Path) -> None:
        """Initialize the reporter.

        Args:
            template_dir: Directory containing Jinja templates.
            output_dir: Directory where reports will be written.
        """
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_html(self, data: ReportData) -> Path:
        """Render HTML report from template and save to disk.

        Args:
            data: :class:`ReportData` instance.

        Returns:
            Path to the generated HTML file.
        """
        template = self.env.get_template("report.html.j2")
        rendered = template.render(data=data)
        fname = f"report_{data.run_timestamp.strftime('%Y%m%d_%H%M%S')}.html"
        out_path = self.output_dir / fname
        out_path.write_text(rendered, encoding="utf-8")
        return out_path

    def generate_csv(self, data: ReportData) -> Path:
        """Write organize results to a CSV file.

        Args:
            data: :class:`ReportData` instance.

        Returns:
            Path to the generated CSV file.
        """
        fname = f"report_{data.run_timestamp.strftime('%Y%m%d_%H%M%S')}.csv"
        out_path = self.output_dir / fname
        with out_path.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["source", "destination", "action", "success", "reason"])
            for r in data.organize_results:
                writer.writerow([
                    str(r.source),
                    str(r.destination) if r.destination else "",
                    r.action,
                    r.success,
                    r.reason or "",
                ])
        return out_path
