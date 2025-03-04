import json
from typing import Any
import logging

class Assertions:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def assert_status_code(self, response, expected_status_code: int):
        actual_status_code = response.status_code
        if actual_status_code == expected_status_code:
            self.logger.info(f"[PASS] Status code check: Expected {expected_status_code}, got {actual_status_code}")
        else:
            error_msg = f"Unexpected status code! Expected: {expected_status_code}, Actual: {response.status_code}"
            self.logger.error(f"[FAIL] {error_msg}")
            assert False, error_msg

    def assert_json_has_key(self, response, key: str):
        try:
            response_json = response.json()
            if key in response_json:
                self.logger.info(f"[PASS] JSON has key: '{key}' found in response")
            else:
                error_msg = f"Response JSON doesn't have key '{key}'"
                self.logger.error(f"[FAIL] {error_msg}")
                assert False, error_msg
        except json.JSONDecodeError:
            error_msg = "Response is not in JSON format"
            self.logger.error(f"[FAIL] {error_msg}")
            assert False, error_msg

    def assert_json_value(self, response, key: str, expected_value: Any):
        try:
            response_json = response.json()
            if key in response_json:
                if response_json[key] == expected_value:
                    self.logger.info(f"[PASS] JSON value check: '{key}' equals {expected_value}")
                else:
                    error_msg = f"JSON value '{key}' is not equal to {expected_value}, got {response_json[key]}"
                    self.logger.error(f"[FAIL] {error_msg}")
                    assert False, error_msg
            else:
                error_msg = f"Response JSON doesn't have key '{key}'"
                self.logger.error(f"[FAIL] {error_msg}")
                assert False, error_msg
        except json.JSONDecodeError:
            error_msg = "Response is not in JSON format"
            self.logger.error(f"[FAIL] {error_msg}")
            assert False, error_msg
            
    def assert_true(self, condition, pass_message, fail_message):
        if condition:
            self.logger.info(f"[PASS] {pass_message}")
        else:
            self.logger.error(f"[FAIL] {fail_message}")
            assert False, fail_message
            
    def assert_equal(self, actual, expected, pass_message=None, fail_message=None):
        if actual == expected:
            msg = pass_message or f"Values are equal: {actual} == {expected}"
            self.logger.info(f"[PASS] {msg}")
        else:
            msg = fail_message or f"Values are not equal! Expected: {expected}, Actual: {actual}"
            self.logger.error(f"[FAIL] {msg}")
            assert False, msg
            
    def assert_in(self, item, container, pass_message=None, fail_message=None):
        if item in container:
            msg = pass_message or f"Item '{item}' found in container"
            self.logger.info(f"[PASS] {msg}")
        else:
            msg = fail_message or f"Item '{item}' not found in container"
            self.logger.error(f"[FAIL] {msg}")
            assert False, msg
            
    def assert_instance(self, obj, cls, pass_message=None, fail_message=None):
        if isinstance(obj, cls):
            msg = pass_message or f"Object is instance of {cls.__name__}"
            self.logger.info(f"[PASS] {msg}")
        else:
            msg = fail_message or f"Object is not instance of {cls.__name__}, but {type(obj).__name__}"
            self.logger.error(f"[FAIL] {msg}")
            assert False, msg

    def assert_response_time(self, response, max_time_ms: float, pass_message=None, fail_message=None):
        """Assert that response time is within acceptable limits"""
        if hasattr(response, 'response_time'):
            response_time = response.response_time
            if response_time <= max_time_ms:
                msg = pass_message or f"Response time {response_time:.2f} ms is within limit of {max_time_ms} ms"
                self.logger.info(f"[PASS] {msg}")
            else:
                msg = fail_message or f"Response time {response_time:.2f} ms exceeds limit of {max_time_ms} ms"
                self.logger.error(f"[FAIL] {msg}")
                assert False, msg
        else:
            self.logger.error("[FAIL] Response object does not have response_time attribute")
            assert False, "Response time was not measured for this request"