# --------------------------------------------
# @File     : ZipFileStream.py
# @Time     : 2018/6/13 19:51
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 仿照antlr4中的FileStream类编写的压缩文件流类
# --------------------------------------------

#
# Copyright (c) 2012-2017 The ANTLR Project. All rights reserved.
# Use of this file is governed by the BSD 3-clause license that
# can be found in the LICENSE.txt file in the project root.
#

#
#  This is an InputStream that is loaded from a file all at once
#  when you construct the object.
#

import codecs
from antlr4.InputStream import InputStream


class ZipFileStream(InputStream):

    def __init__(self,file_bytes:bytes, encoding:str='utf-8', errors:str='ignore'):
        super().__init__(self.decode(file_bytes,encoding,errors))

    def decode(self, file_bytes:bytes, encoding:str, errors:str='ignore'):
        return codecs.decode(file_bytes, encoding, errors)



