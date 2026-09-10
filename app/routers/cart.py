# app/routers/cart.py


from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from typing import List


router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CartItemOut)
def create_cart_item(cartitem: schemas.CartItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    existing_item = db.query(models.CartItems).filter(
        models.CartItems.UserID == current_user.id,
        models.CartItems.ProductID == cartitem.ProductID  
    ).first()

    
    if existing_item:
        existing_item.Quantity += cartitem.Quantity  
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        new_item = models.CartItems(
            UserID=current_user.id,
            ProductID= cartitem.ProductID,
            Quantity=cartitem.Quantity
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item


@router.get("/", response_model=List[schemas.CartItemOut])
def get_all_cart_items(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    cartitem = db.query(models.CartItems).filter(models.CartItems.UserID == current_user.id).all()
    return cartitem



@router.get("/{id}", response_model=schemas.CartItemOut)
def get_one_cart_item(id:int, db:Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    item = db.query(models.CartItems).filter(
    models.CartItems.id == id,
    models.CartItems.UserID == current_user.id
                ).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"cart of id {id} not found")
    return item


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(id:int, db:Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    cart = db.query(models.CartItems).filter(models.CartItems.id == id,
                                            models.CartItems.UserID == current_user.id).first()

    
    if cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"cart of id {id} not found")

    db.delete(cart)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)
