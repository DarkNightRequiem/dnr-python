import os


if __name__ == '__main__':
    """
    This file is wrote to extract the mapping of clue web ID to relevance.
    If "rlvMap.py" does not exist in the util package, then this file 
    should be run first.
    """
    # 获取搜索日志所所在的目录
    packDir = os.path.dirname(os.path.realpath(__file__))
    packDir = os.path.split(packDir)[0]
    path2 = os.path.join(packDir, 'sessionlog', 'relevance2012.txt')
    path3 = os.path.join(packDir, 'sessionlog', 'relevance2013.txt')
    wpath = os.path.join(packDir, 'util', 'rlvMap.py')

    f = open(path2, 'r')
    lines = f.readlines()  # 读取全部内容
    f.close()

    # 一个文件最后只有一个'\n'没事，但是如果有多个'\n',那么最后一个'\n'之前的'\n'都会被读进来
    # 记录12年的
    wrtList = list()
    wrtList.append("rlvDict={\n")
    for ind in range(lines.__len__()):
        ele = lines[ind].replace("\n", "").strip().split(" ")
        cont = "\'" + ele[0] + "*" + ele[-2] + "\' : " + ele[-1]
        wrtList.append(cont + ",\n")

    # 记录13年的
    f = open(path3, "r")
    lines = f.readlines()
    f.close()

    for ind in range(lines.__len__()):
        ele = lines[ind].replace("\n", "").strip().split(" ")
        cont = "\'" + ele[0] + "*" + ele[-2] + "\' : " + ele[-1]
        if ind == lines.__len__() - 1:
            wrtList.append(cont + "\n")
        else:
            wrtList.append(cont + ",\n")
    wrtList.append("}")

    # 写入文件
    with open(wpath, "w")as fl:
        for line in wrtList:
            fl.write(line)
