from abc import ABC, abstractmethod


class BaseComplianceChecker(ABC):

    @abstractmethod
    def load_rules(self, standard):
        """Load compliance rules for a specific standard (e.g., CIS, PCI-DSS)."""
        pass

    @abstractmethod
    def run_compliance_checks(self, standard):
        """Run compliance checks for a specific standard."""
        pass

    @abstractmethod
    def check_rule(self, rule):
        """Run a single compliance rule check."""
        """"rule parameter can carry valuable validation metadata info required to run the check. """
        pass
