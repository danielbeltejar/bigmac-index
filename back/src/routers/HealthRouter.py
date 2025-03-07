import logging
from http import HTTPStatus

from fastapi import APIRouter

from src.routers import ActualPricesRouter

health_router = APIRouter()
logger = logging.getLogger()


@health_router.get('/healthz')
async def heath_check():
    return HTTPStatus.OK if ActualPricesRouter.cache else HTTPStatus.SERVICE_UNAVAILABLE
