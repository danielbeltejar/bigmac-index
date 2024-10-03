from unicodedata import decimal

from src.sql.MySQLGet import exchange
from src.task.ScrapeTask import ScrapeTask


print(round(exchange("PLN", 'USD', 3.35),2))
#ScrapeTask()
