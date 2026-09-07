from fastapi import Response , status, HTTPException, Depends, APIRouter 
# from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas



router = APIRouter(
    prefix="/product",
    tags = ['product']    
)




@router.get("/", status_code=status.HTTP_200_OK)
def get_product(db: Session = Depends(get_db)):
    products = db.query(models.Products).all()
    return products





@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product : schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Products(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put("/{id}")
def update_product(product : schemas.ProductUpdate):
    return {"Status" : "product updated"}


@router.delete("/{id}")
def delete_product():
    return {"Status" : "product deleted"}