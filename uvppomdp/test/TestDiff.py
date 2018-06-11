# --------------------------------------------
# @File     : TestDiff.py
# @Time     :
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : Generated Before I set template
# --------------------------------------------
import difflib
from util.logreader.CompileLogReader import cmpl_reader
from util.diffutil.NaiveCmplCodeDiffer import navie_differ

if __name__=='__main__':
    # 测试读取指定文件
    # contents1=cmpl_reader.read("20143622-2018-03-20-16-28-42.zip")
    # contents2=cmpl_reader.read("20143622-2018-05-02-22-26-17.zip")

    # 测试读取所有文件
    cmplfile_list=cmpl_reader.readall()

    # 测试code diff
    navie_differ.diffall(cmplfile_list)

    print("ddd")