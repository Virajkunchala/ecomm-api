import pytest
from app.schemas.product import ProductCreate
from app.services.product_service import ProductService
from app.models.product import Product
from sqlalchemy.exc import IntegrityError
from pydantic_core._pydantic_core import ValidationError

def test_get_products(test_db, sample_products):
    service = ProductService(test_db)
    products = service.get_products()
    assert len(products) == 3
    assert products[0].name == "Laptop"
    assert products[1].name == "Mouse"
    assert products[2].name == "Keyboard"

def test_get_products_pagination(test_db, sample_products):
    service = ProductService(test_db)
    products = service.get_products(skip=1, limit=1)
    assert len(products) == 1
    assert products[0].name == "Mouse"

@pytest.mark.usefixtures("sample_products")
def test_create_product(test_db, sample_product_create):
    service = ProductService(test_db)
    new_product = service.create_product(sample_product_create)
    
    assert new_product.name == "New Product"
    assert test_db.query(Product).count() == 4 

def test_create_duplicate_product(test_db):
    service = ProductService(test_db)
    product_data = ProductCreate(name='New Product', description='A brand new product', price=150.0, stock=30)
    service.create_product(product_data)  
    with pytest.raises(ValueError) as exc_info:
        service.create_product(product_data) 
    assert "A product with the same name already exists." in str(exc_info.value)
        

def test_create_product_negative_price(test_db):
    with pytest.raises(ValidationError):  
        product_data = ProductCreate(name="Invalid Product", description="Desc", price=-10.0, stock=50)

def test_create_product_negative_stock(test_db):
    with pytest.raises(ValidationError):
        product_data = ProductCreate(name="Invalid Product", description="Desc", price=10.0, stock=-50)

def test_create_product_empty_name(test_db):
    service = ProductService(test_db)
    with pytest.raises(ValidationError):
        ProductCreate(name="", description="Desc", price=10.0, stock=50)

def test_create_product_empty_description(test_db):
    service = ProductService(test_db)
    with pytest.raises(ValidationError):
        ProductCreate(name="Name", description="", price=10.0, stock=50)