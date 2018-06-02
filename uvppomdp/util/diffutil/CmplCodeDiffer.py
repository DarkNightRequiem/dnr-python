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

    def diffcode(self, cmpl_file_from, cmpl_file_to):
        """
        对比两个文件的内容差异
        :param cmpl_file_from: 旧得编译日志文件
        :param cmpl_file_to: 新的编译日志文件
        :return:
        """
        # TODO: 修改代码
        # 对比结果信息头
        diff_result_header = self.generate_header(cmpl_file_from, cmpl_file_to)

        # 进行对比并生成对比信息
        diff_info = ''.join(
            difflib.ndiff(cmpl_file_from[0].content.splitlines(1),
                          cmpl_file_to[0].content.splitlines(1))
        )

        # 写入文件
        with open(
                os.path.join(self.output_path, "test.txt"),
                "w",
                encoding="utf-8"
        ) as fo:
            # difflib.HtmlDiff().make_file(cmpl_file_from[0].content, cmpl_file_to[0].content)
            fo.write(diff_result_header + diff_info)
        fo.close()

    def generate_header(self, cmpl_file_from, cmpl_file_to):
        """
        生成比对结果的头部信息
        :param cmpl_file_from:
        :param cmpl_file_to:
        :return:
        """
        # TODO: 修改代码
        header = 'from: ' + cmpl_file_from[0].filename + "\n" \
                 + 'to: ' + cmpl_file_to[0].filename + "\n"
        return header

    def diffall(self,cmpl_file_from, cmpl_file_to):
        """
        对比两个编译文件里的所有程序文件
        :param cmpl_file_from:
        :param cmpl_file_to:
        :return:
        """
        # TODO: 实现和完善


code_differ = CmplCodeDiffer()
