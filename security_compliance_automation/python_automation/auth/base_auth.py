from abc import ABC, abstractmethod

class BaseAuth(ABC):
    @abstractmethod
    def get_auth_credentials(self):
        """Authentication for the vendor."""
        pass

  