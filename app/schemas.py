from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal
from datetime import datetime
from typing import Literal
from datetime import datetime
from typing import Optional



class ProductBase(BaseModel):
    # shared fields every product has — name, description, price, stock, category
    # fill these in yourself, snake_case, with correct types
    ...
    Name : str
    Description : str
    Price : Decimal
    StockQuantity : int
    CategoryID : int
class ProductCreate(ProductBase):
    # what extra does creation need that ProductBase doesn't have?
    # (hint: think about your last two attempts — does it need anything at all,
    #  or is ProductBase already everything the client sends on create?)
    ...


class ProductUpdate(BaseModel):
    # should this inherit ProductBase, or define its own fields as Optional?
    # think about PATCH semantics — partial updates
    ...
    Name: Optional[str] = None
    Description : Optional[str] = None
    Price : Optional[Decimal] = None
    StockQuantity : Optional[int] = None
    CategoryID : Optional[int] = None
    
    

    
class ProductOut(ProductBase):
    # what does the *response* have that the input never had?
    id: int
    UpdatedAt : datetime
    CreatedAt : datetime
    # createdAt / updatedAt go here if you want to expose them — who sets them?
    ...