import json
import requests
import pprint
from src.crawlers.requestCrawler.associateDegreeCrawler import AssociateDegreeCrawler
if __name__ == "__main__":
   test = AssociateDegreeCrawler()
   test.crawl()