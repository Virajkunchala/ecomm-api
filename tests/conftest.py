# tests/conftest.py
import sys
sys.path.append("/app")
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.product import ProductCreate
# from app.schemas.order import OrderProductCreate
from app.models.product import Product
from app.models.order import Order, OrderProduct
from app.database.db_session import get_db
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="function")
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Product.metadata.create_all(engine)
    Order.metadata.create_all(engine)
    OrderProduct.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="function")
def test_client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client
        
        
@pytest.fixture(scope="function")
def sample_products(test_db):
    # Create sample product data
    products = [
        Product(name="Laptop", description="A great laptop", price=1000.0, stock=10),
        Product(name="Mouse", description="Wireless mouse", price=25.0, stock=100),
        Product(name="Keyboard", description="Mechanical keyboard", price=75.0, stock=50),
    ]
    
    # Insert into the test database
    test_db.add_all(products)
    test_db.commit()

    # Return the products for use in tests
    return products

@pytest.fixture(scope="function")
def sample_product_create():
    # Create a sample product creation payload
    return ProductCreate(
        name="New Product",
        description="A brand new product",
        price=150.0,
        stock=30
    )
@pytest.fixture(scope="function")
def sample_orders(test_db, sample_products):
    orders = [
        Order(total_price=1250.0, status="completed", products=[
            OrderProduct(product_id=sample_products[0].id, quantity=1),
            OrderProduct(product_id=sample_products[1].id, quantity=2)
        ]),
        Order(total_price=80.0, status="completed", products=[
            OrderProduct(product_id=sample_products[2].id, quantity=1)
        ])
    ]
    test_db.add_all(orders)
    test_db.commit()
    return orders