from fastapi import FastAPI
from . import models
from .database import engine 
from .routers import product, category, user, auth, cart, order
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
import logging

models.Base.metadata.create_all(bind = engine)
app = FastAPI()

logger = logging.getLogger("uvicorn.error")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.method} {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    
    allow_credentials=True,    
    allow_methods=["*"],        
    allow_headers=["*"],   
    )    

app.include_router(product.router)
app.include_router(category.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(cart.router)
app.include_router(order.router)


@app.get("/")
def root():
    return {"Status" : "OK"}