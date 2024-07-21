import pandas


# TODO 重构导出器
class Exporter(object):
    def __init__(self) -> None:
        pass

    @staticmethod
    def export(data: list, majorName: list[str], mode="a") -> None:
        if mode == "a":
            table = pandas.DataFrame(data)
            with pandas.ExcelWriter("./院校总表", engine="xlsxwriter") as w:
                table.to_excel(excel_writer=w, sheet_name="总表数据")
        elif mode == "p":
            with pandas.ExcelWriter("./院校总表.xlsx", engine="xlsxwriter") as w:
                for part, index in zip(data, range(0, 13)):
                    table = pandas.DataFrame(part)
                    table.to_excel(excel_writer=w, sheet_name=majorName[index])
        else:
            raise ValueError("请输入正确的模式")
