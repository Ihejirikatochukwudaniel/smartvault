# ███████╗███╗   ███╗ █████╗ ██████╗ ███████╗██████╗ ██╗   ██╗
# ██╔════╝████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔══██╗╚██╗ ██╔╝
# █████╗  ██╔████╔██║███████║██████╔╝█████╗  ██████╔╝ ╚████╔╝ 
# ██╔══╝  ██║╚██╔╝██║██╔══██║██╔══██╗██╔══╝  ██╔══██╗  ╚██╔╝  
# ██║     ██║ ╚═╝ ██║██║  ██║██║  ██║███████╗██║  ██║   ██║   
# ╚═╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![code style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![tests](https://img.shields.io/badge/tests-passing-brightgreen)](#)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-orange)](#)

SmartVault is an intelligent file organization system that automatically
watches directories, classifies files using configurable rules, handles
duplicates, and generates detailed reports.

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Usage](#usage)
5. [How It Works](#how-it-works)
6. [Configuration](#configuration)
7. [Rule Matching Logic](#rule-matching-logic)
8. [Running Tests](#running-tests)
9. [Sample Report](#sample-report)
10. [Roadmap](#roadmap)
11. [Contributing](#contributing)
12. [License](#license)

## ✨ Features

- 🗂️ Watch a directory and automatically organize new files
- 🧠 Rule-based classification with extensions, keywords, and age
- 🔍 Detect and handle duplicate files with hashing
- 📄 Generate HTML and CSV reports with stats and results
- ⚙️ Fully configurable via `config.yaml` with dynamic paths
- 🔁 Dry-run mode for safe simulation

## 🏗️ Project Structure

```
SmartVault/
├── main.py
├── config.yaml
├── requirements.txt
├── README.md
├── .gitignore
├── smartvault/
│   ├── __init__.py
│   ├── watcher.py
│   ├── organizer.py
│   ├── duplicate_finder.py
│   ├── rules_engine.py
│   ├── reporter.py
│   └── logger.py
├── templates/
│   └── report.html.j2
├── logs/
│   └── .gitkeep
├── reports/
│   └── .gitkeep
└── tests/
    ├── __init__.py
    ├── test_organizer.py
    ├── test_duplicate_finder.py
    └── test_rules_engine.py
```

*(annotations omitted for brevity)*

## ⚙️ Installation

```bash
git clone <repo-url> smartvault
cd smartvault
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 🚀 Usage

```bash
python main.py watch ~/Downloads
python main.py scan ~/Downloads --recursive --report
python main.py dupes ~/Downloads --action delete
python main.py report --last
```

Each command supports `--dry-run` and custom `--config`.

## 🗂️ How It Works

```text
File Created → Watcher → Rules Engine → Organizer → Reporter
```

## 📋 Configuration

| Field             | Type   | Default                 | Description                        |
|-------------------|--------|-------------------------|------------------------------------|
| watch_directory   | str    | `~/Downloads`           | Directory to monitor              |
| output_directory  | str    | `~/SmartVault/Organized`| Destination root for organized files|
| dry_run           | bool   | false                   | Simulate actions only              |
| duplicate_action  | str    | report                  | `report`/`delete`/`move`           |
| log_level         | str    | INFO                    | Logging level                      |
| log_max_bytes     | int    | 5242880                 | Max size for log rotation          |
| log_backup_count  | int    | 3                       | Rotated file count                 |
| rules             | list   | []                      | Rule definitions                   |

## 🔁 Rule Matching Logic

```
[extension] → [keyword] → [age]
```

## 🧪 Running Tests

```bash
pytest tests/ --cov=smartvault
```

## 📊 Sample Report

```
[SmartVault Report mockup]
... (ASCII art or description of layout)
```

## 🗺️ Roadmap

- 🔒 Support encryption for stored rules
- ☁️ Cloud synchronization
- 🧩 Plugin system for custom rules

## 🤝 Contributing

Contributions are welcome! Please open issues or pull requests.

## 📄 License

MIT License
