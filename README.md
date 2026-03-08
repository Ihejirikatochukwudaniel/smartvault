```
  ██████  ███▄ ▄███▓ ▄▄▄       ██▀███  ▄▄▄█████▓ ██▒   █▓ ▄▄▄       █    ██  ██▓ ▄▄▄█████▓
▒██    ▒ ▓██▒▀█▀ ██▒▒████▄    ▓██ ▒ ██▒▓  ██▒ ▓▒▓██░   █▒▒████▄     ██  ▓██▒▓██▒ ▓  ██▒ ▓▒
░ ▓██▄   ▓██    ▓██░▒██  ▀█▄  ▓██ ░▄█ ▒▒ ▓██░ ▒░ ▓██  █▒░▒██  ▀█▄  ▓██  ▒██░▒██░ ▒ ▓██░ ▒░
  ▒   ██▒▒██    ▒██ ░██▄▄▄▄██ ▒██▀▀█▄  ░ ▓██▓ ░   ▒██ █░░░██▄▄▄▄██ ▓▓█  ░██░▒██░ ░ ▓██▓ ░ 
▒██████▒▒▒██▒   ░██▒ ▓█   ▓██▒░██▓ ▒██▒  ▒██▒ ░    ▒▀█░   ▓█   ▓██▒▒▒█████▓ ░██████▒▒██▒ ░ 
▒ ▒▓▒ ▒ ░░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░  ▒ ░░      ░ ▐░   ▒▒   ▓▒█░░▒▓▒ ▒ ▒ ░ ▒░▓  ░▒ ░░   
░ ░▒  ░ ░░  ░      ░  ▒   ▒▒ ░  ░▒ ░ ▒░    ░       ░ ░░    ▒   ▒▒ ░░░▒░ ░ ░ ░ ░ ▒  ░  ░    
░  ░  ░  ░      ░     ░   ▒     ░░   ░   ░           ░░    ░   ▒    ░░░ ░ ░   ░ ░   ░      
      ░         ░         ░  ░   ░                    ░        ░  ░   ░         ░  ░ ░      
```

<div align="center">

