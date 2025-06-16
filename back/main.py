import asyncio
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.ActualPricesRouter import actual_prices_router, get_latest_prices_async
from src.routers.PriceHistoryRouter import price_history_router
from src.routers.HealthRouter import health_router
from src.sql.MySQL import MySQL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


try:
        mysql = MySQL()

        asyncio.create_task(get_latest_prices_async())
        logger.info("Background task for price fetching created")

        get_latest_prices_async()
        logger.info("Initial price fetch completed")

except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


app = FastAPI()
app.include_router(health_router)
app.include_router(actual_prices_router)
app.include_router(price_history_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development
    allow_methods=["GET"],
    allow_headers=["*"],
)

