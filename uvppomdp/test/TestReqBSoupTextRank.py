# --------------------------------------------
# @File     : TestReqBSoupTextRank.py
# @Time     : 2018/7/10 17:25
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : TestReqBSoupTextRank.py
# --------------------------------------------
import requests
from bs4 import BeautifulSoup
from textrank4zh import TextRank4Keyword,TextRank4Sentence

if __name__=='__main__':
    # TODO: 找出有哪些网页
    urls=[
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

    for url in urls:
        res=requests.get(url)
        soup=BeautifulSoup(res.text,'html.parser')

        # 有的网页内容没有body
        t=soup.find("body").text
        tr4w=TextRank4Keyword()

        tr4w.analyze(text=t,lower=True,window=2)
        print("keyword: [",end="")
        for item in tr4w.get_keywords(20,word_min_len=1):
            print(item.word,end=" ")
        print("]")

        tr4s=TextRank4Sentence()
        tr4s.analyze(text=t,lower=True,source='all_filters')

        print("abstraction:")
        for item in tr4s.get_key_sentences(num=3):
            print(item.index, item.weight, item.sentence)

        # 从结果看来还是提取关键词的方法比较靠谱

    pass