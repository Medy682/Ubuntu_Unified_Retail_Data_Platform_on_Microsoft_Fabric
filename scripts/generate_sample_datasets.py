"""
generate_sample_datasets.py

Build realistic batch, reference, and streaming data sources.
Prepare relationship-preserving sample datasets for the modern retail 
Data platform on Microsoft Fabric.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
import pandas as pd

# =============================================================================
# 📌 1st PART:
# ==============================================================================

# ==============================================================================
# Configuration (project_paths)
# ==============================================================================

# Project root (navigates up from scripts/ to the platform directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
ORIGINAL_DATA_DIR = DATA_DIR / "original_data"
BATCH_DATA_DIR = DATA_DIR / "batch"

LOGS_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOGS_DIR / "generate_sample_datasets.log"

# --------------------------------------------------------------------------
# Input datasets (Raw production sources)
# --------------------------------------------------------------------------
INPUT_FILES = {
    "online_retail": "online_retail_ii.csv",
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
}

# ==============================================================================
# Expected Schemas
# ==============================================================================
EXPECTED_COLUMNS = {
    "online_retail": [
        "Invoice", "StockCode", "Description", "Quantity", 
        "InvoiceDate", "Price", "Customer ID", "Country"
    ],
    "customers": [
        "customer_id", "customer_unique_id", "customer_zip_code_prefix", 
        "customer_city", "customer_state"
    ],
    "orders": [
        "order_id", "customer_id", "order_status", "order_purchase_timestamp", 
        "order_approved_at", "order_delivered_carrier_date", 
        "order_delivered_customer_date", "order_estimated_delivery_date"
    ],
    "order_items": [
        "order_id", "order_item_id", "product_id", "seller_id", 
        "shipping_limit_date", "price", "freight_value"
    ],
    "payments": [
        "order_id", "payment_sequential", "payment_type", 
        "payment_installments", "payment_value"
    ],
    "reviews": [
        "review_id", "order_id", "review_score", "review_comment_title", 
        "review_comment_message", "review_creation_date", "review_answer_timestamp"
    ],
    "products": [
        "product_id", "product_category_name", "product_name_lenght", 
        "product_description_lenght", "product_photos_qty", "product_weight_g", 
        "product_length_cm", "product_height_cm", "product_width_cm"
    ],
    "sellers": [
        "seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"
    ],
}

# ==============================================================================
# Output Files (Simplified names for development batch folder)
# ==============================================================================
OUTPUT_FILES = {
    "online_retail": "pos_sales_transactions.csv",
    "customers": "customers.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "payments": "payments.csv",
    "reviews": "reviews.csv",
    "products": "products.csv",
    "sellers": "sellers.csv",
}

# --------------------------------------------------------------------------
# Downsampling target configuration limits for Part 2
# --------------------------------------------------------------------------
TARGET_ROW_COUNTS = {
    "online_retail": 75_000,
    "customers": 10_000,
    "orders": 20_000,
    "order_items": 40_000,
    "payments": 20_000,
    "reviews": 20_000,
    "products": 15_842,
    "sellers": 2_517,
}

RANDOM_SEED = 42

# ==============================================================================
# Logger Setup
# ==============================================================================
def configure_logger() -> logging.Logger:
    """
    Configure the application logger. 
    Logs are written to both: Console and logs/generate_sample_datasets.log
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Using a distinct local variable name to prevent confusion with the global scope
    local_log = logging.getLogger("generate_sample_datasets")
    
    if local_log.handlers:
        return local_log

    local_log.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # File Handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    local_log.addHandler(console_handler)
    local_log.addHandler(file_handler)

    return local_log

# Call the function and assign it to the clean global variable
logger = configure_logger()

# ==============================================================================
# Validation
# ==============================================================================
def validate_input_directory() -> None:
    """Validate that the original data directory exists."""
    if not ORIGINAL_DATA_DIR.exists():
        raise FileNotFoundError(f"Input directory not found:\n{ORIGINAL_DATA_DIR}")

def validate_required_files() -> None:
    """Ensure all raw production source CSV files exist on disk."""
    logger.info("Validating input datasets...")
    missing_files = []
    
    for filename in INPUT_FILES.values():
        file_path = ORIGINAL_DATA_DIR / filename
        if not file_path.exists():
            missing_files.append(filename)

    if missing_files:
        logger.error("Missing required files:")
        for file in missing_files:
            logger.error("   %s", file)
        raise FileNotFoundError("One or more required datasets are missing.")
        
    logger.info("All required datasets found.")

def validate_schema(dataset_name: str, dataframe: pd.DataFrame) -> None:
    """Validate that the dataset contains all expected columns."""
    expected = set(EXPECTED_COLUMNS[dataset_name])
    actual = set(dataframe.columns)
    missing = expected - actual

    if missing:
        raise ValueError(f"{dataset_name} is missing columns: {sorted(missing)}")

