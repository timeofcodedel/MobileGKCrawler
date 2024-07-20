import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BaseCrawler:
    def __init__(self) -> None:
        self._chromeOptions = Options()
        self._chromeOptions.add_experimental_option("detach", True)
        self.URL = "https://www.gaokao.cn/school/search"
        # self._chromeOptions.add_argument("--headless")
        self.DATA_PATH = self._positioningPath()
        self._chromeDrive = webdriver.Chrome(options=self._chromeOptions)
        self._chromeDrive.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """ Object.defineProperty(navigator, 'webdriver', {get:()=>undefined})"""
        })  # 防反爬

    def _getWebSource(self) -> None:
        self._chromeDrive.get("https://www.gaokao.cn/school/search")
        time.sleep(15)  # 登录时间，后面在扩展
        # TODO 尝试登录
        self.login()
        self._web_source = self._chromeDrive.page_source
        1+1+1+1+2
        3+4+5+6

    def _positioningPath(self) -> str:
        filePath = os.path.abspath(__file__)
        # print(filePath)
        currentDir = os.path.dirname(filePath)
        # print(currentDir)
        projectRoot = os.path.dirname(os.path.dirname(currentDir))
        # print(projectRoot)
        dataFilePath = os.path.join(projectRoot, "data")
        # print(dataFilePath)
        return dataFilePath

    def login(self, username: str, password: str):
        loginButton = WebDriverWait(self._chromeDrive, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-btn-float_loginText__9o_uo"))
        )
        loginButton.click()
        passwordLoginButton = WebDriverWait(self._chromeDrive, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "icon_fillLock"))
        )
        passwordLoginButton.click()

    def crawl(self) -> None: ...

    def dataParse(self, dataStr: str) -> dict: ...
