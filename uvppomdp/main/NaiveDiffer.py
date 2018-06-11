# --------------------------------------------
# @File     : NaiveDiffer.py
# @Time     : 2018/6/11 21:14
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : * 此文件用户生成 基本的编译日志代码的比较结果。
#             * 比较结果以json文件的格式存放
#             * 比较结果中记录的了相邻两个编译日志（一个编译日志是一个压缩包）
#               中所有文件的添加的行和删除的行。
#             * 空白行和程序块的边界行（单行花括号）忽略不计
# --------------------------------------------

from util.logreader.CompileLogReader import cmpl_reader
from util.diffutil.NaiveCmplCodeDiffer import navie_differ

if __name__=='__main__':
    # 读取所有编译日志
    cmplfile_list=cmpl_reader.readall()

    # 进行比较
    navie_differ.diffall(cmplfile_list)

    print("[NaiveDiffer] Accomplished Differing")
