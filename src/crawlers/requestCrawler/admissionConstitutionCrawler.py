import json
import re
import time
import requests
from requests import JSONDecodeError
from openpyxl import load_workbook
from urllib3 import HTTPSConnectionPool


#  先爬取‘https://static-data.gaokao.cn/www/2.0/school/56/news/list.json’里面要爬的招生章程位置的id、school_id、type
#  写成‘https://www.gaokao.cn/school/{school_id}/newsdetail/{type}/{id}.json’爬里面的content数据
# https://static-data.gaokao.cn/www/2.0/school/287/news/68002/211442.json
#  将数据里面的’&nbsp;‘、’\u003C/p\u003E \u003Cp\u003E‘ 写成\t再导入表格
class AdmissionConstitutionCrawler:
    def __init__(self) -> None:
        super().__init__()
        self.URL = "https://static-data.gaokao.cn/www/2.0/school/287/news/list.json"
        self.headers = {
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.gaokao.cn/',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.responseData = None
        self.majorData: list = []
        self.overallUrlName: list = []
        self.overall2024 = []
        self.processedData = []

    def initializeData(self):
        self.majorData: list = []
        self.overallUrlName: list = []
        self.overall2024 = []

    # @BaseHTTPCrawler.proxyUpdate(300)
    def firstCrawler(self, j):
        time.sleep(5)
        self.URL = f"https://static-data.gaokao.cn/www/2.0/school/{j}/news/list.json"
        try:
            response = requests.get(self.URL, self.headers)
            overall = response.json()['data']
            print(self.URL)
            for i in overall:
                if ('2024' in i['title'] and '招生' in i['title']) and ('章程' in i['title'] or '简章' in i['title']):
                    # print(f'成功的url:{self.URL}', i)
                    self.overall2024 += [i]
            self.firstDataTreating()
        except JSONDecodeError:
            pass
        except HTTPSConnectionPool:
            try:
                response = requests.get(self.URL, self.headers)
                overall = response.json()['data']
                print(self.URL)
                for i in overall:
                    if ('2024' in i['title'] and '招生' in i['title']) and (
                            '章程' in i['title'] or '简章' in i['title']):
                        # print(f'成功的url:{self.URL}', i)
                        self.overall2024 += [i]
                self.firstDataTreating()
            except:
                pass
        #  全部的招生章程网址的相关数据爬取

    def firstDataTreating(self):
        for i in self.overall2024:
            self.overallUrlName += [
                [f'https://static-data.gaokao.cn/www/2.0/school/{i["school_id"]}/news/{i["type"]}/{i["id"]}.json',
                 i['title']]]
        # print(self.overallUrlName)
        return self.overallUrlName
        # 提取出相关的数据id、school_id、type形成新的url

    # @BaseHTTPCrawler.proxyUpdate(300)
    def secondaryCrawler(self, urlAndName):
        time.sleep(5)
        self.URL = urlAndName[0]  # 新的url
        self.Name = urlAndName[1]  # 相关的名字
        response = requests.get(self.URL, self.headers)
        self.responseData = response.json()[
            'data']  # 最后需要处理的数据形式如：{'id': '212734', 'school_id': '60', 'type': '68002', 'title': '天津大学2024年本科招生章程', 'content': ‘……’}
        # print(self.responseData)
        self.endDataTreating()
        pass
        # 爬取新url里面招生章程的内容

    def endDataTreating(self):
        # print(self.responseData['content'])
        one = self.responseData['content']
        self.text = ''
        for i in re.findall(r'>(.*?)<', one):
            if i == '':
                continue
            self.text += i.replace('&nbsp;', '\n').replace('\u3000', ' ')
        self.processedData += [self.Name, self.text]
        # print(text)
        pass
        # 将数据进行处理后写成str格式

    def writeExcel(self, name):
        wb = load_workbook(r'./data/招生章程.xlsx')
        ws = wb['Sheet1']
        self.processedData = [name] + self.processedData
        ws.append(self.processedData)
        wb.save(r'./data/招生章程.xlsx')
        pass

    def programInitiation(self):
        with open('./data/linkage.json', 'r', encoding='utf-8') as f:
            data = json.load(f)['school']
            for i in data:
                self.initializeData()
                self.firstCrawler(i['school_id'], )
                for j in self.overallUrlName:
                    self.secondaryCrawler(j)
                self.writeExcel(i['name'])
                # print(self.processedData)
                print(i['name'], "好了")
