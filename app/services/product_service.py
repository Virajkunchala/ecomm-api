from app.utils.logger import logger
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logger
    def get_products(self, skip: int = 0, limit: int = 10):
        """Fetch all products"""
        try:
            result = self.db.execute(select(Product).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching products: {str(e)}")
            raise
        
    def _check_duplicate_product(self, product: ProductCreate):
        """Check if a product with the same name already exists."""
        existing_product = self.db.query(Product).filter(
            Product.name == product.name
        ).first()
        if existing_product:
            raise ValueError("A product with the same name already exists.")

    def create_product(self, product: ProductCreate):
        """Create a new product"""
        try:
            self._check_duplicate_product(product)
            db_product = Product(**product.model_dump())
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)
            self.logger.info(f"Product created: {db_product.name}")
            return db_product
        except IntegrityError:
            self.db.rollback()
            self.logger.warning("IntegrityError: Duplicate product detected.")
            raise ValueError("A product with the same details already exists.")
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error(f"Database error during product creation: {str(e)}")
            raise