from fastapi import FastAPI
from . import models
from .database import engine 
from .routers import product, category, user, auth, cart, order
from .config import settings

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(product.router)
app.include_router(category.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(cart.router)
app.include_router(order.router)


@app.get("/")
def root():
    return {"Status" : "OK"}