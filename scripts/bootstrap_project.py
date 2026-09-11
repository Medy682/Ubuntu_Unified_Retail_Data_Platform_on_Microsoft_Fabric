from pathlib import Path

# Root project folder
PROJECT_NAME = "retail_data_platform_on_Microsoft_Azure"

# Folder structure
folders = [
    ".github/workflows",
    "infrastructure/terraform",
    "infrastructure/architecture",

    "data/batch",
    "data/streaming",
    "data/reference",

    "ingestion/connectors",
    "ingestion/loaders",
    "ingestion/config",

    "orchestration/dags",

    "processing/bronze",
    "processing/silver",
    "processing/gold",
    "processing/common",

    "dbt/models",
    "dbt/macros",
    "dbt/tests",
    "dbt/seeds",
    "dbt/snapshots",

    "warehouse",

    "dashboards",

    "monitoring",

    "tests/unit",
    "tests/integration",
    "tests/data_quality",
    "tests/performance",

    "docs/architecture",
    "docs/diagrams",
    "docs/runbooks",
    "docs/images",

    "docker",

    "config",

    "scripts"
]

# Files to create
files = [
    ".env.example",
    ".gitignore",
    "README.md",
    "requirements.txt",
    "docker-compose.yml",
    "Makefile",

    ".github/workflows/ci.yml",
    ".github/workflows/cd.yml",
    ".github/workflows/dbt_tests.yml",
    ".github/workflows/security_scan.yml",

    "dbt/dbt_project.yml",
]

root = Path(PROJECT_NAME)

# Create folders
for folder in folders:
    (root / folder).mkdir(parents=True, exist_ok=True)

# Create files
for file in files:
    file_path = root / file
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.touch()

print(f"\n✅ Repository '{PROJECT_NAME}' created successfully!")