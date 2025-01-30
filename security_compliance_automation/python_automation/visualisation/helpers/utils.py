import os
import json
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_json_data(file_path):
    """Loads JSON data from a file and logs errors."""
    try:
        logger.info(f"Loading JSON data from {file_path}")
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None

        with open(file_path, 'r') as file:
            data = json.load(file)
        logger.info(f"Successfully loaded data from {file_path}")
        return data
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    return None


def get_shared_data_file_path():
    current_dir = os.getcwd()
    current_dir = os.path.join(
        current_dir, "security_compliance_automation/python_automation"
    )
    return os.path.join(current_dir, "compliance_result.json")

def json_to_dataframe(standard_data):
    """
    Converts compliance data for a specific standard to a DataFrame.
    
    Args:
        standard_data (dict): The compliance standard data (e.g., `pci_dss` data).
        
    Returns:
        pd.DataFrame: DataFrame containing scan results.
    """
    results = []
    for vendor, details in standard_data.items():
        scan_results = details.get("scan_results", [])
        for result in scan_results:
            results.append({
                "Vendor": vendor,
                "ScanID": details.get("scan_id", ""),
                "ScanDate": details.get("scan_date_utc", ""),
                "RuleID": result.get("rule_id", ""),
                "RuleDescription": result.get("rule_description", ""),
                "Status": result.get("status", ""),
                "Message": result.get("message", "")
            })
    return pd.DataFrame(results)