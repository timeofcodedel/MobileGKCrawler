import os
import time
import threading
import queue

from functools import wraps
from .proxyApi import extractIp

from ...signsafeparse.signsafeParser import getSignSafe


class BaseHTTPCrawler(object):
    """
    一个基础的HTTP爬虫类，提供了代理IP更新、请求头设置、请求参数设置等功能。
    """

    def __init__(self) -> None:
        # 初始化请求头
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.gaokao.cn",
            "priority": "u=1, i",
            "referer": "https://www.gaokao.cn/",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }
        # 初始化请求参数
        self.jsonForm: dict = {
            "is_single": 2,
            "local_province_id": "44",
            "page": 1,
            "province_id": "",
            "request_type": 1,
            "signsafe": "",
            "size": 20,
            "special_id": "1",
            "type": "",
            "uri": " ",
        }
        # 初始化代理IP
        self.proxies: dict = {}
        # 默认URL
        self.DEFAULTURL = "https://api.zjzw.cn/web/api/?is_single=2&local_province_id=44&page=1&province_id=&request_type=1&size=20&special_id=1&type=&uri="


    def iterPage(self, url: str, index: int) -> str:
        """
        根据页码迭代URL中的page参数。

        参数:
        - url: str: 原始URL。
        - index: int: 目标页码。

        返回:
        修改后的URL。
        """
        startIndex = url.find("page=") + len("page=")
        endIndex = url.find("&", startIndex)
        self.jsonForm["page"] = index
        return url[:startIndex] + str(index) + url[endIndex:]

    def iterID(self, url: str, ID: int) -> str:
        """
        根据ID迭代URL中的special_id参数。

        参数:
        - url: str: 原始URL。
        - ID: int: 目标ID。

        返回:
        修改后的URL。
        """
        startIndex = url.find("special_id=") + len("special_id=")
        endIndex = url.find("&", startIndex)
        self.jsonForm["special_id"] = ID
        return url[:startIndex] + str(ID) + url[endIndex:]

    def iterUri(self, url: str, uri: str) -> str:
        """
        根据URI迭代URL中的uri参数。

        参数:
        - url: str: 原始URL。
        - uri: str: 目标URI。

        返回:
        修改后的URL。
        """
        startIndex = url.find("uri=") + len("uri=")
        self.jsonForm["uri"] = uri
        return url[:startIndex] + str(uri)

    def iterSignSafe(self, url: str) -> str:
        signsafe = getSignSafe(url)
        self.jsonForm["signsafe"] = signsafe
        return url + "&signsafe=" + signsafe

    @staticmethod
    def proxyUpdate(updateTimes: int):
        """
        该函数是一个装饰器，用于定时更新代理IP。

        参数:
        - updataTimes:int: 更新代理IP的时间间隔(秒)。

        返回:
        装饰器函数。

        Usage:
        >>>@BaseHTTPCrawler.proxyUpdate(60)
        >>>def crawl():
        """

        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                def runTimer():
                    while True:
                        self.getProxyIP()
                        time.sleep(updateTimes)

                timerThread = threading.Thread(target=runTimer)
                timerThread.daemon = True
                timerThread.start()

                result = func(self, *args, **kwargs)
                return result

            return wrapper

        return decorator

    @staticmethod
    def _positioningPath() -> str:
        """
        定位并返回数据文件的存储路径。

        返回:
        存储数据的文件路径。
        """
        filePath = os.path.abspath(__file__)
        currentDir = os.path.dirname(filePath)
        projectRoot = os.path.dirname(os.path.dirname(os.path.dirname(currentDir)))
        dataFilePath = os.path.join(projectRoot, "data")
        return dataFilePath

    def setSignSafe(self, signsafeStr: str) -> None:
        """
        设置请求参数中的signsafe值。

        参数:
        - signsafeStr: str: signsafe值。
        """
        self.jsonForm["signsafe"] = signsafeStr

    def setSpecialId(self, specialId) -> None:
        """
        设置请求参数中的special_id值。

        参数:
        - specialId: 目标special_id值。
        """
        self.jsonForm["special_id"] = specialId

    def setUri(self, uri: str) -> None:
        """
        设置请求参数中的uri值。

        参数:
        - uri: str: 目标uri值。
        """
        self.jsonForm["uri"] = uri

    def setPage(self, pageNumber: int) -> None:
        """
        设置请求参数中的page值。

        参数:
        - pageNumber: int: 目标页码。
        """
        self.jsonForm["page"] = pageNumber

    def setArgs(self, *args, **kwargs) -> None:
        """
        批量设置请求参数。

        参数:
        - *args: 位置参数，按索引设置参数值。
        - **kwargs: 关键字参数，按名称设置参数值。
        """
        for index, value in enumerate(args):
            self.jsonForm[str(index)] = value
        self.jsonForm.update(kwargs)


    def getProxyIP(self) -> None:
        """
        更新当前使用的代理IP.
        """
        ip = extractIp()
        if ip is None:
            return None
        self.proxies = {"http": f"http://{ip}"}
        print(f"代理IP更新成功！,当前ip为{ip}")


if __name__ == "__main__":
    pass
