import requests
from baseCrawler import BaseCrawler
from bs4 import BeautifulSoup

if __name__ == "__main__":
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.gaokao.cn',
    'priority': 'u=1, i',
    'referer': 'https://www.gaokao.cn/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

json_data = {
    'is_single': 2,
    'local_province_id': '44',
    'page': 1,
    'province_id': '',
    'request_type': 1,
    'signsafe': '3fbcc8c199609130c4f1c5e092387ad6',
    'size': 20,
    'special_id': '1',
    'type': '',
    'uri': 'apidata/api/gk/special/school',
}

response = requests.post(
    'https://api.zjzw.cn/web/api/?is_single=2&local_province_id=44&page=1&province_id=&request_type=1&size=20&special_id=1&type=&uri=apidata/api/gk/special/school&signsafe=3fbcc8c199609130c4f1c5e092387ad6',
    headers=headers,
    json=json_data,
)

path = BaseCrawler._positioningPath()
with open(path+"\\"+"test.html","w",encoding="utf-8") as f:
    f.write(response.text)