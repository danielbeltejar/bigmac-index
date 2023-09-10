import asyncio

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

app = FastAPI()
app.include_router(health_router)
app.include_router(actual_prices_router)
app.include_router(price_history_router)

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Create an instance of the scheduled task scheduler `SchedulerAdmin`
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))
scheduler = SchedulerAdmin.bind(site)


mysql = MySQL()


@scheduler.scheduled_job('interval', hours=6)
async def scrape():
    ScrapeTask()
    await get_latest_prices_async()


@app.on_event("startup")
async def startup():
    # Start the scheduled task scheduler
    scheduler.start()
    asyncio.create_task(get_latest_prices_async())

