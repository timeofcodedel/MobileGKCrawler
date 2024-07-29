import requests
from ...signsafeparse.signsafeParser import getSignSafe
from .baseHTTPCrawler import BaseHTTPCrawler

class MajorDetailCrawler(BaseHTTPCrawler):
    def __init__(self) -> None:
        super().__init__()
        self.signsafe:str=""
        self.pageNumber:int=1
        self.URL=f'https://api.zjzw.cn/web/api/?is_single=2&local_province_id=44&page={self.pageNumber}&province_id=&request_type=1&size=20&special_id=1&type=&uri=apidata/api/gk/special/school&signsafe={self.signsafe}'
    def crawl(self,uri:str):
        
        response=requests.post(self.URL,headers=self.headers,data=self.jsonForm)
    def _getSignSafe(self):
        self.signsafe=getSignSafe(self.URL)



        
if __name__ == "__main__":
    pass

  