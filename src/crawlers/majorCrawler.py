import time

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from ..exports.exporter import Exporter
from .baseCrawler import BaseCrawler


class MajorCrawler(BaseCrawler):
    """
    专门爬取高校信息的爬虫类，继承自BaseCrawler。
    """

    def __init__(self):
        super().__init__()
        self.URL = "https://www.gaokao.cn/school/search"
        self.username = "17875328528"
        self.password = "Dym1561317465"
        self._PAGE_NUMBER = 148
        self._MAJOR_NAME: list = [
            "综合类",
            "理工类",
            "农林类",
            "医药类",
            "师范类",
            "语言类",
            "财经类",
            "政法类",
            "体育类",
            "艺术类",
            "民族类",
            "军事类",
            "其他类",
        ]

    def crawl(self) -> None:
        """
               主要的爬取函数，负责分页爬取高校信息并进行基础处理。
        """
        self._getWebSource()
        self._chromeDrive.refresh()
        schoolDataList: list[dict] = []
        for pageNum in range(2, self._PAGE_NUMBER + 1):
            pageCssSeletor: str = (
                f"li[title='{pageNum}'].ant-pagination-item.ant-pagination-item-{pageNum}"
            )
            dataCssSelector: str = "school-search_schoolItem__3q7R2"
            webElements: list[WebElement] = self._chromeDrive.find_elements(
                By.CLASS_NAME, dataCssSelector
            )
            for element in webElements:
                # print(element.text+'\n')
                schoolDataList.append(self.dataParse(element.text))
            self._chromeDrive.find_element(By.CSS_SELECTOR, pageCssSeletor).click()
            time.sleep(0.4)
            print(pageNum)
            if pageNum == self._PAGE_NUMBER - 1:
                break

    # Exporter.export(data=self._classifySchoolTypes(schoolDataList, mode="p"), majorName=self._MAJOR_NAME, mode="p")

    def _classifySchoolTypes(
            self, schoolList: list[dict], mode="a"
    ) -> list[dict] | list:
        """
               对爬取的高校信息进行分类。

               :param schoolList: 高校信息列表
               :param mode: 分类模式，"a"表示合并同类项，"p"表示分组
               :return: 分类后的高校信息列表或列表的列表
        """
        _comprehensiveTypeList: list = []
        _scienceAEngineerList: list = []
        _agricultureAForestryList: list = []
        _medicineList: list = []
        _teacherTrainList: list = []
        _languagTypeList: list = []
        _financeAEconomicsTypeList: list = []
        _politicsALawTypeList: list = []
        _sportsTypeList: list = []
        _artTypeList: list = []
        _ethnicityTypeList: list = []
        _militaryTypeList: list = []
        _otherTypeList: list = []
        for school in schoolList:
            match school["type"]:
                case "综合类":
                    _comprehensiveTypeList.append(school)
                case "理工类":
                    _scienceAEngineerList.append(school)
                case "农林类":
                    _agricultureAForestryList.append(school)
                case "医药类":
                    _medicineList.append(school)
                case "师范类":
                    _teacherTrainList.append(school)
                case "语言类":
                    _languagTypeList.append(school)
                case "财经类":
                    _financeAEconomicsTypeList.append(school)
                case "政法类":
                    _politicsALawTypeList.append(school)
                case "体育类":
                    _sportsTypeList.append(school)
                case "艺术类":
                    _artTypeList.append(school)
                case "民族类":
                    _ethnicityTypeList.append(school)
                case "军事类":
                    _militaryTypeList.append(school)
                case "其他类":
                    _otherTypeList.append(school)
        if mode == "a":
            resultList: list = (
                    _comprehensiveTypeList
                    + _scienceAEngineerList
                    + _agricultureAForestryList
                    + _medicineList
                    + _teacherTrainList
                    + _languagTypeList
                    + _financeAEconomicsTypeList
                    + _politicsALawTypeList
                    + _sportsTypeList
                    + _artTypeList
                    + _ethnicityTypeList
                    + _militaryTypeList
                    + _otherTypeList
            )
            return resultList
        elif mode == "p":
            return [
                _comprehensiveTypeList,
                _scienceAEngineerList,
                _agricultureAForestryList,
                _medicineList,
                _teacherTrainList,
                _languagTypeList,
                _financeAEconomicsTypeList,
                _politicsALawTypeList,
                _sportsTypeList,
                _artTypeList,
                _ethnicityTypeList,
                _militaryTypeList,
                _otherTypeList,
            ]
        else:
            raise ValueError("请输入正确的模式")

    def dataParse(self, dataStr: str) -> dict:
        """
               对爬取的高校信息字符串进行解析，转换为字典格式。

               :param dataStr: 高校信息的字符串表示
               :return: 解析后的高校信息字典
        """
        dataList = dataStr.split("\n")
        # print(dataList)
        schoolDict: dict = {
            "name": dataList[0],
            "local": dataList[1],
            "level": dataList[2],
            "type": dataList[3],
            "feature": dataList[4],
        }
        temptags = ["985", "211", "双一流", "强基计划"]
        tempList = []
        for tag in temptags:
            if tag in dataList:
                tempList.append(tag)
        if len(tempList) == 0:
            schoolDict["universityStauts"] = None
        else:
            schoolDict["universityStauts"] = ",".join(tempList)

        return schoolDict


if __name__ == "__main__":
    pass
