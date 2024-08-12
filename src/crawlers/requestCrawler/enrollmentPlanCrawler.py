from .baseHTTPCrawler import BaseHTTPCrawler


if __name__ == "__main__":
    a = BaseHTTPCrawler()
    print(a.iterSignSafe('https://api.zjzw.cn/web/api/?local_batch_id=14&local_province_id=44&local_type_id=2073&page=2&school_id=420&size=10&special_group=&uri=apidata/api/gkv3/plan/school&year=2024'))
