# --------------------------------------------
# @File     : __init__.py.py
# @Time     : 2018/6/15 21:07
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 利用Antlr4的基于Token进行代码比较的POMDP
# --------------------------------------------
"""
运行顺序：
1. TokenBasedPreprocessor.py        对编译日志的预处理
2. TokenBasedMerger.py              对预处理的结果进行整合去冗余文件
3. TokenBasedFilter.py              对整合的结果进行过滤
4. TokenBasedDiffer.py              基于过滤结果进行基于Token的比较
"""