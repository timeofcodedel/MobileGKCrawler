import random
import requests
import re
import time
import json
import pprint
import os

from typing import Union

from ...signsafeparse.signsafeParser import getSignSafe
from .baseHTTPCrawler import BaseHTTPCrawler


class MajorDetailCrawler(BaseHTTPCrawler):
    def __init__(self) -> None:
        super().__init__()
        self._dataDict: dict = {}

    def crawl(self):
        if self.jsonForm["uri"] is None:
            raise ValueError("接口uri地址不可为空")
        proxies = {
            "https": "https://175.6.171.225:30000"
        }
        majorData: dict = self._loadJson()
        # 历遍外层键和值 分别是大类名和小类字典
        for outerKey, outerDict in majorData.items():
            # 历遍内层键值，分别是小类名和url列表
            tempDict: dict = {}  # 储存所有小类的数据
            for innerKey, innerList in outerDict.items():
                datadict: dict = {}
                # 历遍每一个url
                for url in innerList:
                    resultList: list = []
                    majorName: str = url.split(":")[2]
                    requestUrl = self.initUrl(self._extractSpecialNumber(url), 1)  # type: ignore
                    # 历遍一个专业里面的所有页数
                    for index in range(1, 200):
                        requestUrl = self.iterUrl(requestUrl, index)
                        response = requests.post(requestUrl, json=self.jsonForm, headers=self.headers,proxies=proxies)  # type: ignore
                        if response.status_code == 200:
                            tempContainer: dict = response.json()
                            if len(tempContainer["data"]["item"]) == 0:
                                print(f"现在爬取完成的专业是{outerKey}下的{innerKey}的{majorName}专业")
                                response.close()
                                break
                            else:
                                resultList.extend(
                                    self._extractName(tempContainer["data"]["item"])
                                )

                                response.close()
                        else:
                            raise ConnectionError(
                                f"请求失败 错误代码为:{response.status_code}"
                            )
                    datadict[majorName] = datadict.get(majorName, resultList)
                    time.sleep(3)
                tempDict[innerKey] = tempDict.get(innerKey, datadict)
            self._dataDict[outerKey] = tempDict

        with open(
            os.path.join(self._positioningPath(), "majorData.json"),
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(self._dataDict, file, ensure_ascii=False, indent=False)
            file.write("\n")

    def _extractName(self, responseData: list) -> list:
        resultList: list = []
        for item in responseData:
            resultList.append(item["name"])
        return resultList

    def _extractSpecialNumber(self, url: str) -> int | None:
        match = re.search(r"special/(\d+)", url)
        if match:
            return int(match.group(1))
        else:
            return None  # type: ignore

    def _getSignSafe(self):
        self.signsafe = getSignSafe(self.URL)

    def initUrl(self, specialId: int, pageNumber: int) -> str:
        url=f"https://api.zjzw.cn/web/api/?is_single=2&local_province_id=44&page={pageNumber}&province_id=&request_type=1&size=20&special_id={specialId}&type=&uri=apidata/api/gk/special/school"
        self.jsonForm["special_id"] = specialId
        self.jsonForm["page"] = pageNumber
        self.jsonForm["signsafe"] = getSignSafe(self.URL)
        return url + f"&signsafe={self.jsonForm['signsafe']}"

    def iterUrl(self, url: str, index: int) -> str:
        startIndex = url.find("page=") + len("page=")
        endIndex = url.find("&", startIndex)
        self.jsonForm['page']=index
        return url[:startIndex] + str(index) + url[endIndex:]

    def _loadJson(self):
        with open(
            os.path.join(BaseHTTPCrawler._positioningPath(), "urls.json"),
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)
        return data


if __name__ == "__main__":
    pass
