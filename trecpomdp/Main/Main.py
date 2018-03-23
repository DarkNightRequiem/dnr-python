from ProcessingUtil.TrecDomParser import TrecDomParser

if __name__ == '__main__':
    # 在session track2012中有一个subject是"merck & co"在6140行左右，&是特殊字符解析或报错，我先简单替换成空格，分析无影响
    tdp2012=TrecDomParser("D:\\SAL\\POMDP\\TRECData\\sessiontrack2012.xml")
    tdp2013=TrecDomParser("D:\\SAL\\POMDP\\TRECData\\sessiontrack2013.xml")
    sessions12=tdp2012.getElementByTagName("session")
    sessions13=tdp2013.getElementByTagName("session")

    # 根据时间对session进行排序

    print("sssss")
