import json
import re
import time
from datetime import datetime, timedelta

import requests
from _decimal import Decimal
from bs4 import BeautifulSoup
from mechanize import Browser

from src.sql.MySQLInsert import MySQLInsert
from src.task.PriceScraperTask import PriceScraperTask


class PriceScraperWorker(PriceScraperTask):

    def run(self):
        """
        This method implements the run method of PriceScraperTask.
        It extracts the price and currency for a menu item from a given URL
        using Beautiful Soup and JSON parsing.
        """
        time.sleep(0.1)

        # Start the timer
        start_time = time.time()

        # Use mechanize to avoid UberEats protection
        b = Browser()
        b.set_handle_robots(False)
        b.addheaders = [('Referer', 'https://www.google.com'), ('User-agent',
                                                                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')]

        try:
            b.open(self.get_url())
        except:
            print(f"Request failed. Status code: {b.response().code} for URL: " + self.get_url())
            return

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(b.response().read(), 'html.parser')

        # Find the script tag containing the JSON data
        script_tags = soup.select('script[type="application/ld+json"]')
        script_tags += soup.select('script[type="application/json"]')
        bigmac_name = ["big mac", "big mac®", "hamburguesa bigmac", "Hamburguesa Big Mac", "big mac™", "big mac ™", "big mac [560.0 cals]",
                       "Big Mac [560.0 Cals]", "ビッグマック Big Mac", "McCombo Big Mac"]

        menu_jsons = []
        for script_tag in script_tags:
            if script_tag.string.lower().__contains__("big mac"):
                menu_jsons.append(script_tag)

        # Loop through each script tag containing the JSON data
        for script_tag in menu_jsons:
            if not script_tag.string.__contains__("hasMenuSection"):
                continue
            # Parse the JSON data
            if script_tag.string.__contains__("u0022"):
                if script_tag.text.__contains__("%5C"):
                    data = json.loads(script_tag.text.replace("\\u0022", '"').replace("%5C", "\\"))
                else:
                    data = json.loads((script_tag.string.encode().decode('unicode_escape')))
            else:
                data = json.loads(script_tag.string)

            self._price: Decimal = self.find_price_by_title(data, bigmac_name)

            # Check if any menu items were found
            if self._price is not None:
                    # Print the price, country and currency of the menu item
                    print("=" * 50)
                    print(f"Big Mac: {self._price} {self._currency} {self._country}")

                    # Print the time taken to scrape the menu item
                    print(f"Scraped in {(time.time() - start_time) * 1000:.2f} ms.")
                    MySQLInsert(country=str(self._country).title().upper(), price=self._price)
                    print("=" * 50)

    def find_price_by_title(self, data, title_variations):
        if isinstance(data, dict):
            for title in title_variations:
                if "title" in data and str(data["title"]).lower() == title.lower():
                    numeric_value = data.get("priceTagline").get("text")

                    if numeric_value.__contains__(".") and numeric_value.__contains__(","):
                        numeric_value = numeric_value.replace(",", "")
                        numeric_value = numeric_value.split(".")[0].replace(".", "")

                    elif numeric_value.__contains__(",") and len(numeric_value.split(",")[1]) > 2:
                        numeric_value = numeric_value.replace(",", "")

                    numeric_value: str = numeric_value.replace(" ", "").replace(',', '.')
                    numeric_value = re.findall(r'[\d,]+\.*\d*', numeric_value)[0]
                    numeric_value = numeric_value.replace(".00", "")
                    return Decimal(numeric_value)
            for value in data.values():
                result = self.find_price_by_title(value, title_variations)
                if result is not None:
                    return Decimal(result)
        elif isinstance(data, list):
            for item in data:
                result = self.find_price_by_title(item, title_variations)
                if result is not None:
                    return Decimal(result)
        return None
