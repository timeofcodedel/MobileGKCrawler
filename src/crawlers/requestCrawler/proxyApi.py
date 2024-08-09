import pprint
import requests
import logging
from ssl import SSLError

headers = {
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


def setupLogger():
    logger = logging.getLogger("Logger")
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def getProxy() -> list | None:
    logger = setupLogger()
    ip: str|None = extractIp() # type: ignore
    if ip is []:
        return None

    proxies = {"http": f"http://{ip}"}
    try:
        response = requests.get(
            "https://ipinfo.io/json", headers=headers, proxies=proxies
        )
        if response.status_code == 200:
             # type: ignore
            response.close()
            if ip == []:
                return None
            elif ip != []:
                logger.info("正在使用的ip为:"+ip[0]) # type: ignore
                return ip[0] #type:ignore
    except requests.exceptions.ProxyError:
        logger.debug(f"{ip} is not working error:{'requests.exceptions.ProxyError'}")
        return extractIp()[0]#type: ignore


def extractIp() -> list|None:
    whiteListCertification = "https://api2.docip.net/v1/set_whitelist?api_key=D9sGK2KbLTxlebj798ISwm66b08119&whitelist=192.168.0.107"
def extractIp() -> str|None:
    whiteListCertification = "https://api2.docip.net/v1/set_whitelist?api_key=D9sGK2KbLTxlebj798ISwm66b08119&whitelist=192.168.30.101"
    certificationResponse = requests.get(whiteListCertification)
    certificationResponse.close()
    # 主动提取接口
    activeExtractionResponse = requests.get(
        "https://api2.docip.net/v1/get_proxy?api_key=D9sGK2KbLTxlebj798ISwm66b08119&time=300&format=json&num=1"
    )
    print(activeExtractionResponse)
    resultIP = activeExtractionResponse.json()
    if resultIP==[]:
        return None
    else:
        return resultIP[0]


if __name__ == "__main__":
    extractIp()
