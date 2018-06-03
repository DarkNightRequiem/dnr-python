import difflib
import os
from util.BasicUtil import BasicUtil


class CmplCodeDiffer(BasicUtil):
    def __init__(self):
        BasicUtil.__init__(self)

        # 比较结果输出的目录
        self.output_path = self.cfg.get("compile.log")["diff.path"]
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        # 序列比较器
        self.matcher=difflib.SequenceMatcher()

    def diffcode(self, from_content, to_content):
        """
        对比两个文件的内容差异
        :param from_content: 旧的文件内容
        :param to_content: 新的文件内容
        :return:
        """
        # TODO: 修改代码
        # 对比结果信息头
        # diff_result_header = self.generate_header(from_content, to_content)

        # # 进行对比并生成对比信息
        # diff_info = ''.join(
        #     difflib.ndiff(
        #         from_content.splitlines(1),
        #         to_content.splitlines(1)
        #     )
        # )

        # 进行序列比较
        self.matcher.set_seqs( from_content,to_content)
        opcodes=self.matcher.get_opcodes()

        # 建立比较结果字典
        dict_perfile={}
        dict_perfile["add"]=[]
        dict_perfile["rmv"]=[]
        for opcode in opcodes:
            if opcode[0]!="equal":
                # delete类型
                if opcode[0]=="delete":
                    for i in range(opcode[1],opcode[2]+1):
                        dict_perfile["rmv"].append(from_content[i])

                # replace类型
                elif opcode[0]=="replace":
                    for i in range(opcode[1],opcode[2]+1):
                        dict_perfile["rmv"].append(from_content[i])
                    for i in range(opcode[3],opcode[4]+1):
                        dict_perfile["add"].append(to_content[i])

                # insert类型
                elif opcode[0]=="insert":
                    for i in range(opcode[3],opcode[4]+1):
                        dict_perfile["add"].append(to_content[i])

        # TODO: 完善 计划是使用jon存储数据具体查看JsonHelper类
        print("gggg")

        # # 写入文件
        # with open(
        #         os.path.join(self.output_path, "test.txt"),
        #         "w",
        #         encoding="utf-8"
        # ) as fo:
        #     fo.write(diff_result_header + diff_info)
        # fo.close()

        return opcodes

    def generate_header(self, fromfile, tofile):
        """
        生成比对结果的头部信息
        """
        # TODO: 修改代码
        header = 'from: ' + fromfile.filename + "\n" \
                 + 'to: ' + tofile.filename + "\n"
        return header

    def diffall(self, cmplfile_list):
        """
        对给列表中的相邻的文件两两进行对比，列表元素必须是CompileFile类型。
        """
        for i in range(1,cmplfile_list.__len__()):
            # 旧编译文件
            fromfiles=cmplfile_list[i-1]
            # 新编译文件
            tofiles=cmplfile_list[i]

            for key in fromfiles.contents.keys():
                if tofiles.has_path(key):
                    # 新旧编译日志中都有的文件
                    diff_info=self.diffcode(
                        fromfiles.get_content(key).splitlines(1),
                        tofiles.get_content(key).splitlines(1)
                    )
                    print("sss")
                    pass
                else:
                    # 只有旧的编译日志中有的文件
                    # TODO：实现处理
                    pass

            for key in tofiles.contents.keys():
                if not fromfiles.has_path(key):
                    # 只有新的编译日志中有的文件
                    # TODO: 实现处理
                    pass


code_differ = CmplCodeDiffer()
