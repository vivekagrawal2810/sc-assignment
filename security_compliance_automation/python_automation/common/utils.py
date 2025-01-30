import os


def get_project_working_directory():
    current_dir = os.getcwd()
    current_dir = os.path.join(
        current_dir, "security_compliance_automation/python_automation"
    )
    return current_dir