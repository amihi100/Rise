import pytest
from infra.base_test import BaseTest

class TestProducts(BaseTest):
    @pytest.mark.description("Test products list")
    def test_get_all_products(self):
        response = self.api_client.read("products")
        self.assertions.assert_status_code(response, 200)
        products = response.json()
        
        self.assertions.assert_instance(products, list, 
            pass_message="Response contains a list of products",
            fail_message=f"Expected list of products, but got {type(products)}")
        
        self.assertions.assert_equal(len(products), 20, 
            pass_message="Product list contains 20 items",
            fail_message="Product list should contain exactly 20 items")
            
        product_titles = [product['title'] for product in products]
        self.logger.info(f"Products: {', '.join(product_titles[:3])}... and {len(product_titles)-3} more")
        
    @pytest.mark.description("Test product categories")
    def test_product_categories(self):
        response = self.api_client.read("products")
        products = response.json()
        categories = {product["category"] for product in products}
        expected_categories = {"men's clothing", "women's clothing", "electronics", "jewelery"}
        
        self.assertions.assert_equal(categories, expected_categories,
            pass_message="All expected categories found",
            fail_message="Categories don't match expected values")
        
    @pytest.mark.description("Test product structure")
    def test_product_structure(self):
        response = self.api_client.read("products", 1)
        product = response.json()
        required_fields = {"id", "title", "price", "description", "category", "image", "rating"}
        
        for field in required_fields:
            self.assertions.assert_in(field, product,
                pass_message=f"Product contains required field: {field}",
                fail_message=f"Product missing required field: {field}")
        
        self.assertions.assert_in("rate", product["rating"], 
            pass_message="Rating contains 'rate' field",
            fail_message="Rating missing 'rate' field")
            
        self.assertions.assert_in("count", product["rating"],
            pass_message="Rating contains 'count' field",
            fail_message="Rating missing 'count' field")
        
    @pytest.mark.description("Test price validation")
    def test_price_validation(self):
        response = self.api_client.read("products")
        products = response.json()
        prices = [product["price"] for product in products]
        
        self.assertions.assert_true(min(prices) > 0,
            pass_message="All prices are positive",
            fail_message="Found non-positive prices")
            
        self.assertions.assert_true(max(prices) < 1000,
            pass_message="All prices are below $1000",
            fail_message="Found prices over $1000")

    @pytest.mark.description("Test single product retrieval")
    def test_get_single_product(self):
        product_id = 1
        response = self.api_client.read("products", product_id)
        
        self.assertions.assert_status_code(response, 200)
        self.assertions.assert_json_has_key(response, "id")
        self.assertions.assert_json_value(response, "id", product_id)

    @pytest.mark.description("Test product creation")
    def test_create_product(self):
        payload = {
            "title": "Test Product",
            "price": 13.5,
            "description": "Test description",
            "category": "test category"
        }
        response = self.api_client.create("products", payload)
        
        self.assertions.assert_status_code(response, 200)
        self.assertions.assert_json_has_key(response, "id")
        self.assertions.assert_json_value(response, "title", payload["title"])

    @pytest.mark.description("Test product deletion")
    def test_delete_product(self):
        product_id = 1
        
        # Verify product exists
        get_response = self.api_client.read("products", product_id)
        self.assertions.assert_status_code(get_response, 200)
        
        # Delete product
        delete_response = self.api_client.delete("products", product_id)
        self.assertions.assert_status_code(delete_response, 200)

    @pytest.mark.description("Test API response time")
    def test_api_response_time(self):
        # Test list endpoint
        list_response = self.api_client.read("products")
        self.assertions.assert_status_code(list_response, 200)
        self.assertions.assert_response_time(list_response, 1000)
        
        # Test single item endpoint
        item_response = self.api_client.read("products", 1)
        self.assertions.assert_status_code(item_response, 200)
        self.assertions.assert_response_time(item_response, 500)

    @pytest.mark.description("Test non-existent product")
    def test_get_nonexistent_product(self):
        non_existent_id = 999
        response = self.api_client.read("products", non_existent_id)
        
        # FakeStoreAPI returns 200 even for non-existent products
        self.assertions.assert_status_code(response, 200)
        
        # Check that the response is empty or null
        try:
            product = response.json()
            self.assertions.assert_true(
                product is None or (isinstance(product, dict) and len(product) == 0),
                pass_message="API returned empty response for non-existent product",
                fail_message="API returned data for non-existent product"
            )
        except ValueError:
            self.logger.info("API returned non-JSON response for non-existent product")

    @pytest.mark.description("Test invalid product creation")
    def test_create_product_invalid_data(self):
        invalid_payload = {"title": ""}
        response = self.api_client.create("products", invalid_payload)
        
        # FakeStoreAPI accepts invalid data, so we just verify it responds
        self.assertions.assert_status_code(response, 200)
        self.logger.info("Note: FakeStoreAPI accepts invalid data (expected behavior for this mock API)")