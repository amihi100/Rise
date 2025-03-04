import time
import requests
from utils.logger import Logger

class ApiClient:
    def __init__(self, base_url="https://fakestoreapi.com"): #constructor
        self.base_url = base_url
        self.logger = Logger()
    
    def _measure_response_time(self, method, url, **kwargs):
        """Measure response time for an API request"""
        start_time = time.time()
        response = method(url, **kwargs)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.logger.info(f"Response time: {response_time:.2f} ms")
        response.response_time = response_time  # Attach response time to response object
        return response

    #Below are the methods for the API client by CRUD operations.
    #create product
    def create(self, endpoint: str, payload: dict) -> requests.Response: # 
        """Create a new resource"""
        url = f"{self.base_url}/{endpoint}"
        self.logger.info(f"POST request sent to {url}")
        return self._measure_response_time(requests.post, url, json=payload)
    
    #get product
    def read(self, endpoint: str, item_id: int = None) -> requests.Response:
        """Read a resource or list of resources"""
        url = f"{self.base_url}/{endpoint}"
        if item_id:
            url = f"{url}/{item_id}"
        self.logger.info(f"GET request sent to {url}")
        return self._measure_response_time(requests.get, url)
    
    #delete product
    def delete(self, endpoint: str, item_id: int) -> requests.Response:
        """Delete a resource"""
        url = f"{self.base_url}/{endpoint}/{item_id}"
        self.logger.info(f"DELETE request sent to {url}")
        return self._measure_response_time(requests.delete, url) 