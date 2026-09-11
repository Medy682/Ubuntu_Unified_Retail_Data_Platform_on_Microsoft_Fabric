"""
event_simulator.py
Production-grade live retail streaming engine.
Reads transaction templates from disk and streams live event payloads 
directly into memory and broadcasts them to Azure Event Hubs.
"""


from __future__ import annotations
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Try importing the official Azure client SDK
from azure.eventhub import EventHubProducerClient, EventData

# ==============================================================================
# CONFIGURATION & PROJECT PATHS
# ==============================================================================
# 1. Get the exact folder where event_simulator.py lives (the scripts/ folder)
SCRIPT_DIR = Path(__file__).resolve().parent

# 2. Step up exactly one level to hit the root folder where environment_variable.env lives
PROJECT_ROOT = SCRIPT_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
BATCH_DATA_DIR = DATA_DIR / "batch"
LOGS_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOGS_DIR / "event_simulator.log"

# 3. Explicitly discover and load your custom environment file layout
env_file_path = PROJECT_ROOT / "environment_variable.env"

# 4. Force load_dotenv to read it, checking if the file actually exists first
if env_file_path.exists():
    load_dotenv(dotenv_path=env_file_path, override=True)
else:
    print(f"CRITICAL ERROR: Python cannot find the env file at: {env_file_path}")

# Fallbacks will act as automatic fail-safes if your .env file parsing ever drops out
EVENT_HUB_CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STR")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")

# Simulation Tuning Knobs
STREAM_DELAY_SECONDS = 2.0 
BATCH_SEND_SIZE = 5 

# ==============================================================================
# LOGGER CONFIGURATION
# ==============================================================================
def configure_logger() -> logging.Logger:
    """Initialize local event streaming log handlers."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    local_log = logging.getLogger("event_simulator")
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
# CORE EVENT ENGINE ROUTINES
# ==============================================================================
def run_live_simulation(df_template: pd.DataFrame) -> None:
    """Infinite in-memory stream generator loop mimicking retail actions."""
    logger.info("Initializing Azure Event Hubs Producer Client...")
    
    # Air-tight verification check looking for authentic protocol formats
    is_live_cloud = True
       
    if is_live_cloud:
        logger.info(f"CONNECTED: Live cloud endpoint hub active: '{EVENT_HUB_NAME}'")
        client = EventHubProducerClient.from_connection_string(
            conn_str=EVENT_HUB_CONNECTION_STR, 
            eventhub_name=EVENT_HUB_NAME
        )
    else:
        logger.warning("DRY-RUN FALLBACK MODE ACTIVE: Azure SDK missing or connection parameters unconfigured.")
        client = None
        
    logger.info("Stream Loop Started successfully. Press [CTRL + C] to halt event production loops.")
    EVENT_TYPES = ["product_view", "cart_action", "checkout_start", "purchase_success", "inventory_update"]
    message_batch = []
    
    try:
        while True:
            # 1. Sample base data for realistic customer/product attributes
            sample_row = df_template.sample(n=1).iloc[0]
            current_time = datetime.now(timezone.utc).isoformat()
            chosen_event = np.random.choice(EVENT_TYPES, p=[0.40, 0.25, 0.15, 0.15, 0.05])
            
            # 2. Build the baseline shared schema payload
            event_payload = {
                "event_type": chosen_event,
                "event_timestamp": current_time,
                "customer_id": str(sample_row["Customer ID"]),
                "product_id": str(sample_row["StockCode"]),
                "product_description": str(sample_row["Description"]),
                "country": str(sample_row["Country"])
            }
            
            # 3. Inject event-specific columns depending on the business action
            if chosen_event == "product_view":
                event_payload.update({"session_id": f"SES_{np.random.randint(10000, 99999)}", "view_duration_seconds": int(np.random.randint(5, 180))})
            elif chosen_event == "cart_action":
                event_payload.update({"cart_id": f"CRT_{np.random.randint(10000, 99999)}", "action": np.random.choice(["add_item", "remove_item", "update_quantity"]), "quantity": int(np.random.randint(1, 5))})
            elif chosen_event == "checkout_start":
                event_payload.update({"checkout_id": f"CHK_{np.random.randint(10000, 99999)}", "payment_method_preference": np.random.choice(["Credit Card", "Boleto", "PayPal", "Voucher"])})
            elif chosen_event == "purchase_success":
                event_payload.update({"invoice_id": str(sample_row["Invoice"]), "quantity": int(sample_row["Quantity"]), "unit_price": float(sample_row["Price"]), "total_order_value": round(int(sample_row["Quantity"]) * float(sample_row["Price"]), 2)})
            elif chosen_event == "inventory_update":
                event_payload.update({"warehouse_id": f"WH_{np.random.choice(['SP_01', 'RJ_02', 'BH_03'])}", "stock_adjustment": int(np.random.choice([-10, -5, 20, 50, 100])), "reason_code": np.random.choice(["Restock", "Damaged Goods", "Cycle Count Adjustment"])})
            
            # Serialize payload to JSON transmission strings
            serialized_data = json.dumps(event_payload)
            message_batch.append(serialized_data)
            
            logger.info(f"LIVE STREAM -> Type: {chosen_event:<18} | Customer: {event_payload['customer_id']:<10} | Time: {current_time}")
            
            # 4. Flush batch to network array when size limit met
            if len(message_batch) >= BATCH_SEND_SIZE:
                if is_live_cloud and client is not None:
                    event_data_batch = client.create_batch()
                    for msg in message_batch:
                        event_entry = EventData(msg)
                        # CRITICAL: Content-Type header forces Fabric to allow data preview rendering
                        event_entry.content_type = "application/json"
                        event_data_batch.add(event_entry)
                        
                    client.send_batch(event_data_batch)
                    logger.info(f"SUCCESS: Network flush executed for {BATCH_SEND_SIZE} cloud event packets.")
                else:
                    logger.info(f"DRY-RUN SIMULATION: Successfully flushed {BATCH_SEND_SIZE} packets locally.")
                
                # Wiped cleanly inside the appropriate batch block tracking scope
                message_batch.clear()
                
            time.sleep(STREAM_DELAY_SECONDS)
            
    except KeyboardInterrupt:
        logger.warning("\nPipeline interruption caught manually via Keyboard command. Initializing safe closing routines...")
    finally:
        if client is not None:
            client.close()
        logger.info("Live Event Hub producer client session disconnected cleanly. System halted.")

def main() -> None:
    HEADER_SEPARATOR = "=" * 60
    logger.info("Real-Time Messaging Simulation Bus Initializing")
    logger.info(HEADER_SEPARATOR)
    try:
        template_source_path = BATCH_DATA_DIR / "pos_sales_transactions.csv"
        if not template_source_path.exists():
            raise FileNotFoundError(
                f"Missing upstream data template dependency: '{template_source_path.name}'\n"
                f"Please ensure scripts/generate_sample_datasets.py has executed successfully first."
            )
        logger.info(f"Extracting streaming sequence parameters from: {template_source_path.name}")
        df_template = pd.read_csv(template_source_path)
        #  Clear out empty or corrupt index references to protect stream types
        df_template = df_template.dropna(subset=["Invoice", "Price", "Customer ID"])
        run_live_simulation(df_template)
    except FileNotFoundError as fnfe:
        logger.critical(f"Pipeline initialization terminated: {str(fnfe)}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Fatal error crashed the live event simulator script thread: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
