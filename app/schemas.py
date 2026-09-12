from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal
from datetime import datetime
from typing import Literal, List
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
    
    

    
# class ProductOut(ProductBase):
#     # what does the *response* have that the input never had?
#     id: int
#     UpdatedAt : datetime        this cause an error due to updatedat is null in stariting
#     CreatedAt : datetime   
#     model_config = {"from_attributes": True}
#     # createdAt / updatedAt go here if you want to expose them — who sets them?
#     ...

class ProductOut(ProductBase):
    id: int
    CreatedAt: datetime
    UpdatedAt: Optional[datetime] = None
    model_config = {"from_attributes": True}


class CategoryBase(BaseModel):
    Name : str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    Name: Optional[str] = None
    
    

class CategoryOut(CategoryBase):
    id : int
    # Name: Optional[str] = None
    CreatedAt : datetime

    model_config = {"from_attributes" : True}



class Token(BaseModel):
    access_token : str
    token_type : str

class UserLogin(BaseModel):
    Email : EmailStr
    Password: str


class TokenData(BaseModel):
    id : Optional[int] = None


class UserCreate(BaseModel):
    Name : str
    Email : EmailStr
    Password : str


class UserOut(BaseModel):
    id: int
    Name: str
    Email: EmailStr
    Role: str
    created_at: datetime

    model_config = {"from_attributes": True}



class CartItemBase(BaseModel):
    
    ProductID : int
    Quantity : int

class CartItemCreate(CartItemBase):
    pass



class CartItemOut(CartItemBase):
    id : int
    UserID : int

    model_config = {"from_attributes" : True}


class OrderItemOut(BaseModel):
    id : int
    OrderID : int
    ProductID : int
    Quantity : int
    PurchasePrice : Decimal

    model_config = {"from_attributes" : True}
    
class OrderOut(BaseModel):
    id : int
    UserID : int
    TotalAmount : Decimal
    OrderStatus : str
    CreatedAt : datetime
    order_items: List[OrderItemOut]   # <- a list of OrderItemOut objects, nested inside

    model_config = {"from_attributes" : True}

