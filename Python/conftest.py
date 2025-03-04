import pytest
import os
import logging
from datetime import datetime
#using pytest.hookimpl to configure the reports directory
os.makedirs("reports", exist_ok=True)#create reports directory

def pytest_configure(config):
    # custom markers 
    config.addinivalue_line(
        "markers", "description(text): mark test with a description for the report"
    )
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('reports/test.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    config._metadata = {
        'Project Name': 'RISE Test Automation',
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        if hasattr(item, '_testcase'):
            report.description = str(item._testcase.description)
            
            try:
                with open('reports/test.log', 'r') as f:
                    logs = f.read()
                    report.extra = [{'name': 'Test Logs', 'content': logs, 'format': 'text'}]
            except:
                pass