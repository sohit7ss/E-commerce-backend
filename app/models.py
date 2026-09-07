# app/Models.py


from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DECIMAL
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship

class Products(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key= True, nullable=False)
    Name = Column (String, nullable= False) 
    Description = Column(String)
    Price = Column(DECIMAL, nullable=False)
    StockQuantity = Column(Integer, nullable=False, default=0)
    CategoryID = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    CreatedAt = Column(TIMESTAMP(timezone = True), 
                        nullable = False, server_default=text('now()'))
    UpdatedAt = Column(TIMESTAMP(timezone = True))

    category = relationship("Categories", back_populates="products") #.............................
    cart_items = relationship("CartItems", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key= True, nullable=False)
    Name = Column(String, nullable=False)
    Email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)
    Role = Column(String, nullable=False, default="customer")
    created_at = Column(TIMESTAMP(timezone = True), 
                        nullable = False, server_default=text('now()'))
    orders = relationship("Orders", back_populates="user") #.........
    cartitems = relationship("CartItems", back_populates="user")
    


class CartItems(Base):

    __tablename__  = "cartitems"

    id = Column(Integer, primary_key=True, nullable= False)
    UserID = Column(Integer, ForeignKey(
                    "users.id", ondelete= "CASCADE", onupdate="CASCADE"), 
                    nullable=False)
    ProductID = Column(Integer, ForeignKey(
                    "products.id", ondelete= "CASCADE", onupdate="CASCADE"), 
                    nullable=False)
    Quantity = Column(Integer, nullable=False, default=1)
    user = relationship("User", back_populates="cartitems")
    product = relationship("Products", back_populates="cart_items")
    


class Categories(Base):

    __tablename__ = "categories"

    id = Column(Integer, nullable=False, primary_key=True)
    Name = Column(String, nullable=False, unique=True)
    CreatedAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default = text('now()'))

    products = relationship("Products", back_populates="category") #.........................


class Orders(Base):

    __tablename__ = "orders"

    id = Column(Integer, nullable=False, primary_key=True)
    UserID = Column(Integer, ForeignKey(
                            "users.id", ondelete= "CASCADE", onupdate="CASCADE"),
                            nullable=False)
    TotalAmount = Column(DECIMAL, nullable=False)
    OrderStatus = Column(String, nullable=False, default="Pending")
    CreatedAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default = text('now()'))

    # user_order = relationship("User", back_populates="orders")
    user = relationship("User", back_populates="orders") #--------------
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "ordersitem"
    id = Column(Integer, nullable=False, primary_key=True)
    OrderID = Column(Integer, ForeignKey( 
                    "orders.id", ondelete= "CASCADE", onupdate="CASCADE"), 
                    nullable=False)
    ProductID = Column(Integer, ForeignKey(
                    "products.id", ondelete= "CASCADE", onupdate="CASCADE"), 
                    nullable=False)
    Quantity = Column(Integer, nullable=False)
    PurchasePrice = Column(DECIMAL, nullable=False)
    order = relationship("Orders", back_populates="order_items")
    product = relationship("Products", back_populates="order_items")