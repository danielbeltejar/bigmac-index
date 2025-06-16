import datetime

from _decimal import Decimal


class MySQLInsert(object):

    def __init__(self, country: str, price: Decimal):
        from main import mysql
        connector = mysql.get_connector()
        cursor = connector.cursor()

        # Check if the latest price for the country is different
        latest_price = self.get_latest_price(cursor, country)
        if latest_price != price:
            # Prepare the insert query
            query = "INSERT INTO bigmac_prices (country, date, price) VALUES (%s, %s, %s)"
            insert_data = (country, datetime.datetime.today().date(), price)

            # Execute the query
            cursor.execute(query, insert_data)
            connector.commit()
            print("New price inserted.")
        else:
            print("Skipping insertion, last price for", country, "was already", price)

        # Close the cursor and connection
        cursor.close()

    @staticmethod
    def get_latest_price(cursor, country):
        # Retrieve the latest price for the country from the database
        query = "SELECT price FROM bigmac_prices WHERE country = %s ORDER BY date DESC LIMIT 1"
        cursor.execute(query, (country,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
