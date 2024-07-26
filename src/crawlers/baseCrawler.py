import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BaseCrawler:
    """
    爬虫基础类，用于设置和管理爬虫的基本行为和登录操作。
    
    属性:
    username: 登录所需的用户名。
    password: 登录所需的密码。
    _chromeOptions: Chrome浏览器的选项设置。
    URL: 需要爬取的网站URL。
    DATA_PATH: 存储数据的路径。
    _chromeDrive: Chrome浏览器的驱动实例。
    """

    def __init__(self) -> None:
        """
        初始化函数，设置Chrome浏览器的选项，创建浏览器驱动实例，并进行防爬设置。
        """
        self.username: str = ""
        self.password: str = ""
        self._chromeOptions = Options()
        # self._chromeOptions.add_experimental_option("detach", True)
        self.URL: str = ""
        self.DATA_PATH = self._positioningPath()
        self._chromeDrive = webdriver.Chrome(options=self._chromeOptions)
        self._chromeDrive.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """ Object.defineProperty(navigator, 'webdriver', {get:()=>undefined})"""
            },
        )  # 防反爬

    def _getWebSource(self) -> None:
        """
        打开URL并登录网站。
        
        注意:
        此方法中应包含获取网页源代码的逻辑，但此处未实现。
        """
        self._chromeDrive.get(self.URL)
        # time.sleep(15)
        self.login(self.username, self.password)

    def _positioningPath(self) -> str:
        """
        定位并返回数据文件的存储路径。
        
        返回:
        存储数据的文件路径。
        """
        filePath = os.path.abspath(__file__)
        currentDir = os.path.dirname(filePath)
        projectRoot = os.path.dirname(os.path.dirname(currentDir))
        dataFilePath = os.path.join(projectRoot, "data")
        return dataFilePath

    def login(self, username: str, password: str) -> None:
        """
        执行登录操作。
        
        参数:
        username: 登录用的用户名。
        password: 登录用的密码。
        
        异常:
        ValueError: 如果用户名或密码为空，则抛出此异常。
        
        注意:
        此方法中应包含完整的登录逻辑，包括等待元素出现、点击登录按钮、输入用户名和密码等操作。
        """
        if username == None or password == None:
            raise ValueError("用户名或密码不能为空")
        loginButton = WebDriverWait(self._chromeDrive, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".login-btn-float_loginText__9o_uo")
            )
        )
        loginButton.click()
        passwordLoginButton = WebDriverWait(self._chromeDrive, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "icon_fillLock"))
        )
        passwordLoginButton.click()
        usernameButton = WebDriverWait(self._chromeDrive, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".login-popup_inputItem__29c36 input")
            )
        )
        passwordButton = WebDriverWait(self._chromeDrive, 5).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '.login-popup_inputItem__29c36.login-popup_verificationCodeIpt__2ZArF > input[type="password"]',
                )
            )
        )
        checkBox = WebDriverWait(self._chromeDrive, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".login-popup_agreeCheckBox__2so9j")
            )
        )
        loginButton = WebDriverWait(self._chromeDrive, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".login-popup_loginBtn__3buCc")
            )
        )
        checkBox.click()
        usernameButton.send_keys(username)
        passwordButton.send_keys(password)
        time.sleep(0.3)
        loginButton.click()
        print("登录成功")

    def crawl(self) -> None:
        """
        爬取数据的抽象方法。
        
        注意:
        此方法应由子类实现具体的爬虫逻辑。
        """
        ...

    def dataParse(self, dataStr: str) -> dict:
        """
        解析数据的抽象方法。
        
        参数:
        dataStr: 需要解析的原始数据字符串。
        
        返回:
        解析后的数据字典。
        
        注意:
        此方法应由子类实现具体的解析逻辑。
        """
        ...


if __name__ == "__main__":
    bc = BaseCrawler()
    bc._getWebSource()
