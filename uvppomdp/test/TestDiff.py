# --------------------------------------------
# @File     : TestDiff.py
# @Time     :
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : Generated Before I set template
# --------------------------------------------
import difflib

from past.builtins import cmp

from util.logreader.CompileLogReader import cmpl_reader
from util.diffutil.NaiveCmplCodeDiffer import navie_differ

if __name__=='__main__':
    # 测试读取指定文件
    # contents1=cmpl_reader.read("20143622-2018-03-20-16-28-42.zip")
    # contents2=cmpl_reader.read("20143622-2018-05-02-22-26-17.zip")

    # # 测试读取所有文件
    # cmplfile_list=cmpl_reader.readall()
    #
    # # 测试code diff
    # navie_differ.diffall(cmplfile_list)


    #------测试
    # 这种方法将list中的元素的顺序也考虑进去了
    s1=["aa","bb","cc"]
    s2=["dd","ff","gg"]

    s11=set(s1)
    s22=set(s2)
    re= s11 & s22
    # for line in difflib.unified_diff(s1,s2):
    #     print(line)

    print(re.__len__())


    print("ddd")