from functools import wraps
def singleton(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pass
        return wrapper.instance
class Core(object):
    def __init__(self):
        pass