import logging
from http import HTTPStatus

from fastapi import APIRouter
from fastapi import status

from src.routers import ActualPricesRouter

health_router = APIRouter()
logger = logging.getLogger()


@health_router.get('/healthz')
async def heath_check():
    if len(ActualPricesRouter.cache) != 0:
        return HTTPStatus.OK
    return HTTPStatus.SERVICE_UNAVAILABLE
