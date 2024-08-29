import json
import time
import requests

from openpyxl.reader.excel import load_workbook
from .baseHTTPCrawler import BaseHTTPCrawler


class EnrollmentPlanCrawler(BaseHTTPCrawler):
    def __init__(self):
        super().__init__()
        self.ws = None
        self.wb = None
        self.school_name = None
        self.URL = None
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

    def batchInformationCrawler(self, local_province_id, local_type_id, region):
        if local_type_id % 2 != 0:
            print(f'开始爬取{region}……', end='')
        for i in range(1, 50):
            self.URL = self.iterSignSafe(
                f'https://api.zjzw.cn/web/api/?local_province_id={local_province_id}&local_type_id={local_type_id}&page={i}&school_id={self.school_id}&size=10&special_group=&uri=apidata/api/gkv3/plan/school&year=2024'
            )
            response = requests.post(url=self.URL, headers=self.headers)

            # print(response)
            print(response.json())
            interims = response.json()['data']['item']
            if interims == []:
                break
            else:
                for interim in interims:
                    self.Data = [self.school_name,  # 学校名字
                                 interim['length'],  # 学制
                                 interim['local_batch_name'],  # 批次
                                 interim['num'] + '人',  # 招生计划
                                 interim['sg_info'] + interim['sp_info'],  # 选科要求
                                 "专业组" + interim['sg_name'],  # 专业组
                                 interim['spname'],  # 专业名称
                                 interim['tuition'] + '/年',  # 学费
                                 interim['local_type_name'],  # 类别
                                 region,  # 地区
                                 ]
                    self.ws.append(self.Data)
            time.sleep(5)

    @BaseHTTPCrawler.proxyUpdate(300)
    def structureUrl(self, school_id, school_name):  #
        # school_id = data['school_id']
        # school_name = data['name']
        self.school_id = school_id
        self.school_name = school_name
        print('------------------', school_name, '开始爬取', '------------------')
        self.wb = load_workbook(r'./data/招生计划.xlsx')
        self.ws = self.wb['全部']
        self.batchInformationCrawler(11, 3, '北京')
        self.batchInformationCrawler(12, 3, '天津')
        self.batchInformationCrawler(13, 2073, '河北')  # 物理类
        self.batchInformationCrawler(13, 2074, '河北')  # 历史类
        self.batchInformationCrawler(14, 1, '山西')  # 理科
        self.batchInformationCrawler(14, 2, '山西')  # 文科
        self.batchInformationCrawler(15, 1, '内蒙古')  # 理科
        self.batchInformationCrawler(15, 2, '内蒙古')  # 文科
        self.batchInformationCrawler(21, 2073, '辽宁')  # 物理类
        self.batchInformationCrawler(21, 2074, '辽宁')  # 历史类
        time.sleep(4)
        self.batchInformationCrawler(22, 2073, '吉林')  # 物理类
        self.batchInformationCrawler(22, 2074, '吉林')  # 历史类
        self.batchInformationCrawler(23, 2073, '黑龙江')  # 物理类
        self.batchInformationCrawler(23, 2074, '黑龙江')  # 历史类
        self.batchInformationCrawler(31, 3, '上海')
        self.batchInformationCrawler(32, 2073, '江苏')  # 物理类
        self.batchInformationCrawler(32, 2074, '江苏')  # 历史类
        self.batchInformationCrawler(33, 3, '浙江')
        self.batchInformationCrawler(34, 2073, '安徽')  # 物理类
        self.batchInformationCrawler(34, 2074, '安徽')  # 历史类
        time.sleep(4)
        self.batchInformationCrawler(35, 2073, '福建')  # 物理类
        self.batchInformationCrawler(35, 2074, '福建')  # 历史类
        self.batchInformationCrawler(36, 2073, '江西')  # 物理类
        self.batchInformationCrawler(36, 2074, '江西')  # 历史类
        self.batchInformationCrawler(37, 3, '山东')
        self.batchInformationCrawler(41, 1, '河南')  # 理科
        self.batchInformationCrawler(41, 2, '河南')  # 文科
        self.batchInformationCrawler(42, 2073, '湖北')  # 物理类
        self.batchInformationCrawler(42, 2074, '湖北')  # 历史类
        self.batchInformationCrawler(43, 2073, '湖南')  # 物理类
        time.sleep(4)
        self.batchInformationCrawler(43, 2074, '湖南')  # 历史类
        self.batchInformationCrawler(45, 2073, '广西')  # 物理类
        self.batchInformationCrawler(45, 2074, '广西')  # 历史类
        self.batchInformationCrawler(46, 3, '海南')
        self.batchInformationCrawler(50, 2073, '重庆')  # 物理类
        self.batchInformationCrawler(50, 2074, '重庆')  # 历史类
        self.batchInformationCrawler(51, 1, '四川')  # 理科
        self.batchInformationCrawler(51, 2, '四川')  # 文科
        self.batchInformationCrawler(52, 2073, '贵州')  # 物理类
        self.batchInformationCrawler(52, 2074, '贵州')  # 历史类
        time.sleep(4)
        self.batchInformationCrawler(53, 1, '云南')  # 理科
        self.batchInformationCrawler(53, 2, '云南')  # 文科
        self.batchInformationCrawler(54, 1, '西藏')  # 理科
        self.batchInformationCrawler(54, 2, '西藏')  # 文科
        self.batchInformationCrawler(61, 1, '陕西')  # 理科
        self.batchInformationCrawler(61, 2, '陕西')  # 文科
        self.batchInformationCrawler(62, 2073, '甘肃')  # 物理类
        self.batchInformationCrawler(62, 2074, '甘肃')  # 历史类
        self.batchInformationCrawler(63, 1, '青海')  # 理科
        self.batchInformationCrawler(63, 2, '青海')  # 文科
        time.sleep(4)
        self.batchInformationCrawler(64, 1, '宁夏')  # 理科
        self.batchInformationCrawler(64, 2, '宁夏')  # 文科
        self.batchInformationCrawler(65, 1, '新疆')  # 理科
        self.batchInformationCrawler(65, 2, '新疆')  # 文科
        self.wb.save(r'./data/招生计划.xlsx')
        print()
        print('------------------', school_name, '爬取完成', '------------------')

    def programInitiation(self):
        with open('./data/linkage.json', 'r', encoding='utf-8') as f:
            data = json.load(f)['school']
            for i in data:
                self.structureUrl(i['school_id'], i['name'])