def create_output_directory() -> None:
    """Create batch output directory if it does not exist."""
    BATCH_DATA_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("Output directory ready: %s", BATCH_DATA_DIR)

# ==============================================================================
# Reading datasets
# ==============================================================================
def load_dataset(dataset_name: str, file_name: str) -> pd.DataFrame:
    """Read and validate a raw CSV dataset from disk."""
    file_path = ORIGINAL_DATA_DIR / file_name
    
    # Chronological logic fix: Read first, then log factual success
    df = pd.read_csv(file_path)
    logger.info("Successfully read file from disk: '%s'", file_name)

    validate_schema(dataset_name, df)

    if df.empty:
        raise ValueError(f"{file_name} contains no records.")

    logger.info("Loaded Dataset : %s", dataset_name)
    logger.info(f"Rows           : {len(df):,}")
    logger.info("Columns        : %d", len(df.columns))

    return df

def load_all_datasets() -> dict[str, pd.DataFrame]:
    """Load every required raw source dataset into memory."""
    datasets = {}
    for dataset_name, filename in INPUT_FILES.items():
        datasets[dataset_name] = load_dataset(dataset_name, filename)
        
    logger.info("Successfully completed loading process for all raw source systems.")
    return datasets

# ==============================================================================
# Temporary Main logic
# ==============================================================================
""" 
def main() -> None:
    Entry point
    SEPARATOR = "=" * 60
    logger.info("Batch Data Preparation")
    logger.info(SEPARATOR)
    
    validate_input_directory()
    validate_required_files()
    create_output_directory()
    
    datasets = load_all_datasets()
    
    logger.info(SEPARATOR)
    logger.info("Datasets Loaded Successfully")
    logger.info(SEPARATOR)

    for name, df in datasets.items():
     logger.info(
        f"{name:<15} Rows: {len(df):,} | Columns: {len(df.columns)}"
    )

        
    logger.info(SEPARATOR)
    logger.info("Part 1 completed successfully.")
    logger.info(SEPARATOR)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception(
            "Batch data preparation failed due to an unexpected error."
        )
        raise
"""

# =============================================================================
# 📌 2nd PART:
# ==============================================================================
# PART 2 — RELATIONSHIP-PRESERVING SAMPLING ENGINE (CORE LOGIC)
# ==============================================================================

def sample_pos_transactions(df_pos: pd.DataFrame, target_size: int) -> pd.DataFrame:
    """
    Sample POS Transactions independently to the configured target size.
    """
    logger.info("Executing POS Transactions sampling engine...")
    
    if len(df_pos) <= target_size:
        logger.warning(
            "POS source rows (%s) <= target size (%s). Copying full dataset.", 
            f"{len(df_pos):,}", f"{target_size:,}"
        )
        return df_pos.copy()
        
    df_sampled = df_pos.sample(n=target_size, random_state=RANDOM_SEED)
    logger.info("Successfully downsampled POS Transactions to %s rows.", f"{len(df_sampled):,}")
    return df_sampled


