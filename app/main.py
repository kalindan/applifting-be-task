from fastapi import FastAPI

from app.config import settings
from app.routers import login, products
from app.utils import get_offers_task

app = FastAPI(title="Product aggregator")

app.include_router(login.router)
app.include_router(products.router)


@app.on_event("startup")
async def on_startup():
    await get_offers_task(seconds=settings.offer_refresh_rate_sec)


@app.get("/", tags=["Index"])
async def index():
    return "Hello there"
