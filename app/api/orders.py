from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.db_session import get_db
from app.services.order_service import OrderService
from app.schemas.order import OrderCreate, OrderResponse,OrderProductResponse

router = APIRouter()

@router.get("/orders", response_model=list[OrderResponse])
def read_orders(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    """Retrieve paginated products."""
    try:
        order_service = OrderService(db)
        orders = order_service.get_orders(skip=skip, limit=limit)
        return orders
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """place a new order."""
    try:
        order_service = OrderService(db)  # Initialize OrderService with db session
        order = order_service.place_order(order.products)  # Call the place_order method
        return order
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
