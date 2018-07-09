# --------------------------------------------
# @File     : SearchSessionExtractor.py
# @Time     : 2018/7/7 21:26
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 对缩减后的日志提取只和serp有关的部分
# --------------------------------------------
import os, shutil
import json

from util.ColorfulLogger import logger
from util.ConfigReader import config_reader


class SearchSessionExtractor:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.mkdir(self.output_dir)

        if not os.path.exists(input_dir):
            logger.error(self.__class__, "No Shrunken Log Detected!")

    def extract(self):
        file_names=os.listdir(self.input_dir)
        if file_names.__len__()<=0:return

        for name in file_names:
            with open(self.input_dir+"/"+name,"rb") as file:
                session_list=json.loads(file.read())
            file.close()
            if session_list.__len__()<=0:continue

            # 首先获取一个文件中的所有serp
            serp_list=[]
            for session in session_list:
                if session["mergedActions"].__len__()<=0:
                    continue

                for action in session["mergedActions"]:
                    if action["action"]=="serp":
                        del action["id"], \
                            action["tabId"], \
                            action["action"],\
                            action["encrypted"],\
                            action["sequenceId"], \
                            action["serverTimestamp"]
                        action["requestActives"]=[]
                        serp_list.append(action)

            # 然后根据serp来筛选页面
            for session in session_list:
                if session["mergedActions"].__len__()<=0:
                    continue

                for action in session["mergedActions"]:
                    if "action" not in action.keys():
                        continue
                    elif (action["action"]=="request") and \
                            ("refer" in action.keys()):
                        # 在获得的serp中进行索引
                        index = -1
                        referUrl=action["refer"]
                        for serp_node in serp_list:
                            if serp_node["url"]==referUrl:
                                index=serp_list.index(serp_node)

                        if index!=-1:
                            del action["id"],\
                                action["tabId"],\
                                action["sequenceId"],\
                                action["serverTimestamp"]
                            if "redirectUrl" in action.keys():
                                del action["redirectUrl"]
                            serp_list[index]["requestActives"].append(action)

                    elif action["action"]=="active":
                        for serp in serp_list:
                            if action["url"] in serp["urls"]:
                                if "id" in action.keys():
                                    del action["id"]
                                if "redirectUrl" in action.keys():
                                    del action["redirectUrl"]
                                if "sequenceId" in action.keys():
                                    del action["sequenceId"],\
                                        action["serverTimestamp"]
                                serp["requestActives"].append(action)

            # 删除由于原始log数据中不明原因造成的冗余serp现象
            clean_serp_list=[]
            for serp_node in serp_list:
                if("query" not in serp_node.keys()) or \
                        (serp_node["requestActives"].__len__()==0) or \
                        (serp_node["query"] == ""):
                    continue
                else:
                    clean_serp_list.append(serp_node)

            self.write_as_json(clean_serp_list,name.replace("log","serp"))

    def write_as_json(self, json_recognizable, filename):
        """
         写入json文件
        """
        # 这里ensure_asci=False保证写入的时候识别中文
        json_content = json.dumps(json_recognizable, indent=2,ensure_ascii=False)
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        with open(
                os.path.join(self.output_dir, filename),
                "w", encoding="utf-8"
        ) as file:
            file.write(json_content)
        file.close()


if __name__ == '__main__':
    input_dir = config_reader.tb_logshrinker_output_dir
    output_dir = config_reader.tb_searchsessionextractor_output_dir

    extractor = SearchSessionExtractor(input_dir, output_dir)
    extractor.extract()
