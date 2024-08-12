import json
import requests
import pprint
import asyncio
from src.crawlers.requestCrawler.scoreLinesCrawler import ScoreLineCrawler
if __name__ == "__main__":
    c=ScoreLineCrawler()
    asyncio.run(c.test())