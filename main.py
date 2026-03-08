"""Entry point for SmartVault command-line interface."""

from __future__ import annotations

import argparse
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

import yaml

from smartvault.logger import setup_logger
from smartvault.organizer import FileOrganizer
from smartvault.duplicate_finder import DuplicateFinder
from smartvault.watcher import DirectoryWatcher
from smartvault.reporter import Reporter, ReportData


ASCII_BANNER = r"""
  ____                 _   _      _
 / ___|  ___ _ __ ___ | | | | ___| |_ ___
 \___ \ / _ \ '_ ` _ \| |_| |/ _ \ __/ _ \
  ___) |  __/ | | | | |  _  |  __/ ||  __/
 |____/ \___|_| |_| |_|_| |_|\___|\__\___|
"""  


def load_config(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)


def main() -> None:
    parser = argparse.ArgumentParser(prog="SmartVault")
    parser.add_argument("--config", type=Path, help="path to config.yaml")
    sub = parser.add_subparsers(dest="cmd")

    watch_p = sub.add_parser("watch")
    watch_p.add_argument("directory", type=Path)
    watch_p.add_argument("--dry-run", action="store_true")

    scan_p = sub.add_parser("scan")
    scan_p.add_argument("directory", type=Path)
    scan_p.add_argument("--recursive", action="store_true")
    scan_p.add_argument("--report", action="store_true")
    scan_p.add_argument("--check-dupes", action="store_true")
    scan_p.add_argument("--dry-run", action="store_true")

    dupes_p = sub.add_parser("dupes")
    dupes_p.add_argument("directory", type=Path)
    dupes_p.add_argument("--action", choices=["report", "delete", "move"], default="report")
    dupes_p.add_argument("--dry-run", action="store_true")

    report_p = sub.add_parser("report")
    report_p.add_argument("--last", action="store_true")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    config_path = args.config or Path("config.yaml")
    config = load_config(config_path)
    logger = setup_logger(__name__, config)
    logger.info(ASCII_BANNER)

    if args.cmd == "watch":
        organizer = FileOrganizer(config, dry_run=args.dry_run or config.get("dry_run", False))
        watcher = DirectoryWatcher(args.directory.expanduser(), organizer)
        watcher.start()

    elif args.cmd == "scan":
        organizer = FileOrganizer(config, dry_run=args.dry_run or config.get("dry_run", False))
        start = datetime.now()
        results = organizer.organize_directory(args.directory.expanduser(), recursive=args.recursive)
        duration = (datetime.now() - start).total_seconds()
        if args.check_dupes:
            df = DuplicateFinder(args.directory.expanduser())
            dup_summary = df.get_summary()
        else:
            dup_summary = None
        if args.report:
            rpt = Reporter(Path("templates"), Path("reports"))
            data = ReportData(
                run_timestamp=start,
                duration_seconds=duration,
                files_processed=len(results),
                files_moved=sum(1 for r in results if r.action == "moved"),
                files_skipped=sum(1 for r in results if r.action == "skipped"),
                errors=sum(1 for r in results if not r.success),
                duplicate_summary=dup_summary,
                organize_results=results,
                space_saved_bytes=getattr(dup_summary, "wasted_bytes", 0),
            )
            html = rpt.generate_html(data)
            csv = rpt.generate_csv(data)
            logger.info("Report generated: %s and %s", html, csv)

    elif args.cmd == "dupes":
        df = DuplicateFinder(args.directory.expanduser())
        msgs = df.handle_duplicates(args.action, dry_run=args.dry_run or config.get("dry_run", False))
        for m in msgs:
            logger.info(m)

    elif args.cmd == "report":
        out_dir = Path("reports")
        if args.last:
            files = sorted(out_dir.glob("report_*.html"))
            if files:
                webbrowser.open(files[-1].as_uri())
            else:
                logger.warning("No reports found")
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
