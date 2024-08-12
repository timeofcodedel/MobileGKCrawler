import asyncio
import aiohttp
import base64
import hashlib
import hmac
import re
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from urllib.parse import unquote


class AsyncBaseCrawler(object):
    def __init__(self) -> None:
        super().__init__()
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
        self.jsonData: dict
        self.proxies: str = ""
        self.DEFAULTURL = "https://api.zjzw.cn/web/api/?is_single=2&local_province_id=44&page=1&province_id=&request_type=1&size=20&special_id=1&type=&uri="

    async def _cleanUrl(self, url: str) -> str:
        return re.sub(r"^/|https?:///?", "", url)

    async def getSignSafe(self, URL: str):
        p = "D23ABC@#56"
        # 示例:URL = "api.zjzw.cn/web/api/?is_single=2&local_province_id=44&page=1&province_id=&request_type=1&size=20&special_id=1&type=&uri=apidata/api/gk/special/school"
        URL = await self._cleanUrl(URL)
        t = {"SIGN": p, "str": URL}

        # 解码URL
        n = unquote(t["str"])

        # 计算HMAC-SHA1
        hmacSha1 = hmac.new(p.encode("utf-8"), n.encode("utf-8"), hashlib.sha1).digest()

        # Base64编码
        base64Encoded = base64.b64encode(hmacSha1).decode("utf-8")

        # MD5哈希
        md5_hash = hashlib.md5(base64Encoded.encode("utf-8")).hexdigest()

        return md5_hash

    async def iterPage(self, url: str, index: int) -> str:
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
        self.jsonData["page"] = index
        return url[:startIndex] + str(index) + url[endIndex:]

    async def iterID(self, url: str, ID: int) -> str:
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
        self.jsonData["special_id"] = ID
        return url[:startIndex] + str(ID) + url[endIndex:]

    async def iterUri(self, url: str, uri: str) -> str:
        """
        根据URI迭代URL中的uri参数。

        参数:
        - url: str: 原始URL。
        - uri: str: 目标URI。

        返回:
        修改后的URL。
        """
        startIndex = url.find("uri=") + len("uri=")
        self.jsonData["uri"] = uri
        return url[:startIndex] + str(uri)

    async def iterSignSafe(self, url: str) -> str:
        signsafe = await self.getSignSafe(url)
        self.jsonData["signsafe"] = signsafe
        return url + "&signsafe=" + signsafe

    @staticmethod
    def proxyUpdate(updateTimes: int):
        def decorator(func):
            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                def runTimer():
                    while True:
                        self.getProxyIP()
                        time.sleep(updateTimes)
                t=threading.Thread(target=runTimer)
                t.daemon=True
                t.start()

                result = await func(self, *args, **kwargs)
                return result

            return wrapper

        return decorator
    async def setSignSafe(self, signsafeStr: str) -> None:
        """
        设置请求参数中的signsafe值。

        参数:
        - signsafeStr: str: signsafe值。
        """
        self.jsonData["signsafe"] = signsafeStr
    async def setSpecialId(self, specialId) -> None:
        """
        设置请求参数中的special_id值。

        参数:
        - specialId: 目标special_id值。
        """
        self.jsonData["special_id"] = specialId

    async def setUri(self, uri: str) -> None:
        """
        设置请求参数中的uri值。

        参数:
        - uri: str: 目标uri值。
        """
        self.jsonData["uri"] = uri

    async def setPage(self, pageNumber: int) -> None:
        """
        设置请求参数中的page值。

        参数:
        - pageNumber: int: 目标页码。
        """
        self.jsonData["page"] = pageNumber

    async def setArgs(self, *args, **kwargs) -> None:
        """
        批量设置请求参数。

        参数:
        - *args: 位置参数，按索引设置参数值。
        - **kwargs: 关键字参数，按名称设置参数值。
        """
        for index, value in enumerate(args):
            self.jsonData[str(index)] = value
        self.jsonData.update(kwargs)
    def getProxyIP(self) -> None: 
        """
        更新当前使用的代理IP.
        """
        print("Aaaaaaaaaaaaaa")
        ip = self.extractIp()
        if ip is None:
            return None
        self.proxies = f"http://{ip}"
        print(f"代理IP更新成功！,当前ip为{ip}")
    def extractIp(self) -> str|None:
        whiteListCertification = "https://api2.docip.net/v1/set_whitelist?api_key=D9sGK2KbLTxlebj798ISwm66b08119&whitelist=192.168.30.101"
        activeExtraction="https://api2.docip.net/v1/get_proxy?api_key=D9sGK2KbLTxlebj798ISwm66b08119&time=60&format=json&num=1"
        certificationResponse = requests.get(whiteListCertification)
        certificationResponse.close()
        # 主动提取接口
        activeExtractionResponse = requests.get(activeExtraction)
        resultIP = activeExtractionResponse.json()
        if resultIP==[]:
            return None
        else:
            return resultIP[0]


if __name__ == "__main__":
    c=AsyncBaseCrawler()
    @AsyncBaseCrawler.proxyUpdate(10)
    async def main():
        print(c.proxies)
    asyncio.run(main())
