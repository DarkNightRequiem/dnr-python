# --------------------------------------------
# @File     : MpPageDurationStats.py
# @Time     : 2018/8/2 19:40
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 统计页面浏览时长
# --------------------------------------------
from util.ConfigReader import config_reader
import os
import json
import numpy as np
from matplotlib import pyplot


def stats():
    input_dir=config_reader.tb_requestactivemerger_output_dir
    file_list=os.listdir(input_dir)
    duration_dict={}

    for name in file_list:
        with open(input_dir+"/"+name,"rb")as file:
            serps=json.loads(file.read())
        file.close()

        for serp in serps:
            clicks=serp["clicks"]
            for click in clicks:
                msDuration=click["msDuration"]
                if msDuration not in duration_dict.keys():
                    duration_dict[msDuration]=1
                else:
                    duration_dict[msDuration]=duration_dict[msDuration]+1

    # extract the labels and sort them
    labels=[x for x in duration_dict]
    labels=sorted(labels)

    # extract the values
    values=[duration_dict[x] for x in labels]
    num=len(labels)

    # items=duration_dict.items()
    # li=[(elem2,elem1)for elem1,elem2 in items]
    pyplot.scatter(labels,values)
    pyplot.show()


if __name__=='__main__':
    query_dict=stats()
    print("ok")

