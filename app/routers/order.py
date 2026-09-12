from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from typing import List


router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.OrderOut)
def checkout(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # 1. Get this user's cart items
    cart_items = db.query(models.CartItems).filter(models.CartItems.UserID == current_user.id).all()

    # 2. Empty cart check
    if len(cart_items) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cart is empty")

    total_amount = 0
    validated_items = []

    # 3 + 4. Validate stock AND accumulate total — one loop, ends here
    for cart_item in cart_items:
        product = db.query(models.Products).filter(models.Products.id == cart_item.ProductID).first()

        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {cart_item.ProductID} no longer exists")

        if product.StockQuantity < cart_item.Quantity:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="product is out of stock")

        total_amount += product.Price * cart_item.Quantity
        validated_items.append((cart_item, product))
    # <- loop fully ends here; everything below runs ONCE

    # 5. Create the Orders row — once, with the FINAL total_amount
    new_order = models.Orders(
        UserID=current_user.id,
        TotalAmount=total_amount,
        OrderStatus="Pending"
    )
    db.add(new_order)
    db.flush()   # assigns new_order.id, transaction still open

    # 6. For each validated pair: create an OrderItem AND reduce stock — new loop
    for cart_item, product in validated_items:
        new_order_item = models.OrderItem(
            OrderID=new_order.id,
            ProductID=product.id,
            Quantity=cart_item.Quantity,
            PurchasePrice=product.Price
        )
        db.add(new_order_item)
        product.StockQuantity -= cart_item.Quantity

    # 7. Clear the cart — another loop over the same validated pairs
    for cart_item, product in validated_items:
        db.delete(cart_item)

    # 8. Commit everything at once, with rollback safety
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Checkout failed, please try again")

    # 9. Refresh and return
    db.refresh(new_order)
    return new_order