from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import products,orders
from fastapi.responses import JSONResponse


app = FastAPI(title="E-Commerce API", version="1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

app.include_router(products.router)
app.include_router(orders.router)



@app.get("/")
async def root():
    return JSONResponse(content={
        "message": "E-Commerce API!",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": [
            {"path": "/products", "description": "Retrieve and manage products"},
            {"path": "/orders", "description": "Place and retrieve orders"}
        ]
    })