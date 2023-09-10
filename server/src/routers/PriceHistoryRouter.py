import asyncio
import json
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict

from fastapi import APIRouter
from fastapi import status, Response

from src.sql.MySQLGet import MySQLGet

price_history_router = APIRouter()
logger = logging.getLogger()

cache: Dict = {}


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


@price_history_router.get('/prices/history/{country}', status_code=status.HTTP_200_OK)
async def actual_prices(response: Response, country: str):
    result = MySQLGet.get_price_history(country)

    response.headers["Content-Type"] = "application/json"
    return Response(json.dumps(result, cls=DecimalEncoder), media_type='application/json')
