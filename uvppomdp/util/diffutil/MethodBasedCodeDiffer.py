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

    def mbdiff(self):
        """
        基于方法对简单比较结果进行进一步的加工
        """
        # 新建检查点
        checkpoint = MbCheckPoint()

        wirtebuffer=[]

        for i in range(self.filelist.__len__()):
            filename = self.filelist[i]

            # 获取文件内容
            filepath = os.path.join(self.naive_dir, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)

            # 记录当前文件信息
            checkpoint.setinfo(filename,data)

            # 更新检查点记录
            buffer=checkpoint.update()

            if buffer is not None:
                # 生成基于方法的对比记录
                entry=self.gen_entry(buffer,checkpoint.record)
                # 添加到写入缓冲区
                wirtebuffer.append(entry)

            if checkpoint.is_border and i != 0:
                # 新的学生，重置检查点
                checkpoint.reset()
                # TODO: 生成学生的对比文件
            # else:
            #     # 判断是否记录的是无变化事件
            #     if checkpoint.is_empty:
            #         print("empty")
            #     else:
            #         # TODO: 合并信息
            #         print("not empty")
            #
            #     if i != 0:
            #         # 更新检查点时间记录
            #         checkpoint.update()

    def gen_entry(self,buffer,record):
        """
        生成写入缓冲项
        """
        entry={
            "from": record[0],
            "to":record[1],
        }
        # TODO： buffer提取方法去掉文件名
        # entry.update(buffer)
        return entry

    def write(self,id,writebuffer):
        """
        生成学号为id 的学生的基于方法的对比结果
        :param id:
        :param writebuffer:
        :return:
        """
        pass



method_based_differ = MethodBasedCodeDiffer()
