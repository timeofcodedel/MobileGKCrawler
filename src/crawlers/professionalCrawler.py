import time
import json
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from ..exports.exporter import Exporter
from .baseCrawler import BaseCrawler


class ProfessionalUrlCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.URL = "https://www.gaokao.cn/special"
        self.urldict: dict = {
            "哲学": {"哲学类": []},
            "经济学": {
                "经济学类": [],
                "财政学类": [],
                "金融学类": [],
                "经济与贸易类": [],
            },
            "法学": {
                "法学类": [],
                "政治学类": [],
                "社会学类": [],
                "民族学类": [],
                "马克思主义理论类": [],
                "公安学类": [],
            },
            "教育学": {"教育学类": [], "体育学类": []},
            "文学": {"中国语言文学类": [], "外国语言文学类": [], "新闻传播学类": []},
            "历史学": {"历史学类": []},
            "理学": {
                "数学类": [],
                "物理学类": [],
                "化学类": [],
                "天文学类": [],
                "地理科学类": [],
                "大气科学类": [],
                "海洋科学类": [],
                "地球物理学类": [],
                "地质学类": [],
                "生物科学类": [],
                "心理学类": [],
                "统计学类": [],
            },
            "工学": {
                "力学类": [],
                "机械类": [],
                "仪器类": [],
                "材料类": [],
                "能源动力类": [],
                "电气类": [],
                "电子信息类": [],
                "自动化类": [],
                "计算机类": [],
                "土木类": [],
                "水利类": [],
                "测绘类": [],
                "化工与制药类": [],
                "地质类": [],
                "矿业类": [],
                "纺织类": [],
                "轻工类": [],
                "交通运输类": [],
                "海洋工程类": [],
                "航空航天类": [],
                "兵器类": [],
                "核工程类": [],
                "农业工程类": [],
                "交叉工程类": [],
                "林业工程类": [],
                "医学技术类": [],
                "环境科学与工程类": [],
                "生物医学工程类": [],
                "食品科学与工程类": [],
                "建筑类": [],
                "安全科学与工程类": [],
                "生物工程类": [],
                "公安技术类": [],
            },
            "农学": {
                "植物生产类": [],
                "自然保护与环境生态类": [],
                "动物生产类": [],
                "动物医学类": [],
                "林学类": [],
                "水产类": [],
                "草学类": [],
            },
            "医学": {
                "基础医学类": [],
                "临床医学类": [],
                "口腔医学类": [],
                "公共卫生与预防医学类": [],
                "中医学类": [],
                "中西医结合类": [],
                "药学类": [],
                "中药学类": [],
                "法医学类": [],
                "医学技术类": [],
                "护理学类": [],
            },
            "管理学": {
                "管理科学与工程类": [],
                "工商管理类": [],
                "农业经济管理类": [],
                "公共管理类": [],
                "图书情报与档案管理类": [],
                "物流管理与工程类": [],
                "工业工程类": [],
                "电子商务类": [],
                "旅游管理类": [],
            },
            "艺术学": {
                "艺术学理论类": [],
                "音乐与舞蹈学类": [],
                "戏剧与影视学类": [],
                "美术学类": [],
                "设计学类": [],
            },
        }

    def ExtractUrl(self)-> dict:

        totalPageNumber: int = 29
        self._getWebSource()
        self._chromeDrive.refresh()
        self.bigGroupSelector = ".major-list_gridItem__2bfyb"
        self.groupSelector = ".major-list_childItem__1nwyr"
        for index in range(2, totalPageNumber):
            pageCssSeletor: str = (
                f"li[title='{index}'].ant-pagination-item.ant-pagination-item-{index}"
            )
            time.sleep(0.5)
            for bigGroups in self._chromeDrive.find_elements(
                By.CSS_SELECTOR, self.bigGroupSelector
            ):
                bigGroupName: str = bigGroups.find_element(
                    By.CSS_SELECTOR, ".major-list_groupName__2Y4WU"
                ).text
                groups: list[WebElement] = bigGroups.find_elements(
                    By.CSS_SELECTOR, self.groupSelector
                )
                for group in groups:
                    groupName = group.find_element(
                        By.CSS_SELECTOR, ".major-list_zhuanYeName__2-NFX"
                    ).text
                    for element in group.find_elements(
                        By.CSS_SELECTOR, ".major-list_sonList__29bFH"
                    ):
                        majorName = element.find_element(
                            By.CSS_SELECTOR, ".major-list_sonTitle__24f5P"
                        ).text.split("\n")[0]
                        element.find_element(
                            By.CSS_SELECTOR, ".major-list_setSchool__3Nr1N"
                        ).click()
                        self._toggleHandlesAndGetUrl(bigGroupName, groupName, majorName)
            time.sleep(0.2)
            self._chromeDrive.find_element(By.CSS_SELECTOR, pageCssSeletor).click()
        with open(os.path.join(self.DATA_PATH,"urls.json"), "w", encoding="utf-8") as f:
            json.dump(self.urldict,f,ensure_ascii=False, indent=4)
        return self.urldict
    def _toggleHandlesAndGetUrl(
        self, bigGroupName: str, groupName: str, majorName: str
    ) -> None:
        mainHandle = self._chromeDrive.current_window_handle
        for handle in self._chromeDrive.window_handles:
            if mainHandle != handle:
                self._chromeDrive.switch_to.window(handle)
                break
        newWindowsUrl = self._chromeDrive.current_url
        self.urldict[bigGroupName][groupName].append(newWindowsUrl + ":" + majorName)
        self._chromeDrive.close()
        self._chromeDrive.switch_to.window(mainHandle)
