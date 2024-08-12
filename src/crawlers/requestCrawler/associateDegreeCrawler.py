import logging
import pprint
import pandas
import queue
import requests
import time

from .baseHTTPCrawler import BaseHTTPCrawler


class AssociateDegreeCrawler(BaseHTTPCrawler):
    def __init__(self) -> None:
        super().__init__()
        self.DEFAULTURL = "https://api.zjzw.cn/web/api/?keyword=&level1=2&level2=&level3=&page=1&size=30&sort=&uri=apidata/api/gkv3/special/lists"
        self.setUri("apidata/api/gkv3/special/lists")
        self.jsonForm = {
            "keyword": "",
            "level1": "2",
            "level2": "",
            "level3": "",
            "page": 1,
            "signsafe": "",
            "size": 30,
            "sort": "",
            "uri": "apidata/api/gkv3/special/lists",
        }
        self.majorData: list = []

    @BaseHTTPCrawler.proxyUpdate(5)
    def crawl(self):
        time.sleep(1)
        maxPage = 26
        for page in range(1, maxPage):
            #print(f'正在使用的IP为:{self.proxies}')
            responseUrl: str = self.iterPage(self.DEFAULTURL, page)
            responseUrl = self.iterSignSafe(responseUrl)
            try:
                response = requests.post(
                    responseUrl,
                    headers=self.headers,
                    data=self.jsonForm,
                    proxies=self.proxies,
                    timeout=3
                )
            except TimeoutError:
                page-=1
                #self.getProxy()
                print("代理ip失效:TimeoutError")
                continue
            except requests.exceptions.ProxyError:
                page-=1
                #self.getProxy()
                print("代理ip失效:ProxyError")
                pprint.pprint(self.proxies)
                continue
            resultDict = response.json()
            response.close()
            print(f"正在爬取第{page}页",resultDict)
            self.storageData(resultDict)
            time.sleep(1)
        #self.writeData(self.majorData)

    def storageData(self, dataDict: dict) -> None:
        longNumber = len(dataDict["data"]["item"])
        for i in range(longNumber):
            temp = dataDict["data"]["item"][i]
            self.majorData.append(
                [
                    temp["level2_name"],
                    temp["level3_name"],
                    temp["name"],
                    temp["special_id"],
                ]
            )

    def writeData(self, dataList: list) -> None:
        dataFrom = pandas.DataFrame(dataList, columns=['bigGroup', 'smallGroup', 'majorName', 'majorId'])
        tempJson = dataFrom.to_json(orient='records', force_ascii=False)
        with open(BaseHTTPCrawler._positioningPath() + "\\associateDegreeID.json", 'w', encoding='UTF-8') as f:
            f.write(tempJson)

    def admissionConstitutionCrawler(self,number):
        self.DEFAULTURL = f"https://static-data.gaokao.cn/www/2.0/school/{number}/news/list.json"
        response = requests.post(
            self.DEFAULTURL,
            headers=self.headers,
            data=self.jsonForm,
            proxies=self.proxies,
            timeout=3
        )
        print(response.text)

