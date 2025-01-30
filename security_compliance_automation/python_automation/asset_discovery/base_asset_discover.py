from abc import ABC, abstractmethod
from common.cloud_asset import CloudAsset
from typing import Dict,List

class BaseAssetDiscover(ABC):
    @abstractmethod
    def discover_assets(self)-> Dict[str,List[CloudAsset]]:
        """Discovers all assets and then configured to filter the relevant assets for the vendor. 
        This method can return Dictionary Instance with asset type as key and List of Cloud Asset Instances discovered"""
        pass

  