def sample_ecommerce_ecosystem(datasets: dict[str, pd.DataFrame], targets: dict[str, int]) -> dict[str, pd.DataFrame]:
    """
    Downsample the relational e-commerce ecosystem while strictly preserving 
    referential integrity using an unbreakable cascading filter hierarchy.
    """
    logger.info("Initializing relationship-preserving downsampling for Olist ecosystem...")
    sampled = {}

    # 1. Anchor Step: Core Customers Sampling
    df_c = datasets["customers"]
    c_target = targets["customers"]
    logger.info("Sampling core anchor: Customers (Target: %s rows)...", f"{c_target:,}")
    
    if len(df_c) <= c_target:
        sampled["customers"] = df_c.copy()
    else:
        sampled["customers"] = df_c.sample(n=c_target, random_state=RANDOM_SEED)
        
    sampled_customer_ids = set(sampled["customers"]["customer_id"])

      # 2. Relational Cascade: Filter Orders linked to Sampled Customers AND ensure they have items
    df_o = datasets["orders"]
    df_oi_raw = datasets["order_items"]
    o_target = targets["orders"]
    
    # Pre-filter out any ghost orders from the raw source that don't have matching line items
    valid_order_ids_with_items = set(df_oi_raw["order_id"])
    df_o_valid = df_o[df_o["order_id"].isin(valid_order_ids_with_items)]
    
    # Now filter by our downsampled customers
    df_o_filtered = df_o_valid[df_o_valid["customer_id"].isin(sampled_customer_ids)]
    
    # Keep your existing logs and downsampling logic below intact:
    logger.info(f"Filtering Orders tied to sampled customers (Found: {len(df_o_filtered):,})...")
    
    # Downsample orders if they exceed the target boundary limit
    if len(df_o_filtered) > o_target:
        sampled["orders"] = df_o_filtered.sample(n=o_target, random_state=RANDOM_SEED)
    else:
        logger.warning(f"Linked Orders count ({len(df_o_filtered):,}) is below target limit ({o_target:,}).")
        sampled["orders"] = df_o_filtered.copy()
        
    sampled_order_ids = set(sampled["orders"]["order_id"])


    # 3. Structural Cascade: Keep ALL children matching the remaining sample orders
    # Note: We do NOT randomly downsample child records to prevent broken orphan keys.
    
    # Order Items
    df_oi = datasets["order_items"]
    sampled["order_items"] = df_oi[df_oi["order_id"].isin(sampled_order_ids)].copy()
    logger.info("Retained companion Order Items to preserve integrity (Count: %s)", f"{len(sampled['order_items']):,}")

    # Payments
    df_p = datasets["payments"]
    sampled["payments"] = df_p[df_p["order_id"].isin(sampled_order_ids)].copy()
    logger.info("Retained companion Payments to preserve integrity (Count: %s)", f"{len(sampled['payments']):,}")

    # Reviews
    df_r = datasets["reviews"]
    sampled["reviews"] = df_r[df_r["order_id"].isin(sampled_order_ids)].copy()
    logger.info("Retained companion Reviews to preserve integrity (Count: %s)", f"{len(sampled['reviews']):,}")

    # 4. Master Data Slicing: Filter Catalog Items referenced by surviving transactions
    
    # Products Catalog
    referenced_products = set(sampled["order_items"]["product_id"])
    df_prod = datasets["products"]
    sampled["products"] = df_prod[df_prod["product_id"].isin(referenced_products)].copy()
    logger.info("Filtered Products Catalog to active records only (Count: %s)", f"{len(sampled['products']):,}")

    # Sellers Catalog
    referenced_sellers = set(sampled["order_items"]["seller_id"])
    df_sel = datasets["sellers"]
    sampled["sellers"] = df_sel[df_sel["seller_id"].isin(referenced_sellers)].copy()
    logger.info("Filtered Sellers Catalog to active records only (Count: %s)", f"{len(sampled['sellers']):,}")

    return sampled


def validate_data_consistency(sampled_ecosystem: dict[str, pd.DataFrame], df_pos: pd.DataFrame) -> bool:
    """
    Perform programatic validation checks verifying zero duplicate primary keys, 
    no orphaned downstream records, and non-empty outputs.
    """
    logger.info("Executing relational data integrity validation routines...")
    integrity_passed = True

    # Check for empty operational datasets
    if df_pos.empty:
        logger.error("Data Consistency Failure: Sampled POS Transactions dataset is empty.")
        integrity_passed = False
        
    for name, df in sampled_ecosystem.items():
        if df.empty:
            logger.error("Data Consistency Failure: Sampled dataset '%s' contains 0 records.", name)
            integrity_passed = False

    # Check for duplicate Primary Keys
    pk_map = {
        "customers": "customer_id",
        "orders": "order_id",
        "products": "product_id",
        "sellers": "seller_id"
    }
    for name, pk in pk_map.items():
        df = sampled_ecosystem.get(name)
        if df is not None and df[pk].duplicated().any():
            duplicate_count = df[pk].duplicated().sum()
            logger.error("Data Integrity Error: Found %s duplicate Primary Keys in '%s'.", f"{duplicate_count:,}", name)
            integrity_passed = False

    # Complete Referential Integrity Check (Parent-to-Child & Child-to-Parent verification)
    df_orders = sampled_ecosystem["orders"]
    df_items = sampled_ecosystem["order_items"]
    df_payments = sampled_ecosystem["payments"]
    df_reviews = sampled_ecosystem["reviews"]

    # Check: Items point to real Orders
    orphaned_items = df_items[~df_items["order_id"].isin(df_orders["order_id"])]
    if not orphaned_items.empty:
        logger.error("Referential Integrity Failure: %s Order Items are missing parent Orders.", f"{len(orphaned_items):,}")
        integrity_passed = False

    # Check: Payments point to real Orders
    orphaned_payments = df_payments[~df_payments["order_id"].isin(df_orders["order_id"])]
    if not orphaned_payments.empty:
        logger.error("Referential Integrity Failure: %s Payments are missing parent Orders.", f"{len(orphaned_payments):,}")
        integrity_passed = False

    # Check: Orders have at least one Item (Ensures no ghost transactions)
    ghost_orders = df_orders[~df_orders["order_id"].isin(df_items["order_id"])]
    if not ghost_orders.empty:
        logger.error("Business Logic Failure: Found %s Orders containing 0 items.", f"{len(ghost_orders):,}")
        integrity_passed = False

    if integrity_passed:
        logger.info("Referential and relational data consistency checks passed successfully.")
    else:
        logger.warning("Relational violations discovered. Review targeted structure exceptions listed above.")
        
    return integrity_passed


