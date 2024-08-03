import requests
import logging
from ssl import SSLError
headers: dict = {
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
    logger = logging.getLogger('errorLogger')
    logger.setLevel(logging.DEBUG) 
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) 
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
def getProxy() -> list:
    logger=setupLogger()
    ipurl: list[str] = extractIp()
    resultList: list = []
    for ip in ipurl:
        proxies = {"http": f"http://{ip}", "https": f"https://{ip}"}
        try:
            response = requests.get('http://httpbin.org/ip', proxies=proxies, headers=headers,timeout=4)
            if response.status_code == 200:
                if "223.73.93.3" not in response.json()["origin"] :
                    logging.debug(f"{ip} is working | ip is {response.json()['origin']}")
                    resultList.append(ip)
        except requests.exceptions.ProxyError:
            logger.debug(f"{ip} is not working error:{'requests.exceptions.ProxyError'}")
            continue
        except requests.exceptions.ConnectionError:
            logger.debug(f"{ip} is not working error:{'requests.exceptions.ConnectionError'}")
            continue
        except requests.exceptions.ReadTimeout:
            logger.debug(f"{ip} is not working error:{'requests.exceptions.ReadTimeout'}")
            continue
        except SSLError:
            logger.debug(f"{ip} is not working error:{'SSLError'}")
            continue
        except RuntimeError:
            logger.debug(f"{ip} is not working error:{'RuntimeErro'}")
            continue
        except ConnectionError:
            logger.debug(f"{ip} is not working error:{'ConnectionError'}")
            continue
    return resultList


def extractIp() -> list:
    url = "https://api.docip.net/v1/get_openproxy?api_key=QEf10Ji1nTj8hnbzhcfHix66aa67c0&format=json&num=10"
    r = requests.get(url).json()
    return r


if __name__ == "__main__":
    getProxy()
