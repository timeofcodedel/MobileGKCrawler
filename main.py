import json
import requests
import pprint
from src.crawlers.requestCrawler.universityScoresCrawler import UniversityScoresCrawler

if __name__ == "__main__":
   a=UniversityScoresCrawler()
   a.crawl()