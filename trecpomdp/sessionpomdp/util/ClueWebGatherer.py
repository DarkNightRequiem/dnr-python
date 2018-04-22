import requests
import codecs
import re
from bs4 import BeautifulSoup
import urllib.request
import os
from sessionpomdp.util.TrecDomParser import TrecDomParser as tdp

if __name__ == '__main__':
    # 获取搜索日志所所在的目录
    projDir = os.path.dirname(os.path.realpath(__file__))
    projDir = os.path.split(projDir)[0]
    sessionLogPath2 = os.path.join(projDir, 'sessionlog', 'sessiontrack2012.xml')
    sessionLogPath3 = os.path.join(projDir, 'sessionlog', 'sessiontrack2013.xml')
    # wDir = os.path.join(projDir, 'cluewebdemo')

    # 预处理获取 Long Sessions
    long_session_length=4
    sessionTrack12 = tdp(sessionLogPath2, 12)
    longSessions12 = sessionTrack12.getLongSessionsSorted(long_session_length,False)
    print("Long Sessions in Track2012 Count: ", longSessions12.__len__())
    inter12 = tdp.getInteractions(longSessions12, 2012)

    sessionTrack13 = tdp(sessionLogPath3, 13)
    longSessions13 = sessionTrack13.getLongSessionsSorted(long_session_length,False)
    print("Long Sessions in Track2013 Count: ", longSessions13.__len__())
    inter13 = tdp.getInteractions(longSessions13, 2013)

    print("Combined Long Sessions Count: ", longSessions12.__len__() + longSessions13.__len__())

    # 生成interaction列表
    interList = tdp.concat(inter12, inter13)

    count = 0
    excount = 0
    success = 0
    for inter in interList:
        print(str(inter.year) + "--" + str(inter.sessionID) + "--" + str(inter.topicID))
        if inter.results is not None:
            for result in inter.results:
                count += 1
                link=result.url
                name = result.webID + ".txt"  # webID 作为文件名
                if os.path.exists("D:\\clueweb\\" + name):
                    continue
                content = ""
                try:
                    r = requests.get(link)
                    r.encoding = r.apparent_encoding
                    text = r.text
                    soup = BeautifulSoup(text, "lxml")
                    for script in soup(["script", "style"]):
                        script.extract()  # rip it out
                    for c in soup.find_all('div'):
                         content += c.get_text(strip=True)
                         content.strip("\r\n")

                    print(content.__str__())
                    success += 1
                except Exception as e:
                    excount += 1
                    if result.snippet is not None:
                        content += result.snippet
                finally:
                    with codecs.open("D:\\clueweb\\" + name, "w", encoding='utf-8')as f:
                        f.write(content)

    print("ClueWeb content are now gathered \n",
          "[total url count]: ", count,
          "\t[exception count]: ", excount, "\n",
          "\t[success count]: ", success)



    # r = requests.get("http://news.sina.com.cn/photo/rel/csjsy07/399/")
    # r.encoding = r.apparent_encoding
    # text = r.text
    # soup = BeautifulSoup(text, "html.parser")
    # a = soup.find_all('img', {'class': 'b1'})
    # for i in a:
    #     print(i['src'])

"""

                    soup = BeautifulSoup(text,"lxml")
                    for script in soup(["script", "style"]):
                        script.extract()  # rip it out
                    # get text
                    text = soup.get_text()
                    # break into lines and remove leading and trailing space on each
                    lines = (line.strip() for line in text.splitlines())
                    # break multi-headlines into a line each
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    # drop blank lines
                    text = '\n'.join(chunk for chunk in chunks if chunk)

                    # soup = BeautifulSoup(text, "lxml")
                    # for li in soup.findAll(text=True):
                    #     content+=li+"\r\n"
"""