import importlib
from common.logger import app_logger

class ComplianceManager:
    #TODO: Adjust the design to read asset metadata from AssetDiscovery module.
    def __init__(self, vendor_configs):
        self.vendor_configs = vendor_configs

    def run_compliance(self, standard,scan_id,scan_date_time):
        results = {}
        for vendor, config in self.vendor_configs.items():
            app_logger.log_message(f"\nRunning {standard} compliance for {vendor.upper()}...")
            try:
                # Dynamically load the vendor module
                module = importlib.import_module(f'{vendor}_compliance.{vendor}_main')         
                checker = module.ComplianceChecker()
                results[vendor] = {
                    "scan_id": scan_id,
                    "scan_date_utc":scan_date_time,
                    "scan_results":checker.run_compliance_checks(standard)
                }
            except ModuleNotFoundError as me:
                app_logger.log_error(f"ComplianceCheck module for {vendor} not found:{me}")
            except Exception as e:
                app_logger.log_exception(str(e))
        return results
