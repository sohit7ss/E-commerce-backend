# app/routers/category.py


from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from typing import List


router = APIRouter(
    prefix="/category",
    tags=["category"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.CategoryOut])
def get_all_category(db: Session = Depends(get_db)):
    category = db.query(models.Categories).all()
    return category


# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductCreate)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryOut)
def create_category(category : schemas.CategoryCreate, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.Role != "admin":
            raise HTTPException (status_code=status.HTTP_403_FORBIDDEN)
    
    new_category = models.Categories(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.CategoryOut)
def get_one_category(id:int, db:Session = Depends(get_db)):
    category = db.query(models.Categories).filter(models.Categories.id == id)
    if category.first() is None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id {id} not found")
    
    return category.first()


# @router.put("/{id}", response_model=schemas.ProductUpdate)
@router.put("/{id}", response_model=schemas.CategoryOut)
def update_category(id:int, category : schemas.CategoryUpdate, db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if current_user.Role != "admin":
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN)
    
    update_cat = db.query(models.Categories).filter(models.Categories.id == id)

    if update_cat.first() is None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"product of id {id} was not found")

    update_cat.update(category.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()

    return update_cat.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.Role != "admin":
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN)
    
    product = db.query(models.Products).filter(models.Products.CategoryID == id)
    if product.first() :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Delete associated products first")
    
    category = db.query(models.Categories).filter(models.Categories.id == id)
    if category.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product of id{id} not found")

    db.delete(category.first())
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)