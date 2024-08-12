import json
import logging
import os
import pandas
import random
import requests
import time
from .baseHTTPCrawler import BaseHTTPCrawler
class UniversityScoresCrawler(BaseHTTPCrawler):
    def __init__(self) -> None:
        super().__init__()
        self.maxSchoolNumber=2931
        self.DEFAULTURL="https://static-data.gaokao.cn/www/2.0/schoolprovincescore/420/2024/11.json"
        self.headers = {
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.gaokao.cn/',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.dataList=[]
        self.regionDict:dict={
            '11': '北京',
            '12': '天津',
            '13': '河北',
            '14': '山西',
            '15': '内蒙古',
            '21': '辽宁',
            '22': '吉林',
            '23': '黑龙江',
            '31': '上海',
            '32': '江苏',
            '33': '浙江',
            '34': '安徽',  
            '35': '福建',  
            '36': '江西',  
            '37': '山东',
            '41': '河南',
            '42': '湖北',
            '43': '湖南',
            '44': '广东',
            '45': '广西',
            '46': '海南',
            '50': '重庆',
            '51': '四川',
            '52': '贵州',
            '53': '云南',
            '54': '西藏',
            '61': '陕西',
            '62': '甘肃',
            '63': '青海',  
            '64': '宁夏',  
            '65': '新疆',
        }
        self.disciplineCategories:dict=self.loadJson(path=r'C:\Users\15613\Desktop\爬虫\data\dicname2id.json')['data']['type']
    @BaseHTTPCrawler.proxyUpdate(300)
    def crawl(self) -> None:  
        time.sleep(3)
        #######################
        #ai续写
        log_file = 'logs/app.log'
        # 创建日志目录如果不存在
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 初始化日志记录器
        logger = self.setupLogger(log_file)
        #######################
        idList:list=self.loadJson(path=r'C:\Users\15613\Desktop\爬虫\data\linkage.json')['school']
        for i in range(2500,self.maxSchoolNumber):
            messageDict:dict=self.getSpecialId(idList,i)
            iterUrl=self.iterID(self.DEFAULTURL,messageDict['school_id'])
            print(f"正在爬取{messageDict['name']}学校的院校分数线")
            for regionID in self.regionDict.keys():
                print(f"正在爬取{self.regionDict[regionID]}地区")
                time.sleep(random.randint(1,3))
                iterUrl=self.iterProvince(iterUrl,regionID)
                # print(iterUrl)
                try:
                    response=requests.get(iterUrl,headers=self.headers)
                    if response.status_code!=200:
                        response.close()
                        raise requests.HTTPError
                except requests.HTTPError:
                    response=self.inspectYear(iterUrl)
                    if response==None:
                        print(f"这个{self.regionDict[regionID]}地区没有院校分数线")
                        continue
                except requests.ConnectionError:
                    logger.info(f"这个{self.regionDict[regionID]}地区没有院校分数线")
                    continue
                resultDict:dict=response.json() 
                response.close()
                self.storageData(resultDict,messageDict['name'],self.regionDict[regionID])
                
        self.exportFile()
    def exportFile(self)->None:
        pd=pandas.DataFrame(self.dataList,columns=['学校','地区','学科分类','年份','录取批次','招生类型','最低分','最低位次','省控线','专业组','选课要求'])
        pd.to_excel(os.path.join(BaseHTTPCrawler._positioningPath(),'院校分数线.xlsx'),index=False)

    def getSpecialId(self,jsonList:list,index:int) -> dict:
        return jsonList[index] 
    def inspectYear(self,url:str)->requests.Response|None:
        year=2023
        while year>=2021:
            urlList=url.split('/')
            urlList[7]=str(year)
            joinUrl='/'.join(urlList)
            response=requests.get(joinUrl,headers=self.headers)
            if response.status_code==200:
                return response
            else:
                year-=1
                continue
        return None
            

    def iterProvince(self,url:str,provinceID: str) -> str:
        urlList = url.split('/')
        urlList[8]=(str(provinceID)+'.json')
        iterUrl='/'.join(urlList)
        return iterUrl
    def iterID(self,url:str, ID: int) -> str:
        urlList = url.split('/')
        urlList[6]=str(ID)
        iterUrl='/'.join(urlList)
        return iterUrl
    def loadJson(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    def query(self,queryDict:dict,queryKey:str)->str|None:
        for key, val in queryDict.items():
            if val == queryKey:
                return key
        return None
    def setupLogger(self, log_file='app.log'):
    # 创建一个logger
        logger = logging.getLogger('my_logger')
        logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger
    def storageData(self,data:dict,schoolName:str,regionName:str)->None:
        categories=len(data['data'])
        try:
            for key ,value in data['data'].items():
                for i in range(len(value['item'])):
                    tempList=value['item']
                    discipline=self.query(self.disciplineCategories,key)
                    self.dataList.append([
                        schoolName,
                        regionName,
                        discipline,
                        tempList[i]['year'],
                        tempList[i]['local_batch_name'],
                        tempList[i]['zslx_name'],
                        tempList[i]['min'],
                        tempList[i]['min_section'],
                        tempList[i]['proscore'],
                        tempList[i]['sg_name'],
                        tempList[i]['sg_info']
                    ])
        except KeyError:
            print(f"这个{schoolName}学校没有{regionName}地区分数线")