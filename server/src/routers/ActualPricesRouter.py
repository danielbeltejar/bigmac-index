import asyncio
import json
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict

from fastapi import APIRouter
from fastapi import status, Response

from src.sql.MySQLGet import MySQLGet

actual_prices_router = APIRouter()
logger = logging.getLogger()

cache: Dict = {}


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


async def get_latest_prices_async():
    print("Getting the latest prices from the database.")
    now = datetime.now()
    cache['expiration'] = now + timedelta(hours=7)
    results = MySQLGet.get_latest_prices()
    json_results = json.dumps(results, cls=DecimalEncoder)
    cache['json_results'] = json_results


@actual_prices_router.get('/prices/actual', status_code=status.HTTP_200_OK)
async def actual_prices(response: Response):
    now = datetime.now()
    json_results = None

    if 'json_results' in cache and 'expiration' in cache and cache['expiration'] < now:
        print("Cached prices expired.")
        json_results = cache['json_results']
        asyncio.ensure_future(get_latest_prices_async())  # Run in the background without awaiting

    if len(cache) == 0:
        print("No cached prices.")
        json_results = await get_latest_prices_async()

    json_results = cache['json_results']
    response.headers["Content-Type"] = "application/json"
    return Response(json_results, media_type='application/json')
