import os

#
# def getDict(sessions):
#     dDict={}
#     for session in sessions:
#
#     return None

if __name__ == '__main__':
    """
    This file is wrote to extract the mapping of query to explore dimension vale (manually annotated). 
    "If explMap.py" does not exist in sessionpomdp.util. Please run this file before you run "MainSessionSearch.py" 
    """
    # 获取搜索日志所所在的目录
    packDir = os.path.dirname(os.path.realpath(__file__))
    packDir = os.path.split(packDir)[0]
    path2 = os.path.join(packDir, 'sessionlog', 'queryexploration_trec2012.txt')
    path3 = os.path.join(packDir, 'sessionlog', 'queryexploration-trec2013.txt')
    wpath = os.path.join(packDir, 'util', 'explMap.py')

    anList2 = []
    anList3 = []

    anList2.append("explDict12 = {\n")
    with open(path2)as f2:
        lines = f2.readlines()

        # 表示下一行是否exploration的flag
        f = False
        sessionId = 0
        count=0
        for i in range(lines.__len__()):
            line = lines[i].strip().replace("\n", "")
            if line == "#":
                f = True
            elif "Session No." in line:
                d = line.find(".")
                sessionId = line[d + 1:line.__len__()]
                anList2.append(" \'"+sessionId+"\': {\n")
                count=0
                continue
            elif line == "":
                if i != lines.__len__() - 1:
                    anList2.append(" },\n")
                else:
                    anList2.append(" }\n")
                continue
            else:
                if "\'" in line:
                    line=line.replace("\'","\\\'")
                if "\\u00a3" in line:
                    line=line.replace("\\u00a3","\\\\u00a3")
                count+=1
                if f:
                    str = "  \'" +count.__str__()+'*'+ line + "\': " + "\'R\'"
                    if (i!=lines.__len__()-1)and lines[i+1]!="":
                        str+=",\n"
                    else:
                        str+="\n"
                    f = False
                else:
                    str = "  \'" +count.__str__()+'*'+ line + "\': " + "\'T\'"
                    if (i!=lines.__len__()-1)and lines[i+1]!="":
                        str+=",\n"
                    else:
                        str+="\n"
                anList2.append(str)
    anList2.append("}\n\n")

    anList3.append("explDict13 = {\n")
    with open(path3)as f3:
        lines = f3.readlines()

        # 表示下一行是否exploration的flag
        f = False
        sessionId = 0
        count = 0
        for i in range(lines.__len__()):
            line = lines[i].strip().replace("\n", "")
            if line == "#":
                f = True
            elif "Session No." in line:
                d = line.find(".")
                sessionId = line[d + 1:line.__len__()]
                anList3.append(" \'"+sessionId+"\': {\n")
                count=0
                continue
            elif line == "":
                if i != lines.__len__() - 1:
                    anList3.append(" },\n")
                else:
                    anList3.append(" }\n")
                continue
            else:
                if "\'" in line:
                    line=line.replace("\'","\\\'")
                if "\\u00a3" in line:
                    line=line.replace("\\u00a3","\\\\u00a3")
                count+=1
                if f:
                    str = "  \'" +count.__str__()+'*'+ line + "\': " + "\'R\'"
                    if (i!=lines.__len__()-1)and lines[i+1]!="":
                        str+=",\n"
                    else:
                        str+="\n"
                    f = False
                else:
                    str = "  \'" +count.__str__()+'*'+ line + "\': " + "\'T\'"
                    if (i!=lines.__len__()-1)and lines[i+1]!="":
                        str+=",\n"
                    else:
                        str+="\n"
                anList3.append(str)
    anList3.append("}\n")

    with open(wpath, "w") as s:
        for line in anList2:
            s.write(line)
        for line in anList3:
            s.write(line)

    print("OK")
