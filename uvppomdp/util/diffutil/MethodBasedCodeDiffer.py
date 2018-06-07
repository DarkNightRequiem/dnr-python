import os
import json
from util.BasicUtil import BasicUtil
from util.meta.CheckPoint import CheckPoint


class MethodBasedCodeDiffer(BasicUtil):
    def __init__(self):
        BasicUtil.__init__(self)

        # 简单对比结果的存放目录
        self.naive_dir=self.cfg.get("compile.log").get("diff.dir")["naive"]

        # 简单对比结果文件列表
        self.filelist=os.listdir(self.naive_dir)

        # 基于方法的对比结果字典
        self.mbdiff_dict={}

        # 对比结果输出目录
        self.output_path=self.cfg.get("compile.log")["diff.dir"]["method"]

    def mbdiff(self):
        """
        基于方法对简单比较结果进行进一步的加工
        """
        # 新建检查点
        checkpoint=CheckPoint()

        for i in range(self.filelist.__len__()):
            filename=self.filelist[i]

            # 记录当前文件信息
            checkpoint.setinfo(filename)

            if checkpoint.isborder():
                # 学号交界处，重置检查点记录
                checkpoint.reset()
                continue
            else:
                filepath=os.path.join(self.naive_dir,filename)
                with open(filepath,'r') as file:
                    data = json.load(file)

                    # 判断是否记录的是无变化事件
                    if self.isempty(data):
                        if i==0:
                            # 目录中第一个文件为无变化事件
                            pass
                        else:
                            # 更新检查点信息
                            checkpoint.update()
                    else:
                        # TODO: 合并信息
                        print("not empty")

    def isempty(self,data):
        """
        判断文件是否记录空信息
        :return:
        """
        flag=True

        for key in data.keys():
            if key not in ['from','to']:
                if data[key].__len__() > 0:
                    flag=False

        return flag



method_based_differ=MethodBasedCodeDiffer()