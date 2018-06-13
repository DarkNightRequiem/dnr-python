# --------------------------------------------
# @File     : MethodBasedCodeDiffer.py
# @Time     : 2018/6/9 21:14
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 此方法好像有点写废了，目前转用TokenBasedDiffer
# --------------------------------------------
import os
import json
from util.BasicUtil import BasicUtil
from util.meta.MbCheckPoint import MbCheckPoint


class MethodBasedCodeDiffer(BasicUtil):
    def __init__(self):
        BasicUtil.__init__(self)

        # 简单对比结果的存放目录
        self.naive_dir = self.cfg.get("compile.log").get("diff.dir")["naive"]

        # 简单对比结果文件列表
        self.filelist = os.listdir(self.naive_dir)

        # 基于方法的对比结果字典
        self.mbdiff_dict = {}

        # 对比结果输出目录
        self.output_path = self.cfg.get("compile.log")["diff.dir"]["method"]

        # 对比结果写入缓冲区，在每个新的学生记录开始时清空
        self.wirtebuffer=[]

    def mbdiff(self):
        """
        基于方法对简单比较结果进行进一步的加工
        """
        # 新建检查点
        checkpoint = MbCheckPoint()

        for i in range(self.filelist.__len__()):
            filename = self.filelist[i]

            # 获取文件内容
            filepath = os.path.join(self.naive_dir, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)

            # 记录当前文件信息
            checkpoint.setinfo(filename,data)
            # 更新检查点时间记录
            need_pop=checkpoint.update()

            if checkpoint.is_border and i != 0:
                # 释放写入缓冲区
                data=self.release_writebuffer()
                # 写入上个学生的对比结果
                self.write_to_file(checkpoint.pre_id, data)
                # 重置检查点
                checkpoint.reset()

            elif need_pop:
                # 弹出检查点记录并生成对比记录
                entry=self.gen_entry(
                    checkpoint.pop_data(),
                    checkpoint.record
                )
                # 添加到写入缓冲区
                self.wirtebuffer.append(entry)

    def gen_entry(self, period_data, record):
        """
        生成写入缓冲项
        """
        entry={
            "from": record[0],
            "to":record[1],
            "addmth":[],
            "rmvmth":[]
        }

        for data in period_data:
            for key in data.keys():
                if (key in ["from","to"]) or (data[key].__len__==0):
                    continue
                else:
                    for subkey in data[key].keys():
                        if data[key][subkey].__len__ >0:
                            if subkey=="add":
                                # TODO: 从各行中抽取方法
                                entry["addmth"].append(
                                    self.extract_methods(
                                        data[key][subkey]
                                    )
                                )
                            elif subkey=="rmv":
                                entry["addmth"].append(
                                    self.extract_methods(
                                        data[key][subkey]
                                    )
                                )

        return entry

    def extract_methods(self,lines):
        # TODO: 实现
        return ["d","h","g"]

    def write_to_file(self,stuid,data):
        """
        生成学号为id 的学生的基于方法的对比结果
        """
        # TODO: 实现
        pass

    def release_writebuffer(self):
        """
        释放写入缓冲区并返回写入缓冲区中存放的数据
        :return: 写入缓冲区中的数据
        """
        buffer=self.wirtebuffer
        self.wirtebuffer=[]
        return buffer


method_based_differ = MethodBasedCodeDiffer()
