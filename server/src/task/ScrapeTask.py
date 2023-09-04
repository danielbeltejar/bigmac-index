import json

from src.task.Task import Task
from src.worker.PriceScraperWorker import PriceScraperWorker


class ScrapeTask(Task):

    def __init__(self):
        super().__init__()

    def _start(self):
        with open('config/mcdonalds_stores.json') as file:
            data = json.load(file)

        [PriceScraperWorker(url=store['url'], country=store['country'], currency=store['currency']) for store in data]

    def _stop(self):
        pass
