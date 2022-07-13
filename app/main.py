from multiprocessing import Process
from fastapi import FastAPI
from app.utils.utils import offer_caller
from app.db import create_db_and_tables
from app.routers import products

app = FastAPI(title="Product aggregator")
app.include_router(products.router)

p = Process(target=offer_caller)
p.start()


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()


@app.get("/")
def index():
    return {"message": "Test"}
