import json
import os

from google.cloud import storage
from auth.gcp_service_account_auth import GCPServiceAccountAuth
from compliance.check_result import ComplianceCheckResult
from compliance.base_compliance import BaseComplianceChecker
from common.logger import app_logger
from common.utils import get_project_working_directory

class ComplianceChecker(BaseComplianceChecker):
    def __init__(self):
        
        current_dir = get_project_working_directory()
        self.directory_path = os.path.join(current_dir)
        try:
            
            self.credentials = GCPServiceAccountAuth().get_auth_credentials()
            #TODO: read it from passed AssetDiscovery Object 
            self.project_id = self.credentials.project_id
            #TODO: Better design is to abstract this into AssetComponentManager class which and get instance based on the asset type being executed.
            self.storage_client = storage.Client(
                credentials=self.credentials , project=self.credentials.project_id
            )
        except Exception as e:
            app_logger.log_exception(e)

    def load_rules(self, standard):
        # Load GCP compliance rules for the specified standard
        ### TODO: load the json file as resource stored inside python package to
        ### make the code OS-independent and avoids issues with path separators (/ vs \).
        full_path = os.path.join(
            self.directory_path, f"compliance_rules/gcp_{standard.lower()}.json"
        )
        try:
            with open(full_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            app_logger.log_error(f"{standard.lower()} Compliance Rules Json File for GCP Vendor not found")
        
        return {}
        

    def run_compliance_checks(self, standard):
        rules = self.load_rules(standard)
        results = []
        for rule_id, rule in rules.items():
            app_logger.log_message(f"Running Rule: {rule['description']}")
            try:
                check_results = self.check_rule(rule)
                compliance_result = ComplianceCheckResult(
                    rule_id=rule_id,
                    rule_description=rule["description"],
                    status=check_results["status"],
                    message=check_results.get("details", None),
                )
            except Exception as e:
                compliance_result = ComplianceCheckResult(
                    rule_id=rule_id,
                    rule_description=rule["description"],
                    status="FAIL",
                    message=str(e),
                )
            results.append(compliance_result.to_dict())
        return results

    def check_rule(self, rule):
        # Dynamically execute the rule's check function
        try:
            check_function = getattr(self, rule["check_function"])
            return check_function(rule)
        except AttributeError:
            return {
                "status": "FAIL",
                "details": f"Check function {rule['check_function']} not implemented",
            }
        except Exception as e:
            app_logger.log_exception(str(e))
            return {
                "status": "FAIL",
                "details": f"Check function {rule['check_function']} failed to execute due to unknown exception.",
            }

    # Example Rule Checks
    
    def check_bucket_encryption(self, rule):
        # Ensure GCP buckets have default encryption enabled
        buckets = list(self.storage_client.list_buckets())
        failed_buckets = []
        for bucket in buckets:
            if not bucket.default_kms_key_name and not bucket.storage_class == 'STANDARD':
                failed_buckets.append(bucket.name)

        if failed_buckets:
            return {
                "status": "FAIL",
                "details": f"Buckets without encryption: {', '.join(failed_buckets)}",
            }
        return {"status": "PASS", "details": "All buckets are encrypted"}

    def check_public_access(self, rule):
        # Ensure no buckets are publicly accessible
        buckets = list(self.storage_client.list_buckets())
        public_buckets = []
        for bucket in buckets:
            policy = bucket.get_iam_policy(requested_policy_version=3)
            for binding in policy.bindings:
                if (
                    "allUsers" in binding["members"]
                    or "allAuthenticatedUsers" in binding["members"]
                ):
                    public_buckets.append(bucket.name)

        if public_buckets:
            return {
                "status": "FAIL",
                "details": f"Publicly accessible buckets: {', '.join(public_buckets)}",
            }
        return {"status": "PASS", "details": "No buckets are publicly accessible"}

   
   
    def check_secure_data_deletion(self, rule):
         # Ensure GCP buckets have default encryption enabled
        buckets = list(self.storage_client.list_buckets())
        failed_buckets = []
        for bucket in buckets:
            if not bucket.versioning_enabled or not bucket.retention_period:
                failed_buckets.append(bucket.name)

        if failed_buckets:
            return {
                "status": "FAIL",
                "details": f"Buckets not configured for secure data deletion: {', '.join(failed_buckets)}",
            }
        return {"status": "PASS", "details": "All buckets are configured to securely delete the card holder data"}