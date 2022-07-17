from multiprocessing import Process

from fastapi import FastAPI

from app.db import create_db_and_tables
from app.routers import login, products
from app.utils import get_offers_loop

app = FastAPI(title="Product aggregator")

app.include_router(login.router)
app.include_router(products.router)


p = Process(target=get_offers_loop)


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
    p.start()


@app.on_event("shutdown")
async def on_shutdown():
    p.terminate()


@app.get("/", tags=["Index"])
def index():
    return "Hello there"
