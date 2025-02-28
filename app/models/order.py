from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.product import Product 

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)  # autoincrement is default
    total_price = Column(Float, nullable=False)
    status = Column(String, default="pending")

    products = relationship("OrderProduct", back_populates="order")

class OrderProduct(Base):
    __tablename__ = "order_products"

    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="products")
    product = relationship("Product", back_populates="orders")  