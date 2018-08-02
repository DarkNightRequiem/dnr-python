# --------------------------------------------
# @File     : MpQueryStats.py
# @Time     : 2018/8/2 16:01
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 
# --------------------------------------------
from util.ConfigReader import config_reader
import os
import json


def stats():
    input_dir=config_reader.tb_requestactivemerger_output_dir
    file_list=os.listdir(input_dir)
    query_dict={}

    for name in file_list:
        if name not in query_dict.keys():
            query_dict[name]=[]

        with open(input_dir+"/"+name,"rb")as file:
            serps=json.loads(file.read())
        file.close()

        for serp in serps:
            query_dict[name].append(serp["query"])

    json_content = json.dumps(query_dict, indent=2, ensure_ascii=False)
    output_path=config_reader.tb_mpquerystats_output_path
    with open(
        output_path,
        "w",encoding="utf-8"
    ) as file:
        file.write(json_content)
    file.close()

    return query_dict


if __name__=='__main__':
    query_dict=stats()
    print("ok")

