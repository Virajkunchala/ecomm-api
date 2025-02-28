import pytest
from app.services.order_service import OrderService
from app.models.order import Order
from app.models.product import Product
from app.schemas.order import OrderProductCreate
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import patch

def test_get_orders(test_db, sample_orders):
    service = OrderService(test_db)
    orders = service.get_orders()
    assert len(orders) == 2
    assert orders[0].total_price == 1250.0

def test_get_orders_pagination(test_db, sample_orders):
    service = OrderService(test_db)
    orders = service.get_orders(skip=1, limit=1)
    assert len(orders) == 1
    assert orders[0].total_price == 80.0

def test_place_order_success(test_db, sample_products):
    service = OrderService(test_db)
    order_products = [
        OrderProductCreate(product_id=sample_products[0].id, quantity=1),
        OrderProductCreate(product_id=sample_products[1].id, quantity=2),
    ]
    order = service.place_order(order_products)
    assert order.total_price == 1050.0
    assert order.status == "pending"
    assert sample_products[0].stock == 9
    assert sample_products[1].stock == 98 

def test_place_order_insufficient_stock(test_db, sample_products):
    service = OrderService(test_db)
    order_products = [
        OrderProductCreate(product_id=sample_products[0].id, quantity=100),
    ]
    with pytest.raises(ValueError) as exc_info:
        service.place_order(order_products)
    assert str(exc_info.value) == "Insufficient stock for product with ID 1."

def test_place_order_product_not_found(test_db):
    service = OrderService(test_db)
    order_products = [
        OrderProductCreate(product_id=999, quantity=1),
    ]
    with pytest.raises(ValueError) as exc_info:
        service.place_order(order_products)
    assert str(exc_info.value) == "Product with ID 999 not found."

def test_place_order_db_error(test_db, sample_products):
    service = OrderService(test_db)
    order_products = [
        OrderProductCreate(product_id=sample_products[0].id, quantity=1),
    ]

    with patch.object(test_db, 'commit', side_effect=SQLAlchemyError("Database error")) as mock_commit:
        with pytest.raises(SQLAlchemyError) as exc_info:
            service.place_order(order_products)
        assert str(exc_info.value) == "Database error"