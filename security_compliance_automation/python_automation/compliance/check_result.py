class ComplianceCheckResult:
    # TODO: Use @dataclass decorator
    def __init__(self, rule_id, rule_description, status, message=None):

        self.rule_id = rule_id

        self.rule_description = rule_description
        self.status = status
        self.message = message

    def to_dict(self):

        return {
            "rule_id": self.rule_id,
            "rule_description": self.rule_description,
            "status": self.status,
            "message": self.message,
        }

    def __str__(self):

        result = f"Rule ID: {self.rule_id}\n"

        result += f"Description: {self.rule_description}\n"
        result += f"Status: {self.status}\n"
        if self.message:
            result += f"Failure Message: {self.message}\n"

        return result
