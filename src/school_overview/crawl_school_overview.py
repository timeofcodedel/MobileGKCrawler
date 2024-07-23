import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from src.crawlers.baseCrawler import BaseCrawler


class SchoolDetail(BaseCrawler):

    def __init__(self):
        super().__init__()
        self.URL = 'https://www.gaokao.cn/school/3238'

    def crawlSchoolOverview(self):
        self._chromeDrive.get(self.URL)
        detail = WebDriverWait(self._chromeDrive, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#root > div > div.container > div > div > div.layout_layoutBox__2YeRR > div:nth-child(2) > div.main > div > div:nth-child(4) > div > div.clearfix > div.school-content-left_box__2JrKH > div > div > div > div > div.left_info_item.base_info_box.clearfix.bgwhite.p20.radius8 > div.base_info_item.clearfix > div.school-introduce_box__ILNMa > div.cursor.school-introduce_more__1vggP")
            )
        )
        detail.click()
        wait = WebDriverWait(self._chromeDrive, 10)
        school_overview = ''
        content: list[WebElement] = self._chromeDrive.find_elements(By.CSS_SELECTOR,'#root > div > div.container > div > div > div.layout_layoutBox__2YeRR > div:nth-child(2) > div.main > div > div:nth-child(4) > div > div.clearfix > div.school-content-left_box__2JrKH > div > div:nth-child(2) > div > p')
        for element in content:
            school_overview += element.text + '\n'
        print(school_overview)
        self._chromeDrive.close()

    def professionalOpening(self):
        pass


if __name__ == "__main__":
    bc = SchoolDetail()
    bc.crawlSchoolOverview()
