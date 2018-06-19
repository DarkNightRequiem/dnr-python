# --------------------------------------------
# @File     : TokenBasedFilter.py
# @Time     : 2018/6/18 16:13
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 
# --------------------------------------------
import os
import json

import re

from util.ConfigReader import config_reader
from util.ColorfulLogger import logger


class TokenBasedFilter:

    def __init__(self, input_dir, output_dir, api_path):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.api_path = api_path
        self.identifier_set = set()

        if not os.path.exists(output_dir):
            os.mkdir(self.output_dir)

        if not os.path.exists(input_dir):
            logger.error(self.__class__, "No Preprocessed Results Detected!")

    def filter(self):
        """
        过滤函数
        """
        file_names = os.listdir(self.input_dir)
        for filename in file_names:
            with open(self.input_dir + "/" + filename, "r") as file:
                # 获取Token列表
                data = json.load(file)
                tokens = data["tokens"]

                # 过滤
                filtered_tokens=[]
                for token in tokens:
                    if token in self.identifier_set:
                        filtered_tokens.append(token)

                # 更新并写入
                data["tokens"] = filtered_tokens
                with open(self.output_dir+"/"+filename,"w",encoding="utf-8") as newfile:
                    newfile.write(json.dumps(data,indent=4))
                newfile.close()
            file.close()

    def built_identifer_set(self):
        """
        建立标识符集合
        """
        with open(self.api_path) as api_file:
            api_data = json.load(api_file)
            for data in api_data:
                if "name" in data.keys():
                    name_identifier = self._get__name_itentifiers(data["name"])
                    self.identifier_set.add(name_identifier)

                if "namespace" in data.keys():
                    namespace_identifiers = self._get_namespace_identifiers(data["namespace"])
                    for identifier in namespace_identifiers:
                        self.identifier_set.add(identifier)

                if "properties" in data.keys():
                    properties_identifiers = self._get_properties_identifiers(data["properties"])
                    for identifier in properties_identifiers:
                        self.identifier_set.add(identifier)

                if "methods" in data.keys():
                    methods_identifiers = self._get_methods_identifiers(data["methods"])
                    for identifier in methods_identifiers:
                        self.identifier_set.add(identifier)

                if "events" in data.keys():
                    events_identifiers = data["events"]
                    for identifier in events_identifiers:
                        self.identifier_set.add(identifier)

        api_file.close()

    def _get__name_itentifiers(self,name):
        # 去除泛型
        pattern=re.compile(r"<.*>")
        return re.sub(pattern,"",name)

    def _get_namespace_identifiers(self,namesapce):
        return namesapce.split(".")

    def _get_properties_identifiers(self,properties):
        if properties is None or properties.__len__()<=0:
            return None
        else:
            return properties.keys()

    def _get_methods_identifiers(self,methods):
        if methods is None or methods.__len__()<=0:
            return None
        else:
            return methods.keys()


if __name__ == '__main__':
    # 获取配置信息
    input_dir = config_reader.tb_tokenbasedpreprocessor_output_dir
    output_dir = config_reader.tb_tokenbasedfilter_ouput_dir
    api_path = config_reader.uwp_api_path

    # 新建过滤器
    tbfilter = TokenBasedFilter(input_dir, output_dir, api_path)

    # 建立标识符集合
    tbfilter.built_identifer_set()
    print("Successfully built identifier set")

    # 过滤
    tbfilter.filter()
    print("Successfully filtered")
