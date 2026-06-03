from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import couriers, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Candy Delivery API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(couriers.router)
app.include_router(orders.router)