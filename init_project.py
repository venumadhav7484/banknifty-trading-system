import os

folders = [
    "backtrader",
    "data/dummy_data",
    "reports/benchmarks",
    "reports/dashboards",
    "logs/error_logs",
    "tests",
    "config/asset_configs",
    "scripts",
    "docs",
    ".github/workflows"
]

files = [
    "backtrader/__init__.py",
    "data/__init__.py",
    "reports/generate_reports.py",
    "scripts/run_backtest.py",
    "config/banknifty_config.yaml",
    "requirements.txt",
    "README.md",
    "dockerfile",
    "setup.sh",
    ".gitignore",
    ".github/workflows/ci.yml",
    "docs/strategy_playbook.md"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create empty files
for file in files:
    with open(file, 'w') as f:
        f.write("")

print("✅ Project structure initialized!")
