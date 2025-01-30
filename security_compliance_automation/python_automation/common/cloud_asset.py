from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CloudAsset:
    """Data Model for Cloud Asset Metadata"""
    name: str  # Mandatory for all assets
    provider: str  # AWS, Azure, GCP, etc.
    region: str  # Cloud region (us-east-1, europe-west3, etc.)
    metadata: Dict[str, str] = field(default_factory=dict)  # Optional details
