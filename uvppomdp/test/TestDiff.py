import difflib
from util.logreader.CompileLogReader import cmpl_reader
from util.diffutil.CmplCodeDiffer import code_differ

if __name__=='__main__':
    # 测试读取指定文件
    print(cmpl_reader)
    contents1=cmpl_reader.read("20143622-2018-03-20-16-28-42.zip")
    contents2=cmpl_reader.read("20143622-2018-05-02-22-26-17.zip")

    # 测试读取所有文件
    # content_dict=cmpl_reader.readall()

    # 测试单次diff
    res=code_differ.diffcode(contents1,contents2)




    print("ddd")