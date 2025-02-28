from pydantic import BaseModel, Field, field_validator,ConfigDict
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)  
    description: Optional[str] = Field(None,  min_length=1,max_length=500) 
    price:float= Field(..., ge=0)
    stock:int= Field(..., ge=1)
    
    # @field_validator('price')
    # def validate_price(cls, value):
    #     if value < 0:
    #         raise ValueError("Price must be non-negative.")
    #     return value

    # @field_validator('stock')
    # def validate_stock(cls, value):
    #     if value < 1:
    #         raise ValueError("Stock must be non-negative.")
    #     return value
    
class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id:int
    
    model_config = ConfigDict(from_attributes=True)

    