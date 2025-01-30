import datetime
import os
import json
import uuid
from compliance.manager import ComplianceManager
from vendor_config import VENDOR_CONFIG
from common.logger import app_logger
from common.utils import get_project_working_directory
from asset_discovery.asset_manager import AssetDiscoveryManager



def main():

    try:
     
        app_logger.log_message("Starting Asset Discovery...")
        # TODO : vendor name can be read from runtime arguments with defaults for local env.
        asset_manager = AssetDiscoveryManager(VENDOR_CONFIG)
        #TODO: send the results to ComplianceManager 
        asset_discovery_results = asset_manager.run_discovery()
        print(asset_discovery_results)
        app_logger.log_message("Completed Asset Discovery...")
        app_logger.log_message("Starting Compliance Assessment...")
        results = {}
        scan_id = str(uuid.uuid4())
        scan_date_utc= datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z%z")
        #TODO : this should be read from runtime argument with defaults for local env.
        standards = ["pci_dss", "cis"]
        for standard in standards:
            compliance_manager = ComplianceManager(VENDOR_CONFIG)
            results[standard] = compliance_manager.run_compliance(standard,scan_id=scan_id,scan_date_time=scan_date_utc)
        save_compliance_results(results)
        app_logger.log_message("Completed Compliance Assessment...")
        

    except Exception as e:
        app_logger.log_error(e)




def save_compliance_results(results):
    # save the json to a common location
    project_dir = get_project_working_directory()
    result_json_file = os.path.join(project_dir, "compliance_result.json")
    with open(result_json_file, "w") as json_file:
        json.dump(results, json_file, indent=4)


if __name__ == "__main__":
    main()
