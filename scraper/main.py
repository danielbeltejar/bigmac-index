import logging
from src.task.ScrapeTask import ScrapeTask
from src.sql.MySQL import MySQL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mysql = MySQL()


def main():
    ScrapeTask()
    logger.info("Initial scrape task completed")

if __name__ == "__main__":
    main()