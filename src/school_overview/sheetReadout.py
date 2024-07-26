import pandas as pd
import xlsxwriter


def gainSchoolUrl():
    df = pd.read_excel('D:/项目学习/git/MobileGKCrawler/data/学校.xlsx', sheet_name='Sheet1')
    # print(df.columns)
    URl_data = df['获取地址']
    overallSchoolName = df['学校名字']
    print(URl_data[1], overallSchoolName[1])
    return len(URl_data), URl_data, overallSchoolName


def createSchoolSummaryForm():
    workbook = xlsxwriter.Workbook('学校简介.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', '学校名字')
    worksheet.write('B1', '学校简介')
    worksheet.write('C1', '获取地址')
    workbook.close()
    print('excel表格创建成功')


def createSchoolSpecialtyForm():
    workbook = xlsxwriter.Workbook('学校.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', '学校名字')
    worksheet.write('B1', '学校简介')
    worksheet.write('C1', '获取地址')
    workbook.close()
    print('excel表格创建成功')
