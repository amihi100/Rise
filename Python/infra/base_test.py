import pytest
from infra.api_client import ApiClient
from utils.assertions import Assertions
from utils.logger import Logger

class BaseTest:
    def setup_method(self, method):
        self.logger = Logger()
        self.api_client = ApiClient()
        self.assertions = Assertions()
        self.logger.info(f"Starting test: {method.__name__}")
        
    def teardown_method(self, method):
        self.logger.info(f"Finishing test: {method.__name__}")