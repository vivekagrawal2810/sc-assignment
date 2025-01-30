import os
from google.cloud import asset_v1
from google.oauth2 import service_account
from common.cloud_asset import CloudAsset
from auth.gcp_service_account_auth import GCPServiceAccountAuth
from common.utils import get_project_working_directory
from asset_discovery.base_asset_discover import BaseAssetDiscover
from typing import Dict,List

class AssetDiscover(BaseAssetDiscover):
    """
    Designed using Factory Pattern
    Discovers all the assets configured for GCP.
    """
    __VENDOR = "gcp"
    def __init__(self, vendor_config):
        self.project_id = vendor_config["project_id"]
        self.credentials = GCPServiceAccountAuth().get_auth_credentials()
        self.asset_types = self.get_asset_types()
        self.asset_client = asset_v1.AssetServiceClient(credentials=self.credentials)
        self.asset_resources_info = {}

    def discover_assets(self)-> Dict[str,List[CloudAsset]]:
        return self.list_assets_by_types(self.asset_types)

  

    def list_assets_by_types(self, asset_types):
        scope = f"projects/{self.project_id}"

        # Request to list assets
        request = asset_v1.ListAssetsRequest(
            parent=scope,
            asset_types=asset_types,
            content_type=asset_v1.ContentType.RESOURCE,
        )

        response = self.asset_client.list_assets(request=request)
        assets_results = {}

        for asset in response:          
            asset_type = asset.asset_type
            if asset_type not in assets_results and asset_type in self.asset_types:
                assets_results[asset_type] = []
            assets_results[asset_type].append(CloudAsset(asset.name,self.__VENDOR,"",None))

        return assets_results

    def get_asset_types(self):
        asset_types = [
            "storage.googleapis.com/Bucket",
            "logging.googleapis.com/LogSink",
            "cloudkms.googleapis.com/CryptoKey",
            "compute.googleapis.com/Instance",
            "compute.googleapis.com/Firewall",
            "sqladmin.googleapis.com/Instance",
            "cloudfunctions.googleapis.com/CloudFunction",
            "bigquery.googleapis.com/Dataset",
            "pubsub.googleapis.com/Topic",
            "pubsub.googleapis.com/Subscription",
            "iam.googleapis.com/ServiceAccount",
        ]
        return asset_types
