# --------------------------------------------
# @File     : TokenBasedMerger.py
# @Time     : 2018/6/17 21:04
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : TokenBasedMerger
# --------------------------------------------
import os
import json
from util.ColorfulLogger import logger
from util.ConfigReader import config_reader


class TokenBasedMerger:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.mkdir(self.output_dir)

        if not os.path.exists(input_dir):
            logger.error(self.__class__, "No Preprocessed Results Detected!")

        # 学生学号列表
        self.stuid_list=[]

    def merge(self):
        file_names=os.listdir(self.input_dir)
        if file_names.__len__()<=0: return

        buffer=[]
        with open(self.input_dir+"/"+file_names[0],"r") as file:
            first_data=json.load(file)
            buffer.append({
                "filename": file_names[0],
                "timestamp": first_data["timestamp"],
                "stuid": first_data["stuid"],
                "tokens": first_data["tokens"]
            })
        file.close()

        for i in range(1,file_names.__len__()):
            with open(self.input_dir+"/"+file_names[i],"r") as current_file:
                # 缓冲区最新文件
                pre_data=buffer[buffer.__len__()-1]
                pre_id=pre_data["stuid"]
                pre_tokens_set=set(pre_data["tokens"])

                # 当前文件
                current_data=json.load(current_file)
                current_id=current_data["stuid"]
                current_timestamp=current_data["timestamp"]
                current_tokens_set = set(current_data["tokens"])

                if current_id != pre_id:
                    # 写入文件
                    for data in buffer:
                        self.write_as_json(data,data["filename"])

                    # 重新缓存
                    buffer=[]
                    buffer.append({
                        "filename": file_names[i],
                        "timestamp": current_timestamp,
                        "stuid":current_id,
                        "tokens": current_data["tokens"]
                    })
                else:
                    intersection=current_tokens_set & pre_tokens_set
                    if not ((intersection.__len__()==current_tokens_set.__len__()) and \
                        (intersection.__len__()==pre_tokens_set.__len__())):
                        # 不相同，加入缓冲区
                        buffer.append(
                            {
                                "filename":file_names[i],
                                "timestamp": current_timestamp,
                                "stuid": current_id,
                                "tokens": current_data["tokens"]
                            }
                        )

            current_file.close()

    def write_as_json(self,json_recognizable,filename):
        """
         写入json文件
        """
        json_content = json.dumps(json_recognizable, indent=4)
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        with open(
                os.path.join(self.output_dir, filename),
                "w",encoding="utf-8"
        ) as file:
            file.write(json_content)
        file.close()


if __name__ == '__main__':
    # 获取配置信息
    input_dir = config_reader.tb_tokenbasedpreprocessor_output_dir
    output_dir = config_reader.tb_tokenbasedmerger_output_dir

    # 进行合并
    merger = TokenBasedMerger(input_dir, output_dir)
    merger.merge()

    print("Successfully Merged")
