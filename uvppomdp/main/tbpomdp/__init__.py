# --------------------------------------------
# @File     : __init__.py.py
# @Time     : 2018/6/15 21:07
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 利用Antlr4的基于Token进行代码比较的POMDP
# --------------------------------------------
"""
运行顺序：
1. TokenBasedPreprocessor.py        对编译日志的预处理
2. TokenBasedFilter.py              对预处理的结果进行过滤
3. TokenBasedMerger.py              对过滤的结果进行整合去冗余文件
4. MediaPlayerExtractor.py          对整合结果抽取出是MediaPlayer任务的json文件
5. MediaPlayerZipExtractor.py       对编译日志提取出是MediaPlayer任务的提交
#######5. TokenBasedDiffer.py              基于整合结果进行基于Token的比较
...
"""