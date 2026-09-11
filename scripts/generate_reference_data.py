"""
generate_reference_data.py
Generate realistic master reference and dimension files for the Modern retail Data platform.
Maintains relational integrity with seeds and saves outputs directly to /data/reference/.
"""

from __future__ import annotations
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import pandas as pd

# ==============================================================================
# CONFIGURATION & PROJECT PATHS
# ==============================================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BATCH_DATA_DIR = DATA_DIR / "batch"
REFERENCE_DATA_DIR = DATA_DIR / "reference"
LOGS_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOGS_DIR / "generate_reference_data.log"

# Target Row Count Boundaries for Core Dimensions
REF_COUNTS = {
    "stores": 50,
    "suppliers": 250,
    "employees": 150,
    "promotions": 30,
    # Note: inventory_snapshots is calculated dynamically below: 
    # (3 Days * 10 Stores * 50 Products) = 1,500 rows.
}

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# ==============================================================================
# LOGGER INITIALIZATION
# ==============================================================================
def configure_logger() -> logging.Logger:
    """Configure reference script local logging engine."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    local_log = logging.getLogger("generate_reference_data")
    if local_log.handlers:
        return local_log
    local_log.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    local_log.addHandler(console_handler)
    local_log.addHandler(file_handler)
    return local_log

logger = configure_logger()

# ==============================================================================
# REFERENCE GENERATION MODULES
# ==============================================================================

def generate_stores() -> pd.DataFrame:
    """Generate master store dimensions map."""
    logger.info("Generating master Stores reference layer...")
    n = REF_COUNTS["stores"]
    
    cities = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Brasília", "Salvador", "Curitiba"]
    regions = ["Southeast", "Southeast", "Southeast", "Central-West", "Northeast", "South"]
    types = ["Flagship", "Standard", "Express", "Mall-Type"]
    
    store_ids = [f"STR_{i:03d}" for i in range(1, n + 1)]
    chosen_indices = np.random.choice(len(cities), size=n)
    
    data = {
        "store_id": store_ids,
        "store_name": [f"Retail Hub {city} #{i}" for i, city in enumerate(np.array(cities)[chosen_indices], 1)],
        "store_type": np.random.choice(types, size=n, p=[0.1, 0.5, 0.3, 0.1]),
        "city": np.array(cities)[chosen_indices],
        "region": np.array(regions)[chosen_indices],
        "is_active": np.random.choice([True, False], size=n, p=[0.94, 0.06])
    }
    return pd.DataFrame(data)


def generate_suppliers() -> pd.DataFrame:
    """Generate vendor and manufacturing supplier attributes mapping."""
    logger.info("Generating corporate Suppliers dimension map...")
    n = REF_COUNTS["suppliers"]
    
    categories = ["Electronics", "Fashion", "Home & Living", "Health & Beauty", "Automotive", "Toys"]
    segments = ["Tier 1 - Strategic", "Tier 2 - Preferred", "Tier 3 - Standard"]
    
    supplier_ids = [f"SUP_{i:04d}" for i in range(1, n + 1)]
    
    data = {
        "supplier_id": supplier_ids,
        "supplier_name": [f"Global Alpha Corp {i:03d}" for i in range(1, n + 1)],
        "primary_category": np.random.choice(categories, size=n),
        "supplier_tier": np.random.choice(segments, size=n, p=[0.15, 0.45, 0.40]),
        "country": np.random.choice(["Brazil", "United States", "China", "Germany"], size=n, p=[0.7, 0.1, 0.1, 0.1])
    }
    return pd.DataFrame(data)


def generate_employees(df_stores: pd.DataFrame) -> pd.DataFrame:
    """Generate corporate employee positions mapped deterministically to valid stores."""
    logger.info("Generating internal corporate Employees registry map...")
    n = REF_COUNTS["employees"]
    
    departments = ["Sales", "Operations", "Inventory", "Management"]
    titles = ["Associate", "Specialist", "Supervisor", "Store Manager"]
    
    emp_ids = [f"EMP_{i:05d}" for i in range(1, n + 1)]
    assigned_store_ids = np.random.choice(df_stores["store_id"], size=n)
    
    data = {
        "employee_id": emp_ids,
        "first_name": [f"Staff_{i}" for i in range(1, n + 1)],
        "last_name": [f"LN_{i}" for i in range(1, n + 1)],
        "department": np.random.choice(departments, size=n, p=[0.6, 0.2, 0.1, 0.1]),
        "job_title": np.random.choice(titles, size=n, p=[0.5, 0.3, 0.1, 0.1]),
        "store_id": assigned_store_ids,
        "hire_date": [datetime(2021, 1, 1) + timedelta(days=int(np.random.randint(0, 1200))) for _ in range(n)]
    }
    return pd.DataFrame(data)


def generate_promotions() -> pd.DataFrame:
    """Generate markdown campaign strategies mappings."""
    logger.info("Generating marketing Campaigns & Promotions map...")
    n = REF_COUNTS["promotions"]
    
    channels = ["Email Blast", "In-Store Banner", "Social Media", "Push Notification"]
    
    promo_ids = [f"PRM_{i:03d}" for i in range(1, n + 1)]
    
    data = {
        "promotion_id": promo_ids,
        "campaign_name": [f"Seasonal Boost Wave {i}" for i in range(1, n + 1)],
        "discount_percentage": np.random.choice([0.05, 0.10, 0.15, 0.20, 0.30], size=n, p=[0.2, 0.4, 0.2, 0.1, 0.1]),
        "marketing_channel": np.random.choice(channels, size=n),
        "is_stackable": np.random.choice([False, True], size=n, p=[0.85, 0.15])
    }
    return pd.DataFrame(data)



def generate_inventory_snapshots(df_stores: pd.DataFrame) -> pd.DataFrame:
    """
    Generate chronological inventory stock status tracking tables.
    Preserves structural ties against valid active Products and target operational Stores.
    
    Scaled down for lightweight local processing (~1,500 total rows).
    """
    logger.info("Generating continuous timeline Inventory Snapshots transactional records...")

    # Safely look up product catalog created inside your batch processing folder
    products_path = BATCH_DATA_DIR / "products.csv"
    if not products_path.exists():
        raise FileNotFoundError(
            f"Missing core products file dependency at: {products_path.name}\n"
            f"Execute generate_sample_datasets.py first."
        )
        
    df_products = pd.read_csv(products_path)
    product_ids = df_products["product_id"].unique()
    store_ids = df_stores["store_id"].unique()

    # Construct a historical snapshot baseline tracking loop for a 3-day history log
    snapshot_dates = [datetime(2026, 8, 8), datetime(2026, 8, 9), datetime(2026, 8, 10)]
    records = []

    # Downsize sample pools to keep the local dataset lightweight and fast
    sampled_product_subset = np.random.choice(product_ids, size=min(50, len(product_ids)), replace=False)
    sampled_store_subset = np.random.choice(store_ids, size=min(10, len(store_ids)), replace=False)

    # Math: 3 dates * 10 stores * 50 products = 1,500 loops
    for date in snapshot_dates:
        for store in sampled_store_subset:
            for product in sampled_product_subset:
                stock_on_hand = int(np.random.randint(0, 150))
                safety_stock = 15
                
                records.append({
                    "snapshot_date": date.strftime("%Y-%m-%d"),
                    "store_id": store,
                    "product_id": product,
                    "stock_on_hand": stock_on_hand,
                    "safety_stock_level": safety_stock,
                    "stock_status": "Out of Stock" if stock_on_hand == 0 else (
                        "Reorder Alert" if stock_on_hand < safety_stock else "Healthy Bucket"
                    )
                })

    return pd.DataFrame(records)

# ==============================================================================
# PIPELINE EXPORT AND ORCHESTRATION 
# ==============================================================================

def export_reference_layers(outputs: dict[str, pd.DataFrame]) -> None:
    """Export reference assets directly into target directory paths."""
    REFERENCE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Target reference directory verified: {REFERENCE_DATA_DIR}")
    
    for filename, df in outputs.items():
        destination = REFERENCE_DATA_DIR / f"{filename}.csv"
        df.to_csv(destination, index=False)
        logger.info(f"Successfully saved master reference file to disk: {destination.name}")

    # Visual Standard Console Panel Summary Output Layout Box
    SEPARATOR = "-" * 40
    print("\n" + "=" * 40)
    print(f"{'Reference Dataset':<26} {'Rows':<10}")
    print(SEPARATOR)
    for name, df in outputs.items():
        print(f"{name.capitalize():<26} {len(df):,}")
    print(SEPARATOR)
    print("All master lookup constraints validated.")
    print("Reference layers successfully generated.")
    print("=" * 40 + "\n")


def main() -> None:
    """Production reference engine orchestrator."""
    HEADER_SEPARATOR = "=" * 60
    logger.info("Reference Data Matrix Initialization Routine")
    logger.info(HEADER_SEPARATOR)
    
    try:
        # Step 1: Execute Independent Base Core Dimensions
        df_stores = generate_stores()
        df_suppliers = generate_suppliers()
        df_promotions = generate_promotions()
        
        # Step 2: Execute Dependent Cascading Dimension Trees
        df_employees = generate_employees(df_stores)
        df_inventory = generate_inventory_snapshots(df_stores)
        
        # Step 3: Bundle collection array maps (FULLY CLOSED NOW)
        reference_payload = {
            "stores": df_stores,
            "suppliers": df_suppliers,
            "employees": df_employees,
            "promotions": df_promotions,
            "inventory_snapshots": df_inventory
        }
        
        # Step 4: Write datasets to disk and output terminal grid panel summary
        export_reference_layers(reference_payload)
        
        logger.info(HEADER_SEPARATOR)
        logger.info("Reference engine finished processing loops cleanly.")
        logger.info(HEADER_SEPARATOR)

    except FileNotFoundError as fnfe:
        logger.critical(f"Pipeline broke on upstream dependency violation: {str(fnfe)}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Fatal anomaly broke the master reference orchestration script thread: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
      main()
              

  


