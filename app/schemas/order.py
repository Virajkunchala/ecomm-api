from pydantic import BaseModel, ConfigDict,Field, field_validator
from typing import Dict,List,Optional

class OrderProductCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    
    @field_validator('quantity')
    def validate_quantity(cls, value):
        if value < 1:
            raise ValueError("Quantity must be positive.")
        return value
    
class OrderProductResponse(BaseModel):
    product_id: int
    quantity: int
    
class OrderCreate(BaseModel):
    products: List[OrderProductCreate]  # List of products with quantity
    

class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str
    products: List[OrderProductResponse]  # List of products in the order

    model_config = ConfigDict(from_attributes=True)
