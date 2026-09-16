from pathlib import Path


# ============================================================
# Project configuration
# ============================================================

PROJECT_NAME = "Ubuntu_Unified_Retail_Data_Platform_on_Microsoft_fabric"


# ============================================================
# Folder structure
# ============================================================

folders = [
    # GitHub
    ".github/workflows",

    # Project architecture
    "architecture",

    # Data
    "data/Original_data",

    # Docker
    "docker",

    # Microsoft Fabric
    "fabric/data_factory",
    "fabric/lakehouse",
    "fabric/notebooks",
    "fabric/power_bi",
    "fabric/warehouse",

    # Documentation
    "docs",

    # Scripts
    "scripts",

    # Testing
    "tests",

    # Logs
    "logs",
]


# ============================================================
# Files to create
# ============================================================

files = [
    # GitHub Actions
    ".github/workflows/platform-ci.yml",

    # Docker
    "docker/Dockerfile",
    "docker/docker-compose.yml",
    "docker/entrypoint.sh",

    # Project configuration
    ".dockerignore",
    ".gitignore",
    "LICENSE",
    "Makefile",
    "README.md",
    "requirements.txt",

    # Scripts
    "scripts/event_simulator.py",
    "scripts/generate_sample_datasets.py",
    "scripts/generate_reference_data.py",
    "scripts/utilities.py",
]


# ============================================================
# Create project root
# ============================================================

root = Path(PROJECT_NAME)


# ============================================================
# Create folders
# ============================================================

for folder in folders:
    (root / folder).mkdir(parents=True, exist_ok=True)


# ============================================================
# Create files
# ============================================================

for file in files:
    file_path = root / file
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Do not overwrite existing files
    if not file_path.exists():
        file_path.touch()


# ============================================================
# Completion message
# ============================================================

print("\n" + "=" * 60)
print("✅ Ubuntu Unified Retail Data Platform created successfully!")
print("=" * 60)
print(f"📁 Project directory: {root.resolve()}")