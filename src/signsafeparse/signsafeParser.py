import re
import hashlib
import hmac
import base64
from urllib.parse import unquote

def clean_url(url):
    return re.sub(r'^/|https?:///?', '', url)
@staticmethod
def getSignSafe(URL:str):
    p = "D23ABC@#56"
    # 示例:URL = "api.zjzw.cn/web/api/?is_single=2&local_province_id=44&page=2&province_id=&request_type=1&size=20&special_id=1&type=&uri=apidata/api/gk/special/school"
    URL = clean_url(URL)
    t = {"SIGN": p, "str": URL}

    # 解码URL
    n = unquote(t["str"])

    # 计算HMAC-SHA1
    hmacSha1 = hmac.new(p.encode("utf-8"), n.encode("utf-8"), hashlib.sha1).digest()

    # Base64编码
    base64Encoded = base64.b64encode(hmacSha1).decode("utf-8")

    # MD5哈希
    md5_hash = hashlib.md5(base64Encoded.encode("utf-8")).hexdigest()

    return md5_hash
if __name__ == '__main__':
    pass



