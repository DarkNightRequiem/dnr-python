# --------------------------------------------
# @File     : MethodBasedDiffer.py
# @Time     : 2018/6/11 21:14
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : * 基于方法的代码比较 * 需要使用NaiveDiffer的运行结果
# --------------------------------------------

import os
from util.ColorfulLogger import logger
from util.diffutil.MethodBasedCodeDiffer import method_based_differ

if __name__=='__main__':
    if not os.path.exists(method_based_differ.naive_dir):
        logger.warning(str(method_based_differ.__class__),"Please run NaiveDiffer.py first")
    else:
        method_based_differ.mbdiff()
        print("[MethodBasedDiffer] Accomplished Differing")

