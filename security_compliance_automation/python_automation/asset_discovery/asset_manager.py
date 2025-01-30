import importlib
from typing import Dict, List
from common.logger import app_logger
from common.cloud_asset import CloudAsset


class AssetDiscoveryManager:
    def __init__(self, vendor_configs):
        self.vendor_configs = vendor_configs

    def run_discovery(self) -> Dict[str, List[CloudAsset]]:
        results = {}
        for vendor, config in self.vendor_configs.items():
            app_logger.log_message(f"\nRunning asset discovery for {vendor.upper()}...")
            try:
                # Dynamically load the vendor module
                module = importlib.import_module(
                    f"asset_discovery.{vendor}_asset_discover"
                )
                asset_discovery_instance = module.AssetDiscover(config)
                return asset_discovery_instance.discover_assets()

            except ModuleNotFoundError as me:
                app_logger.log_error(f"Compliance module for {vendor} not found:{me}")
            except Exception as e:
                app_logger.log_exception(str(e))
        return results
