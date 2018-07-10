# --------------------------------------------
# @File     : RequestActiveMerger.py
# @Time     : 2018/7/9 21:02
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 对request和active进行融合计算时间
# --------------------------------------------
import os, shutil
import json
import time
import chardet
import operator

from util.ColorfulLogger import logger
from util.ConfigReader import config_reader


class RequestActiveMerger:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.mkdir(self.output_dir)

        if not os.path.exists(input_dir):
            logger.error(self.__class__, "No Extracted Serp Detected!")

    def merge(self):
        file_names = os.listdir(self.input_dir)
        if file_names.__len__() <= 0: return

        for name in file_names:
            with open(input_dir + "/" + name, "rb")as file:
                serp_list=json.loads(file.read())
            file.close()

            for serp in serp_list:
                clicks={}
                for req_act in serp["requestActives"]:
                    if req_act["url"] not in clicks.keys():
                        # 未计算过
                        if req_act["url"] in serp["urls"]:
                            clicks[req_act["url"]]={
                                "url": req_act["url"],
                                "rank": serp["urls"].index(req_act["url"]),
                                "startTimestamp":req_act["timestamp"],
                                "endTimestamp": req_act["timestamp"],
                                "msDuration":0
                            }
                    else:
                        # 更新
                        old_endstamp=clicks[req_act["url"]]["endTimestamp"]
                        new_endstamp=req_act["timestamp"]
                        if new_endstamp >old_endstamp:
                            clicks[req_act["url"]]["endTimestamp"]=new_endstamp
                            clicks[req_act["url"]]["msDuration"]=\
                                clicks[req_act["url"]]["msDuration"]+new_endstamp-old_endstamp

                serp["clicks"]=list(clicks.values())
                del serp["requestActives"]

            # 去重（属于极少数的情况）
            clean_serp_list=[]
            serp_dict={}
            for serp_node in serp_list:
                url=serp_node["url"]
                query=serp_node["query"]
                if (url,query)not in serp_dict.keys():
                    serp_dict[(url,query)]=serp_node["timestamp"]
                    clean_serp_list.append(serp_node)

            self.write_as_json(clean_serp_list,name)

    def write_as_json(self,json_recognizable,filename):
        """
         写入json文件
        """
        json_content = json.dumps(json_recognizable, indent=2,ensure_ascii=False)
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        with open(
                os.path.join(self.output_dir, filename),
                "w",encoding="utf-8"
        ) as file:
            file.write(json_content)
        file.close()


if __name__ == '__main__':
    input_dir = config_reader.tb_searchsessionextractor_output_dir
    output_dir = config_reader.tb_requestactivemerger_output_dir

    merger = RequestActiveMerger(input_dir, output_dir)
    merger.merge()
