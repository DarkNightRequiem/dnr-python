import os
import platform
import yaml
import chardet
import zipfile
from util.logutil.BasicUtil import BasicUtil
from util.meta.ComplieFile import CompileFile


class ComplieLogReader(BasicUtil):
    def __init__(self):
        BasicUtil.__init__(self)

        # 编译日志存放目录
        self.dir = self.cfg.get("compile.log")["dir"]

        # 编译日志文件名列表
        self.files_names = os.listdir(self.dir)

    def read(self, name):
        """
        用于读取单个zip文件的内容，文件需要位于dir中
        :param name: 文件名
        :return: 单个压缩文件中的所有内容列表
        """
        contents=[]
        try:
            zip = zipfile.ZipFile(self.dir + "/" + name, "r")

            # 内容为空
            if 0 == zip.filelist.__len__():
                return None

            # 项目名称
            folder = zip.filelist[0].filename.split("/")[0]

            for entry in zip.filelist:
                if entry.filename.find(folder + "/Properties") >= 0:
                    # 忽略Properties文件夹
                    continue
                else:
                    # 读取文件内容
                    file_bytes = zip.read(entry.filename)
                    encode = (chardet.detect(file_bytes))["encoding"]

                    contents.append(
                        CompileFile(
                            entry.filename,
                            zip.read(entry.filename).decode(encode)
                        )
                    )

        except zipfile.BadZipFile:
            # 文件损坏
            print("\033[32;0mBroken File:",name)
            return None
        except TypeError:
            # 无法解析文件编码
            print("\033[32;0mUnKnown File Encoding: ",name)
            return None

        return contents

    def readall(self):
        """
        读取配置文件中指定目录下的所有zip文件内容
        :return: 字典形式的所有文件内容
        """
        cmpllog_dict={}

        for filename in self.files_names:
            contents=self.read(filename)

            if contents is not None:
                cmpllog_dict[filename]=contents

        return cmpllog_dict

