import difflib
from util.logutil.CompileLogReader import ComplieLogReader
from util.logutil.SearchLogReader import SearchLogReader

if __name__=='__main__':
    # 新建编译日志读取器
    clr=ComplieLogReader()

    # 测试读取指定文件
    # contents1=clr.read("20143622-2018-03-20-16-28-42.zip")
    # contents2=clr.read("20143622-2018-05-02-22-26-17.zip")

    # 测试读取所有文件
    content_dict=clr.readall()

    print("ddd")
