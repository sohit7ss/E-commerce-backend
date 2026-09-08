# app/routers/product.py

from fastapi import Response , status, HTTPException, Depends, APIRouter 
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from typing import List



router = APIRouter(
    prefix="/product",
    tags = ['product']
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ProductOut])
def get_all_product(db: Session = Depends(get_db)):
    products = db.query(models.Products).all()
    return products


# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductCreate)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductOut)
def create_product(product : schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Products(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ProductOut)
def get_one_product(id:int, db:Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == id)
    if product.first() is None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id {id} not found")
    
    return product.first()


# @router.put("/{id}", response_model=schemas.ProductUpdate)
@router.put("/{id}", response_model=schemas.ProductOut)
def update_product(id:int, product : schemas.ProductUpdate, db:Session = Depends(get_db)):
    update_pro = db.query(models.Products).filter(models.Products.id == id)

    if update_pro.first() is None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"product of id {id} was not found")

    update_pro.update(product.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()

    return update_pro.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db:Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == id)
    if product.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product of id{id} not found")
    
    db.delete(product.first())
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)