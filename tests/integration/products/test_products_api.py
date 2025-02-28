from fastapi.testclient import TestClient
from app.main import app
from app.database.db_session import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.product import Product
import pytest


@pytest.fixture(scope="function") 
def test_get_products_api(test_client, sample_products):
    response = test_client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 3
    
@pytest.fixture(scope="function")   
def test_post_products_api(test_client, sample_product_create):
    response = test_client.post("/products", json=sample_product_create.model_dump())
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"
 
@pytest.fixture(scope="function")      
def test_post_products_api_duplicate(test_client, sample_product_create):
    test_client.post("/products", json=sample_product_create.model_dump())
    response = test_client.post("/products", json=sample_product_create.model_dump())
    assert response.status_code == 409
    
@pytest.fixture(scope="function")        
def test_post_products_api_negative_price(test_client):
    product_data = {"name": "Invalid Product", "description": "Desc", "price": -10.0, "stock": 50}
    response = test_client.post("/products", json=product_data)
    assert response.status_code == 422
    
@pytest.fixture(scope="function")          
def test_post_products_api_negative_stock(test_client):
    product_data = {"name": "Invalid Product", "description": "Desc", "price": 10.0, "stock": -50}
    response = test_client.post("/products", json=product_data)
    assert response.status_code == 422
