import logging
import os
from common.utils import get_project_working_directory

class LoggerConfig:
    _instance = None  # Class-level variable to store the singleton instance

    current_dir = get_project_working_directory()
   
    logFilePath = os.path.join(current_dir, "logs/compliance_automation.log")

    def __new__(cls, log_file_path=logFilePath, log_level=logging.DEBUG):
        """Override __new__ to control instance creation"""
        if not cls._instance:
            # If no instance exists, create one
            cls._instance = super().__new__(cls)
            cls._instance.__initialize(log_file_path, log_level)
        return cls._instance

    def __initialize(self, log_file_path, log_level):
        """Initialize the logger once when the instance is created"""
        if not hasattr(self, "__initialized"):  # Prevent reinitialization
            self.__logFilePath = log_file_path
            self.__logLevel = log_level

            # Configure the logger
            self.__logger = logging.getLogger("LoggerConfig")
            self.__logger.setLevel(self.__logLevel)

            # Create a single file handler
            file_handler = logging.FileHandler(self.__logFilePath)
            file_handler.setLevel(self.__logLevel)

            # Create console handler (logs to console)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.__logLevel)

            # Create a formatter and add it to the file handler
            formatter = logging.Formatter(
                "%(asctime)s - %(module)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # Add the file handler to the logger
            self.__logger.addHandler(file_handler)
            self.__logger.addHandler(console_handler)

            self.__initialized = True  # Mark the instance as initialized

    def log_message(self, message):
        """Method to log a message"""
        self.__logger.info(message)

    def log_error(self, error_message):
        """Method to log an error message"""
        self.__logger.error(error_message)

    def log_exception(self, exception):
        """Method to log an exception"""
        self.__logger.exception(exception)

    @classmethod
    def get_instance(cls):
        """Get the singleton instance of LoggerConfig"""
        return cls._instance


app_logger = LoggerConfig().get_instance()
