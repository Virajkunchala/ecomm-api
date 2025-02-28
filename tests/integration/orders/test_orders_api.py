import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.db_session import get_db
from app.schemas.order import OrderCreate
from app.models.product import Product
from app.models.order import Order, OrderProduct


@pytest.fixture(scope="function") 
def test_get_orders_api(test_client, sample_orders):
    response = test_client.get("/orders")
    assert response.status_code == 200
    assert len(response.json()) == 2
    
@pytest.fixture(scope="function") 
def test_get_orders_api_pagination(test_client, sample_orders):
    response = test_client.get("/orders?skip=1&limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["total_price"] == 75.0
    
@pytest.fixture(scope="function") 
def test_post_orders_api_success(test_client, sample_products):
    order_data = OrderCreate(products=[
        {"product_id": sample_products[0].id, "quantity": 1},
        {"product_id": sample_products[1].id, "quantity": 2},
    ])
    response = test_client.post("/orders", json=order_data.model_dump())
    assert response.status_code == 200
    assert response.json()["total_price"] == 1050.0
    assert response.json()["status"] == "pending"

@pytest.fixture(scope="function") 
def test_post_orders_api_insufficient_stock(test_client, sample_products):
    order_data = OrderCreate(products=[
        {"product_id": sample_products[0].id, "quantity": 100},
    ])
    response = test_client.post("/orders", json=order_data.model_dump())
    assert response.status_code == 400
    assert "Insufficient stock for product with ID 1." in response.json()["detail"]

@pytest.fixture(scope="function") 
def test_post_orders_api_product_not_found(test_client):
    order_data = OrderCreate(products=[
        {"product_id": 999, "quantity": 1},
    ])
    response = test_client.post("/orders", json=order_data.model_dump())
    assert response.status_code == 400
    assert "Product with ID 999 not found." in response.json()["detail"]
    
@pytest.fixture(scope="function") 
def test_post_orders_api_invalid_quantity(test_client, sample_products):
    order_data = OrderCreate(products=[
        {"product_id": sample_products[0].id, "quantity": -1},
    ])
    response = test_client.post("/orders", json=order_data.model_dump())
    assert response.status_code == 422
    assert "Quantity must be positive." in response.json()["detail"][0]["msg"]
    
@pytest.fixture(scope="function") 
def test_post_orders_api_empty_order(test_client):
    order_data = OrderCreate(products=[])
    response = test_client.post("/orders", json=order_data.model_dump())
    assert response.status_code == 422
    assert "Ensure this value has at least 1 item." in response.json()["detail"][0]["msg"]