**An intelligent, rule-based file organization system built with Python**  
*Watches. Classifies. Organizes. Reports. All automatically.*

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/Tests-Passing-22c55e?style=for-the-badge&logo=pytest&logoColor=white)](#-running-tests)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-f97316?style=for-the-badge)](CONTRIBUTING.md)

[Quick Start](#-installation) · [Usage Guide](#-usage) · [Configuration](#-configuration) · [Report Demo](#-sample-report) · [Roadmap](#-roadmap)

</div>

---

## 📖 Overview

SmartVault solves a universal problem: **your file system is a mess, and organizing it manually is a waste of your time.**

Drop a file into your Downloads folder — SmartVault instantly classifies it, moves it to the right destination, dates it correctly, and logs everything. It runs silently in the background as a real-time watcher, or on-demand as a scanner. It detects duplicates, generates visual reports, and never does anything you haven't approved first via dry-run.

Built to production standards: type hints throughout, config-driven behavior, modular architecture, and full test coverage.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔭 **Real-time Watching** | Monitors directories via filesystem events — zero polling, instant response |
| 🧠 **Smart Rule Engine** | Matches files by extension, filename keywords, and age with priority ordering |
| 📅 **Dynamic Date Paths** | Destinations like `Media/Images/{YYYY}/{MM}` resolve automatically from file metadata |
| 🔍 **Duplicate Detection** | SHA-256 content hashing finds identical files regardless of name |
| 📊 **Rich Reports** | Generates dark-themed HTML reports and CSV exports after every run |
| 🔁 **Dry-Run Mode** | Preview every action before a single file is touched |
| ⚙️ **YAML Configuration** | All behavior driven by `config.yaml` — no code changes needed |
| 🪵 **Structured Logging** | Rotating log files with colored terminal output via `colorlog` |
| 🧪 **Full Test Suite** | `pytest` + `pytest-cov` covering organizer, rules engine, and duplicate finder |

---

## 🏗️ Project Structure

```
SmartVault/
│
├── main.py                        ← CLI entry point; wires all modules together
├── config.yaml                    ← All runtime behavior configured here
├── requirements.txt               ← Pinned dependencies
├── README.md
├── .gitignore
│
├── smartvault/                    ← Core library package
│   ├── __init__.py
│   ├── watcher.py                 ← Watchdog filesystem event handler + Observer
│   ├── organizer.py               ← File moving logic; returns OrganizeResult objects
│   ├── duplicate_finder.py        ← SHA-256 hashing, DuplicateFinder, DuplicateSummary
│   ├── rules_engine.py            ← Rule dataclass + RulesEngine matching logic
│   ├── reporter.py                ← HTML (Jinja2) + CSV report generation
│   └── logger.py                  ← RotatingFileHandler + colorlog setup
│
├── templates/
│   └── report.html.j2             ← Dark-themed Jinja2 HTML report template
│
├── logs/                          ← Auto-populated; gitignored except .gitkeep
│   └── .gitkeep
│
├── reports/                       ← Auto-populated; gitignored except .gitkeep
│   └── .gitkeep
│
└── tests/
    ├── __init__.py
    ├── test_organizer.py          ← dry-run, move, result fields
    ├── test_duplicate_finder.py   ← hash consistency, dupe detection
    └── test_rules_engine.py       ← extension, keyword, date token, no-match
```

---

## ⚙️ Installation

**Prerequisites:** Python 3.11 or higher

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/smartvault.git
cd smartvault

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

**Verify installation:**
```bash
python main.py --help
```

You should see the SmartVault ASCII banner and the full command reference.

---

## 🚀 Usage

### Commands at a Glance

```
python main.py <command> [options]

Commands:
  watch     Monitor a directory in real-time
  scan      Organize an existing directory once
  dupes     Find and handle duplicate files
  report    Open or list generated reports
```

---

### `watch` — Real-Time Organization

Start the background watcher. Every new file that lands in the directory is instantly classified and moved.

```bash
# Watch your Downloads folder
python main.py watch ~/Downloads

# Simulate — see what would happen without moving anything
python main.py watch ~/Downloads --dry-run

# Use a custom config file
python main.py watch ~/Downloads --config /path/to/custom_config.yaml
```

> Press `Ctrl+C` to stop the watcher gracefully.

---

### `scan` — One-Time Organization

Run a single pass over an existing directory. Ideal for first-time setup or periodic cleanup.

```bash
# Basic scan
python main.py scan ~/Downloads

# Recursive scan (includes subdirectories) + HTML/CSV report
python main.py scan ~/Downloads --recursive --report

# Full audit: scan + duplicate check + report, no changes made
python main.py scan ~/Downloads --recursive --check-dupes --report --dry-run
```

---

### `dupes` — Duplicate Management

Scan for duplicate files using content hashing (SHA-256). Operates independently of the rule engine.

```bash
# Report only — list all duplicates, touch nothing
python main.py dupes ~/Downloads --action report

# Delete duplicates (keeps the newest copy)
python main.py dupes ~/Downloads --action delete

# Move duplicates to a holding folder
python main.py dupes ~/Downloads --action move

# Always preview first
python main.py dupes ~/Downloads --action delete --dry-run
```

---

### `report` — View Reports

```bash
# Open the most recent report in your browser
python main.py report --last
```

---

## 🗂️ How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SmartVault Pipeline                          │
└─────────────────────────────────────────────────────────────────────┘

  New File Detected
        │
        ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│    Watcher    │────▶│  Rules Engine │────▶│   Organizer   │
│  (watchdog)   │     │  (rules_engine│     │  (organizer)  │
│               │     │  .py)         │     │               │
│ • Filesystem  │     │ • Extension   │     │ • Move file   │
│   events      │     │   match       │     │ • Dry-run     │
│ • Debounce    │     │ • Keyword     │     │   support     │
│   500ms       │     │   match       │     │ • Error       │
│ • Skip hidden │     │ • Age check   │     │   handling    │
│   & temp      │     │ • Date token  │     │ • Returns     │
│   files       │     │   resolution  │     │   result obj  │
└───────────────┘     └───────────────┘     └───────────────┘
                                                    │
                                                    ▼
                                          ┌───────────────┐
                                          │   Reporter    │
                                          │  (reporter.py)│
                                          │               │
                                          │ • HTML report │
                                          │ • CSV export  │
                                          │ • Dupe summary│
                                          │ • Space saved │
                                          └───────────────┘
                                                    │
                                                    ▼
                                          ┌───────────────┐
                                          │    Logger     │
                                          │  (logger.py)  │
                                          │               │
                                          │ • Rotating    │
                                          │   log file    │
                                          │ • Colored     │
                                          │   terminal    │
                                          └───────────────┘
```

---

## 📋 Configuration

All behavior is controlled by `config.yaml`. No code changes required.

```yaml
# config.yaml — full reference

watch_directory: ~/Downloads           # Directory to monitor or scan
output_directory: ~/SmartVault/Organized  # Root destination for organized files
dry_run: false                         # true = simulate only, no files moved
duplicate_action: report               # report | delete | move
log_level: INFO                        # DEBUG | INFO | WARNING | ERROR
log_max_bytes: 5242880                 # 5MB — max size before log rotation
log_backup_count: 3                    # number of rotated log files to keep

rules:
  - name: "Invoice PDFs"              # Checked BEFORE generic PDFs (keyword priority)
    extensions: [.pdf]
    keywords: ["invoice", "receipt", "bill"]
    destination: Finance/Invoices

  - name: "PDF Documents"
    extensions: [.pdf]
    destination: Documents/PDFs

  - name: "Images"
    extensions: [.jpg, .jpeg, .png, .gif, .webp, .svg]
    destination: Media/Images/{YYYY}/{MM}   # ← dynamic date tokens

  - name: "Videos"
    extensions: [.mp4, .mov, .avi, .mkv]
    destination: Media/Videos/{YYYY}

  - name: "Code Files"
    extensions: [.py, .js, .ts, .html, .css, .json, .yaml, .yml]
    destination: Code

  - name: "Archives"
    extensions: [.zip, .tar, .gz, .rar, .7z]
    destination: Archives

  - name: "Old Files"               # Age-based rule — no extension needed
    age_days: 365
    destination: Archive/OldFiles
```

### Configuration Reference

| Field | Type | Default | Description |
|---|---|---|---|
| `watch_directory` | `str` | `~/Downloads` | Target directory to monitor or scan |
| `output_directory` | `str` | `~/SmartVault/Organized` | Root folder for all organized files |
| `dry_run` | `bool` | `false` | When `true`, logs actions but moves nothing |
| `duplicate_action` | `str` | `report` | How to handle duplicates: `report`, `delete`, or `move` |
| `log_level` | `str` | `INFO` | Python logging level |
| `log_max_bytes` | `int` | `5242880` | Max log file size before rotation (bytes) |
| `log_backup_count` | `int` | `3` | Number of backup log files to keep |
| `rules` | `list` | `[]` | Ordered list of classification rules |

### Rule Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | `str` | ✅ | Human-readable rule name (used in logs and reports) |
| `destination` | `str` | ✅ | Path relative to `output_directory`. Supports `{YYYY}`, `{MM}`, `{DD}` |
| `extensions` | `list[str]` | ❌ | File extensions to match (include the dot: `.pdf`) |
| `keywords` | `list[str]` | ❌ | Substrings to match in the filename (case-insensitive) |
| `age_days` | `int` | ❌ | Minimum file age in days. File must be at least this old |

---

## 🔁 Rule Matching Logic

Rules are evaluated **in order**. The first rule that matches wins.

```
                    ┌─────────────────────────┐
                    │   For each rule in       │
                    │   config (top to bottom) │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Rule has extensions?   │
                    └────────────┬────────────┘
                          Yes    │    No (skip check)
                    ┌────────────▼────────────┐
                    │  File extension match?  │
                    └────────────┬────────────┘
                        Match    │    No match → next rule
                    ┌────────────▼────────────┐
                    │  Rule has keywords?     │
                    └────────────┬────────────┘
                          Yes    │    No (skip check)
                    ┌────────────▼────────────┐
                    │  Keyword in filename?   │
                    └────────────┬────────────┘
                        Match    │    No match → next rule
                    ┌────────────▼────────────┐
                    │  Rule has age_days?     │
                    └────────────┬────────────┘
                          Yes    │    No (skip check)
                    ┌────────────▼────────────┐
                    │  File old enough?       │
                    └────────────┬────────────┘
                        Match    │    No match → next rule
                    ┌────────────▼────────────┐
                    │  ✅ RULE MATCHED         │
                    │  Resolve destination    │
                    │  {YYYY}/{MM}/{DD} →     │
                    │  file's mtime           │
                    └─────────────────────────┘

  If no rule matches → file is SKIPPED (not moved, logged as unmatched)
```

**Tip:** Put specific rules (with keywords) **before** generic ones (extension only). The `Invoice PDFs` rule must come before `PDF Documents` or invoice files will be caught by the generic rule first.

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=smartvault

# Run with detailed coverage (shows uncovered lines)
pytest tests/ --cov=smartvault --cov-report=term-missing

# Run a specific test file
pytest tests/test_rules_engine.py -v

# Run a specific test
pytest tests/test_organizer.py::test_organize_file_dry_run -v
```

### Test Coverage

| Module | Tests |
|---|---|
| `organizer.py` | dry-run validation, file move, result field integrity |
| `duplicate_finder.py` | hash consistency, identical file detection, empty directory |
| `rules_engine.py` | extension match, keyword priority, date token resolution, no-match fallback |

---

## 📊 Sample Report

After running `python main.py scan ~/Downloads --report`, open the generated HTML report:

```
╔══════════════════════════════════════════════════════════════════╗
║                    🗄  SmartVault Report                        ║
║              Run: 2026-03-08 22:30:41  │  Duration: 2.1s        ║
╠══════════╦═══════════╦═══════════╦═════════════════════════════╣
║  📁 247  ║  ✅ 241   ║  ⏭  6    ║  ❌ 0                       ║
║ Processed║  Moved    ║  Skipped  ║  Errors                     ║
╠══════════╩═══════════╩═══════════╩═════════════════════════════╣
║  🔍 Duplicates: 12 groups │ 28 files │ 847 MB wasted           ║
╠══════════════════════════════════════════════════════════════════╣
║ Source                     │ Destination           │ Status     ║
╠══════════════════════════════════════════════════════════════════╣
║ resume.pdf                 │ Documents/PDFs        │ ✅ moved   ║
║ Image_fx (1).jpg           │ Media/Images/2025/06  │ ✅ moved   ║
║ manucouture demo.mp4       │ Media/Videos/2025     │ ✅ moved   ║
║ learnmate-backend.zip      │ Archives              │ ✅ moved   ║
║ main.py                    │ Code                  │ ✅ moved   ║
║ ...                        │ ...                   │ ...        ║
╚══════════════════════════════════════════════════════════════════╝
```

The actual report is a full dark-themed HTML page with color-coded rows, statistics cards, and a complete file-by-file results table. A companion `.csv` is generated alongside it for spreadsheet analysis.

---

## 🗺️ Roadmap

- [ ] 🖥️ **Web Dashboard** — live browser UI showing watcher activity and stats in real-time
- [ ] ☁️ **Cloud Sync** — push organized files to S3, Google Drive, or Dropbox
- [ ] 🤖 **AI Classification** — use an LLM to classify files with no extension or ambiguous names
- [ ] 🔒 **Encrypted Rules** — protect sensitive rule configurations with AES encryption
- [ ] 🧩 **Plugin System** — drop-in Python modules for custom classification logic
- [ ] 📱 **Desktop Notifications** — OS-level alerts when files are moved or duplicates found
- [ ] 📦 **PyPI Package** — `pip install smartvault` + global CLI command
- [ ] 🗃️ **SQLite Audit Log** — persistent database of every file operation for compliance use cases

---

## 🤝 Contributing

Contributions are welcome and appreciated. Here's how to get started:

```bash
# Fork the repo and clone your fork
git clone https://github.com/yourusername/smartvault.git
cd smartvault

# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes, then run tests
pytest tests/ --cov=smartvault

# Commit with a conventional commit message
git commit -m "feat: add support for MIME type detection"

# Push and open a pull request
git push origin feature/your-feature-name
```

**Guidelines:**
- All new code must include type hints and Google-style docstrings
- All new features must include corresponding tests
- Run `black .` before committing to maintain code style
- Keep `dry_run` respected in any new write operations

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built with 🐍 Python · Designed for developers who value clean systems

**[⬆ Back to top](#)**

</div>
