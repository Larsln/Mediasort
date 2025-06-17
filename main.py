from folder_crawler import FolderCrawler
from static_data_loader import StaticDataLoader

staticDataLoader = StaticDataLoader()
folderCrawler = FolderCrawler(staticDataLoader)
folderCrawler.crawl(StaticDataLoader.input_path)
