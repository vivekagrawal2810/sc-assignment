import os
from google.oauth2 import service_account

class GCPServiceAccountAuth():
    def __init__(self):
        super().__init__()
        # below hard coded for demo , needs to come from vault
        # can be configured as part of input param
        # TODO: Load Secrets from Vault manager being implemented
        current_dir = os.getcwd()
        current_dir = os.path.join(
            current_dir, "security_compliance_automation/python_automation"
        )
        service_account_key_file_path = os.path.join(
            current_dir, "auth", "gcp_cred.json"
        )
        self.__credentials = service_account.Credentials.from_service_account_file(
            service_account_key_file_path
        )
    def get_auth_credentials(self):
         return self.__credentials