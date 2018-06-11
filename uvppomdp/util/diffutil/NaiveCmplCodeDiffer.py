# --------------------------------------------
# @File     : NaiveCmplCodeDiffer.py
# @Time     : 2018/6/9 21:14
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     :
# --------------------------------------------
import difflib
import os
import json
import re
from util.BasicUtil import BasicUtil


class NaiveCmplCodeDiffer(BasicUtil):
    def __init__(self):
        BasicUtil.__init__(self)

        # 简单比较结果输出的目录
        self.output_path = self.cfg.get("compile.log").get("diff.dir")["naive"]
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        # 序列适配器
        self.matcher = difflib.SequenceMatcher()

        # 垃圾内容正则模式
        self.junk_patterns = [
            re.compile(r"\s*[\s{}]\s*"),
            re.compile(r""),
            re.compile(r"(\s*)(/+)([^/]*)")
        ]

    def diffcode(self, from_content, to_content):
        """
        对比两个文件的内容差异
        :param from_content: 旧的文件内容
        :param to_content: 新的文件内容
        :return: 两个文件中添加和删除的字典记录
        """
        # 进行序列比较
        self.matcher.set_seqs(from_content, to_content)
        opcodes = self.matcher.get_opcodes()

        # 建立比较结果字典
        dict_perfile = {"add": [], "rmv": []}
        for opcode in opcodes:
            if opcode[0] != "equal":
                # delete类型
                if opcode[0] == "delete":
                    for i in range(opcode[1], opcode[2]):
                        dict_perfile["rmv"].append(from_content[i])

                # replace类型
                elif opcode[0] == "replace":
                    for i in range(opcode[1], opcode[2]):
                        dict_perfile["rmv"].append(from_content[i])
                    for i in range(opcode[3], opcode[4]):
                        dict_perfile["add"].append(to_content[i])

                # insert类型
                elif opcode[0] == "insert":
                    for i in range(opcode[3], opcode[4]):
                        dict_perfile["add"].append(to_content[i])

        # 清洗处理后返回比较结果
        return self.clean_diff_result(dict_perfile)

    def clean_diff_result(self, dict_perfile):
        """
        对某个编译日志中的单个文件的比较结果进行清理
        :param dict_perfile: 某个编译日志中的单个文件的比较结果
        """
        if dict_perfile.get("add").__len__() == 0 and dict_perfile.get("rmv").__len__():
            # 没有变化
            return None

        # 清除值为空的内容
        redundants = []
        for key in dict_perfile.keys():
            if dict_perfile[key].__len__() == 0:
                redundants.append(key)
        for key in redundants:
            del dict_perfile[key]

        # 清理垃圾内容
        for key in dict_perfile.keys():
            newlist = []
            for item in dict_perfile[key]:
                if not self.isjunk(item):
                    newlist.append(item)
            dict_perfile[key] = newlist

        # 排除净内容为空的比较结果
        if dict_perfile.__len__() == 0:
            return None

        return dict_perfile

    def isjunk(self, line):
        """
        用于判断行内容是否是垃圾内容
        """
        for jp in self.junk_patterns:
            if re.sub(jp, "", line) == "":
                return True
        return False

    def diffall(self, cmplfile_list):
        """
        对给列表中的相邻的文件两两进行对比，列表元素必须是CompileFile类型。
        """
        # 先单独处理第一个文件
        fromfiles = cmplfile_list[0]
        diff_dict = {}

        diff_dict["from"] = fromfiles.id + "-0"
        diff_dict["to"] = fromfiles.filename

        for key in fromfiles.contents.keys():
            dict_perfile = self.diffcode(
                "",
                fromfiles.get_content(key).splitlines()
            )

            if dict_perfile is not None:
                diff_dict[key] = dict_perfile
            else:
                diff_dict[key] = {}

        # 写入文件
        self.wirte(
            diff_dict,
            json.dumps(diff_dict, indent=4)
        )

        # 处理剩下的文件
        for i in range(0, cmplfile_list.__len__()-1):
            # 旧编译文件
            fromfiles = cmplfile_list[i]
            # 新编译文件
            tofiles = cmplfile_list[i+1]

            # 建立字典
            diff_dict = {}

            if fromfiles.id != tofiles.id:
                diff_dict["from"] = tofiles.id+"-0"
                diff_dict["to"] = tofiles.filename

                for key in tofiles.contents.keys():
                    dict_perfile = self.diffcode(
                        "",
                        tofiles.get_content(key).splitlines()
                    )

                    if dict_perfile is not None:
                        diff_dict[key] = dict_perfile
                    else:
                        diff_dict[key] = {}

            else:
                diff_dict["from"] = fromfiles.filename
                diff_dict["to"] = tofiles.filename

                for key in fromfiles.contents.keys():
                    if tofiles.has_path(key):
                        # 新旧编译日志中都有的文件
                        dict_perfile = self.diffcode(
                            fromfiles.get_content(key).splitlines(),
                            tofiles.get_content(key).splitlines()
                        )
                    else:
                        # 只有旧的编译日志中有的文件
                        dict_perfile = self.diffcode(
                            fromfiles.get_content(key).splitlines(),
                            ""
                        )

                    if dict_perfile is not None:
                        diff_dict[key] = dict_perfile
                    else:
                        diff_dict[key] = {}

                for key in tofiles.contents.keys():
                    if not fromfiles.has_path(key):
                        # 只有新的编译日志中有的文件
                        dict_perfile = self.diffcode(
                            "",
                            tofiles.get_content(key).splitlines()
                        )

                        if dict_perfile is not None:
                            diff_dict[key] = dict_perfile
                        else:
                            diff_dict[key] = {}

            # 写入文件
            self.wirte(
                diff_dict,
                # 转换为json字符串
                json.dumps(diff_dict, indent=4)
            )

    def wirte(self,diff_dict,diff_json):
        """
        将比较结果写入到json文件中
        """
        with open(
                os.path.join(
                    self.output_path,
                    diff_dict["from"].replace(".zip", "") + "=" + diff_dict["to"].replace(".zip", "") + ".json"
                ),
                "w",
                encoding="utf-8"
        ) as fo:
            fo.write(diff_json)
        fo.close()


navie_differ = NaiveCmplCodeDiffer()


# 对比结果信息头
# diff_result_header = self.generate_header(from_content, to_content)

# # 进行对比并生成对比信息
# diff_info = ''.join(
#     difflib.ndiff(
#         from_content.splitlines(1),
#         to_content.splitlines(1)
#     )
# )

# # 写入文件
# with open(
#         os.path.join(self.output_path, "test.txt"),
#         "w",
#         encoding="utf-8"
# ) as fo:
#     fo.write(diff_result_header + diff_info)
# fo.close()
