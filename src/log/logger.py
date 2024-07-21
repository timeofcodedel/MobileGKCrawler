import logging
import time


def call_logger_terminal(level: int = logging.INFO):
    def decorator(func):
        log_terminal: logging.Logger = logging.getLogger(func.__name__)
        log_terminal.setLevel(level)

        def wrapper(*args, **kwargs):
            times_formatter = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            log_terminal.log(level, f"Called {func.__name__} at {times_formatter}")
            result = func(*args, **kwargs)
            log_terminal.log(level, f"{func.__name__} returned {result}")
            return result

        return wrapper

    return decorator


# TODO logger中的列表需要调整
def call_logger_file(level: int = logging.INFO, file_path: str = ""):
    if file_path is "":
        raise ValueError("请输入正确的日志输出路径")

    def decorator(func):
        log_file: logging.Logger = logging.getLogger(func.__name__)
        log_file.setLevel(level)
        file_handler = logging.FileHandler(
            filename=file_path, mode="a", encoding="UTF-8"
        )
        file_handler.setLevel(level)

        def wrapper(*args, **kwargs):
            times_formatter = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            file_handler.setFormatter(logging.Formatter(times_formatter))
            log_file.addHandler(file_handler)
            log_file.log(level, msg=f"Called {func.__name__} at {times_formatter}")
            result = func(*args, **kwargs)
            log_file.log(level, f"{func.__name__} returned {result}")
            return result

        return wrapper

    return decorator
