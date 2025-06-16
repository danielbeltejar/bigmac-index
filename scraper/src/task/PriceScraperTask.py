import time

from src.task.Task import Task
from src.util.Country import Country


class PriceScraperTask(Task):
    _url: str
    _price: int
    _country: Country
    _currency: str

    def __init__(self, country: Country, url: str, currency: str):
        self._country = country
        self._url = url
        self._currency = currency
        super().__init__()

    def _start(self):
        try:
            self._pre_run()
            attempts = 0
            while attempts < 10:
                self.run()
                time.sleep(1)
                attempts += 1
                if self._price is not None:
                    break
            self._post_run()
        except Exception as e:
            print(e)

    def _stop(self):
        pass

    def _pre_run(self):
        pass

    def run(self):
        raise NotImplementedError

    def _post_run(self):
        pass

    def get_url(self) -> str:
        return self._url
