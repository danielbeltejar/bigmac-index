import json

from _decimal import Decimal

from fastapi import requests
from forex_python.converter import CurrencyRates, RatesNotAvailableError


class MySQLGet(object):

    def __init__(self):
        pass


    @staticmethod
    def get_price_history(country: str):
        from main import mysql
        connector = mysql.get_connector()
        cursor = connector.cursor()

        with open('config/mcdonalds_stores.json', 'r', encoding='utf-8') as file:
            countries = json.load(file)

        currencies = {country['country']: country['currency'] for country in countries}

        query = f"""
            SELECT DISTINCT  bp.country, bp.price, bp.date
            FROM bigmac_prices AS bp
            WHERE bp.country = '{country}';
        """

        # Ejecutar la consulta
        cursor.execute(query)
        results = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()

        results_with_currency = [
            (
                str(date), price,
            )
            for country, price, date in results
        ]

 ##       if len(results_with_currency) == 1:
 ##           fake_value = ("2023-06-06", (results[0][1]) - Decimal(0.001))
 ##           results_with_currency.insert(0, fake_value)

        return results_with_currency

    @staticmethod
    def get_latest_prices():
        from main import mysql
        connector = mysql.get_connector()
        cursor = connector.cursor()

        with open('config/mcdonalds_stores.json', 'r', encoding='utf-8') as file:
            countries = json.load(file)

        country_names = [country['country'] for country in countries]
        currencies = {country['country']: country['currency'] for country in countries}

        query = """
            SELECT bp.country, bp.price, bp.date
            FROM bigmac_prices AS bp
            INNER JOIN (
                SELECT country, MAX(ID) AS max_id
                FROM bigmac_prices
                GROUP BY country
            ) AS max_ids
            ON bp.country = max_ids.country AND bp.ID = max_ids.max_id
            WHERE bp.country IN ({});
        """

        placeholders = ','.join(['%s'] * len(country_names))
        query = query.format(placeholders)
        cursor.execute(query, country_names)
        results = cursor.fetchall()
        cursor.close()

        # Initialize the currency converter
        c = CurrencyRates()

        # Add currency information to the tuples
        results_with_currency = []
        for country, price, date in results:
                currency = currencies[country.lower()]
                usd_price = c.convert(currency, 'USD', float(price))
                results_with_currency.append((country, price, str(date), currency, usd_price))

        return results_with_currency
