from app.utils.logger import logger
from sqlalchemy.orm import Session
from app.models.order import Order,OrderProduct
from app.models.product import Product
from app.schemas.order import OrderProductResponse,OrderCreate,OrderResponse
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
class OrderService:
    def __init__(self,db:Session):
        self.db=db
        
    def place_order(self,product_quantities:list):
        
        """place the order by validating the stock and creating the order"""
        
        try:
            self._validate_stock(product_quantities)
            order = self._create_order(product_quantities)
            self.db.commit()
            return order
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error placing order: {str(e)}")
            raise
    
    def _validate_stock(self,product_quantities:dict):
        """Check if there is enough stock for each product."""
        
        for product in product_quantities:
            product_id = product.product_id
            quantity = product.quantity
            
            if quantity < 1:
                raise ValueError(f"Quantity for product ID {product_id} must be positive.")
            
            product_in_db =self.db.query(Product).filter(Product.id==product_id).first()
            
            if not product_in_db:
                raise ValueError(f"Product with ID {product_id} not found.")
            if product_in_db.stock  < quantity:
                raise ValueError(f"Insufficient stock for product with ID {product_id}.")
            
        
    def _create_order(self, product_quantities: list):
        total_price = 0.0

        db_order = Order(total_price=total_price, status="pending")
        self.db.add(db_order)
        self.db.flush()
        

        for item in product_quantities:
            product = self.db.query(Product).filter(Product.id == item.product_id).first()
            total_price += product.price * item.quantity
            db_order_product = OrderProduct(order_id=db_order.id, product_id=item.product_id, quantity=item.quantity)
            self.db.add(db_order_product)
            product.stock -= item.quantity
            self.db.add(product)
            
        db_order.total_price = total_price
        return db_order
    
    def get_orders(self, skip: int = 0, limit: int = 10):
        """Fetch all orders"""
        try:
            result = self.db.execute(select(Order).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching orders: {str(e)}")
            raise