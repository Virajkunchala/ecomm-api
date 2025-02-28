from app.utils.logger import logger
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from app.database.db_session import get_db
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter()

@router.get("/products", response_model=list[ProductResponse])
def read_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    """Retrieve paginated products."""
    try:
        product_service = ProductService(db)
        products = product_service.get_products(skip=skip, limit=limit)
        return products
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving products: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/products", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Add a new product."""
    try:
        product_service = ProductService(db)
        new_product = product_service.create_product(product)
        return new_product
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product with same details already exists")
    except SQLAlchemyError as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")