# ==============================================================================
# PART 3 — EXPORT, REPORTING & FINAL ORCHESTRATION
# ==============================================================================

def export_and_report(sampled_ecosystem: dict[str, pd.DataFrame], df_pos: pd.DataFrame) -> None:
    """
    Write processed components down to /data/batch/ and output execution matrices.
    """
    logger.info("Writing cleaned sample layers down to target batch directory...")
    
    # Save POS Data Layer
    pos_destination = BATCH_DATA_DIR / OUTPUT_FILES["online_retail"]
    df_pos.to_csv(pos_destination, index=False)
    logger.info("Successfully saved POS Data Layer to: %s", pos_destination.name)

    # Save Remaining Ecosystem
    for key, df in sampled_ecosystem.items():
        destination_path = BATCH_DATA_DIR / OUTPUT_FILES[key]
        df.to_csv(destination_path, index=False)
        logger.info("Successfully saved relational layer to: %s", destination_path.name)

    # Standard Output Structural Terminal Console Panel Reporting
    SEPARATOR = "-" * 40
    print("\n" + "=" * 40)
    print(f"{'Dataset':<26} {'Rows':<10}")
    print(SEPARATOR)
    print(f"{'Customers':<26} {len(sampled_ecosystem['customers']):,}")
    print(f"{'Orders':<26} {len(sampled_ecosystem['orders']):,}")
    print(f"{'Order Items':<26} {len(sampled_ecosystem['order_items']):,}")
    print(f"{'Payments':<26} {len(sampled_ecosystem['payments']):,}")
    print(f"{'Reviews':<26} {len(sampled_ecosystem['reviews']):,}")
    print(f"{'Products':<26} {len(sampled_ecosystem['products']):,}")
    print(f"{'Sellers':<26} {len(sampled_ecosystem['sellers']):,}")
    print(f"{'POS Transactions':<26} {len(df_pos):,}")
    print(SEPARATOR)
    print("All foreign keys validated.")
    print("Sample datasets successfully created.")
    print("=" * 40 + "\n")


# ==============================================================================
# PART 3 — FINAL PRODUCTION ORCHESTRATION 
# ==============================================================================
# ==============================================================================
# MAIN ENGINE ORCHESTRATION WORKFLOW OR FINAL ORCHESTRATION
# ==============================================================================

def main() -> None:
    """
    3. Final Orchestration: Complete production end-to-end pipeline execution workflow.
    Replaces temporary main() loops to fully execute disk validations, downsampling,
    referential integrity constraint checks, and target directory file writes.
    """
    HEADER_SEPARATOR = "=" * 60
    logger.info("Batch Data Preparation Engine Initializing")
    logger.info(HEADER_SEPARATOR)
    
    # Step 1: Disk Layout & Directory Validations (Part 1)
    validate_input_directory()
    validate_required_files()
    create_output_directory()
    
    # Step 2: Load Raw Production Dataframes into Memory (Part 1)
    datasets = load_all_datasets()
    
    logger.info(HEADER_SEPARATOR)
    logger.info("Datasets Loaded Safely into System Memory")
    logger.info(HEADER_SEPARATOR)
    
    # Isolate online_retail (POS) data from the relational ecosystem dictionary
    df_pos_raw = datasets.pop("online_retail")
    
    # Step 3: Execute Core Cascading Sampling Logic (Part 2)
    df_pos_sampled = sample_pos_transactions(
        df_pos=df_pos_raw, 
        target_size=TARGET_ROW_COUNTS["online_retail"]
    )
    
    sampled_ecosystem = sample_ecommerce_ecosystem(
        datasets=datasets, 
        targets=TARGET_ROW_COUNTS
    )
    
    # Step 4: Perform Relational Integrity Checks (Part 2)
    integrity_passed = validate_data_consistency(
        sampled_ecosystem=sampled_ecosystem, 
        df_pos=df_pos_sampled
    )
    
    if not integrity_passed:
        raise ValueError("Data integrity checks failed. Aborting target file export.")
        
    # Step 5: Export Samples & Print Console Table Summary (Part 3)
    export_and_report(
        sampled_ecosystem=sampled_ecosystem, 
        df_pos=df_pos_sampled
    )
    
    logger.info(HEADER_SEPARATOR)
    logger.info("Pipeline processing completed successfully. All layers exported.")
    logger.info(HEADER_SEPARATOR)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Batch data preparation failed due to an unexpected error.")
        sys.exit(1)

