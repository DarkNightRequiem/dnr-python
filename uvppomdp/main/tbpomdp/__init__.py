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
5. MediaPlayerZipExtractor.py       对编译日志提取出是MediaPlayer任务的提交（可选）
6. LogShrinker.py                   将用户的搜索日志缩减至MediaPlayer任务期间
7. SearchSessionExtractor.py        对缩减后的日志提取只和serp有关的部分
8. RequestActiveMerger.py           对提取的serp部分中的request和active进行融合计算时间
9. WebContentScraper.py             对request和active融合过后的结果爬取serp网页内容
10.TrainningDataPacker.py           对第9步和第4步的结果融合成最后的训练数据
...
"""