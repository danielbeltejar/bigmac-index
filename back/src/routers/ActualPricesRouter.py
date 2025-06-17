import json
import logging
from decimal import Decimal
from http import HTTPStatus
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


def get_latest_prices_async():
    print("Getting the latest prices from the database.")
    results = MySQLGet.get_latest_prices()
    json_results = json.dumps(results, cls=DecimalEncoder)
    cache['json_results'] = json_results


@actual_prices_router.get('/prices/actual', status_code=status.HTTP_200_OK)
async def actual_prices(response: Response):
    if len(cache) == 0:
        print("No cached prices.")
        return HTTPStatus.TOO_EARLY

    json_results = cache['json_results']
    response.headers["Content-Type"] = "application/json"
    return Response(json_results, media_type='application/json')
