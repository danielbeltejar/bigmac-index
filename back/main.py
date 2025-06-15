import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_scheduler import SchedulerAdmin

from src.routers.ActualPricesRouter import actual_prices_router, get_latest_prices_async
from src.routers.PriceHistoryRouter import price_history_router
from src.routers.HealthRouter import health_router
from src.sql.MySQL import MySQL
from src.task.ScrapeTask import ScrapeTask

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize scheduler and site globally
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))
scheduler = SchedulerAdmin.bind(site)



try:
        scheduler.start()
        logger.info("Scheduler started successfully")

        # Create background task for initial price fetch
        asyncio.create_task(get_latest_prices_async())
        logger.info("Background task for price fetching created")

        # Run initial scrape
        ScrapeTask()
        logger.info("Initial scrape task completed")

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


# mysql = MySQL()

@scheduler.scheduled_job('interval', hours=6)
async def scrape():
    logger.info("Running scheduled scrape task")
    ScrapeTask()
    await get_latest_prices_async()