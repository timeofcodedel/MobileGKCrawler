import re
import threading
from time import sleep

import requests
from bs4 import BeautifulSoup
from openpyxl.reader.excel import load_workbook

from ..seleniumCrawler.SchoolOverviewcrawler import SheetReadout


def replenish(name, numericalorder):
    try:
        url = f'https://baike.baidu.com/item/{name}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        school = soup.find_all(attrs={'para_mjfg6 summary_jOXa4 MARK_MODULE'})
        schoolOverall = ''
        # print(re.findall(r'>(.*?)<', str(school)))
        for i in re.findall(r'>(.*?)<', str(school)):
            if i == '' or ('[' in i and ']' in i):
                pass
            else:
                schoolOverall += i
        # print(schoolOverall)
        wife(numericalorder, schoolOverall)
        print(numericalorder, '\t\t', name)
    except:
        print('少了' + name)


def wife(numericalorder, overall):
    workbook = load_workbook('D:/项目学习/git/MobileGKCrawler/data/学校简介.xlsx')
    sheet = workbook.active
    sheet[f'D{numericalorder}'] = overall  # type: ignore
    workbook.save('D:/项目学习/git/MobileGKCrawler/data/学校简介.xlsx')
    workbook.close()


if __name__ == '__main__':
    overallSchool = SheetReadout().gainSchoolUrl()
    number = 2
    for i in overallSchool[2]:
        replenish(i, number)
        number += 1
