**API Test Automation Framework**

API test automation framework for testing REST APIs. Uses pytest for running tests and generating HTML reports.
Last run example: 10 passed in 4.00s

**Requirements**
Python 3.9 or higher
pytest>=7.0.0
requests==2.28.2
pytest-html==3.2.0
pyyaml==6.0


**API calls exmamples**

Get all products:
response = self.api_client.read("products")

Get a specific product:
response = self.api_client.read("products", 1)

Create a new product:
payload = {"title": "Test Product", "price": 13.5}
response = self.api_client.create("products", payload)

Delete a product:
response = self.api_client.delete("products", 1)

**Clone the repo:**
git clone "https://github.com/amihi100/API_Python.git" "your\local\machaine"

**Run tests commands:**
pytest --html=reports/report.html

**Build Docker image:**
docker build -t api-test-framework .

**Run tests in Docker:**
docker run my-app
OR:
docker run -v $(pwd)/reports:/app/reports api-test-framework

**Reports:**
HTML report of 9 tests will be generated each run under:
\RiseProject\reports\report.html
generated html file: file:
///C:/Documents/RiseProject/reports/report.html

==================================== 10 passed in 4.00s ====================================

**Project structure:**

├── infra/                  # Core framework components

│   ├── api_client.py       # HTTP client for API requests

│   └── base_test.py        # Base test class with common functionality

├── tests/                  # Test files

│   └── test_products.py    # Tests for product API endpoints

├── utils/                  # Utility classes

│   ├── assertions.py       # Custom assertion methods

│   └── logger.py           # Logging functionality

├── reports/                # Generated test reports

├── conftest.py             # Pytest configuration

├── requirements.txt        # Required packages

├── Dockerfile              # Docker configuration

└── README.md               #current file
