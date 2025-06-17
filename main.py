from folder_crawler import FolderCrawler
from logger_config import logger
from static_data_loader import StaticDataLoader




logger.info("Loading ENV")
staticDataLoader = StaticDataLoader()
logger.info("ENV loaded successfully")
folderCrawler = FolderCrawler(staticDataLoader)
logger.info("Start sorting files...")
folderCrawler.crawl(StaticDataLoader.input_path)
logger.info("Sorting completed.")
