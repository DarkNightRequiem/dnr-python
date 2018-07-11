# --------------------------------------------
# @File     : TestReqBSoupTextRank.py
# @Time     : 2018/7/10 17:25
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : TestReqBSoupTextRank.py
# --------------------------------------------
import requests
import os
from bs4 import BeautifulSoup
from textrank4zh import TextRank4Keyword, TextRank4Sentence

if __name__ == '__main__':
    # TODO: 找出有哪些网页
    urls = [
        "https://docs.microsoft.com/en-us/uwp/api/Windows.UI.Xaml.Controls.StackPanel",
        "https://docs.microsoft.com/en-us/uwp/api/Windows.UI.Xaml.Controls.StackPanel",
        "https://docs.microsoft.com/en-us/windows/uwp/design/layout/grid-tutorial",
        "https://docs.microsoft.com/en-us/windows/uwp/design/layout/grid-tutorial",
        "https://channel9.msdn.com/Series/Windows-10-development-for-absolute-beginners/UWP-009-XAML-Layout-with-StackPanel",
        "https://channel9.msdn.com/Series/Windows-10-development-for-absolute-beginners/UWP-009-XAML-Layout-with-StackPanel",
        "https://social.msdn.microsoft.com/Forums/en-US/3075f6e2-97be-46f2-af4f-f60636f09fe7/uwphow-to-bind-a-list-of-items-to-textbox-inside-stackpanel?forum=wpdevelop",
        "https://social.msdn.microsoft.com/Forums/en-US/3075f6e2-97be-46f2-af4f-f60636f09fe7/uwphow-to-bind-a-list-of-items-to-textbox-inside-stackpanel?forum=wpdevelop",
        "https://stackoverflow.com/questions/36603448/uwp-textbox-wont-stretch-in-stackpanel",
        "https://stackoverflow.com/questions/36603448/uwp-textbox-wont-stretch-in-stackpanel",
        "https://msdn.microsoft.com/en-us/library/windows/apps/system.windows.controls.stackpanel(v=vs.105).aspx",
        "https://msdn.microsoft.com/en-us/library/windows/apps/system.windows.controls.stackpanel(v=vs.105).aspx",
        "https://www.c-sharpcorner.com/article/changing-stackpanel-background-using-coding4fun-colorslider-control-in-uwp-with/",
        "https://www.c-sharpcorner.com/article/changing-stackpanel-background-using-coding4fun-colorslider-control-in-uwp-with/",
        "http://marek.piasecki.staff.iiar.pwr.wroc.pl/dydaktyka/mc/L10/UWP-009-XAML_Layout_with_StackPanel.pdf",
        "http://marek.piasecki.staff.iiar.pwr.wroc.pl/dydaktyka/mc/L10/UWP-009-XAML_Layout_with_StackPanel.pdf",
        "https://www.c-sharpcorner.com/uploadfile/mahesh/stackpanel-in-wpf/",
        "https://www.c-sharpcorner.com/uploadfile/mahesh/stackpanel-in-wpf/",
        "https://www.youtube.com/watch?v=IMDWgJfXQkw",
        "https://www.youtube.com/watch?v=IMDWgJfXQkw"
    ]

    # 用于bs4的查找过滤函数
    def my_filter_func(tag):
        return not tag.name in ["style", "script"]

    path="D:/tttttttest.txt"


    for url in urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        # if soup('script') is not None:
        #     # soup.script.extract()
        #     [s.extract() for s in soup('script')]
        # if soup.style is not None:
        #     soup.style.extract()
        # if soup.footer is not None:
        #     soup.fotter.extract()

        if soup('script') is not None:
            [s.extract() for s in soup('script')]
        if soup('style') is not None:
            [s.extract() for s in soup('style')]
        if soup('footer') is not None:
            [s.extract() for s in soup('footer')]

        with open(path,"ab+") as file:
            if "youtube" in url:
                text=soup.find('title').text
            elif url.endswith(".pdf"):
                #TODO: 是在线pdf文件如果要处理的话需要先下载下来然后用pdfminer
                # 这里先简单处理成标题
                text=url.split("/",1)[0]
                pass
            else:
                text=soup.text
            file.write(str.encode(text))
        file.close()
        print("*")

        # tbody = soup.find("body")
        # ttags = soup.find_all(my_filter_func)
        # tstr = ""
        # for tag in ttags:
        #     tstr += tag.text

        # tstr=soup.text
        # tr4w = TextRank4Keyword()
        # tr4w.analyze(text=tstr, lower=True, window=3)
        # print("关键词: 【", end="")
        # for item in tr4w.get_keywords(20, word_min_len=1):
        #     print(item.word, end=" ")
        # print("】")
        #
        # # print("关键短语: 【",end="")
        # # for phrase in tr4w.get_keyphrases(keywords_num=20,min_occur_num=2):
        # #     print(phrase,end=" ")
        # # print("】")
        #
        # tr4s = TextRank4Sentence()
        # tr4s.analyze(text=tstr, lower=True, source='all_filters')
        #
        # print("摘要:")
        # for item in tr4s.get_key_sentences(num=3):
        #     print(item.index, item.weight, item.sentence)

        # 从结果看来还是提取关键词的方法比较靠谱
        # 关键短语没用
        # 加入try except语句处理异常

    pass

# if "stackoverflow" in url:
#     text=soup.find('title').text+soup.find(id='mainbar').text
# else:
#     text=soup.text