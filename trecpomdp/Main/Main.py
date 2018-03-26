from ProcessingUtil.TrecDomParser import TrecDomParser as tdp

if __name__ == '__main__':
    # 在session track2012中有一个subject是"merck & co"在6140行左右，&是特殊字符解析或报错，我先简单替换成空格，分析无影响
    sessionTrack12=tdp("D:\\SAL\\POMDP\\TRECData\\sessiontrack2012.xml",12)
    sessionTrack13=tdp("D:\\SAL\\POMDP\\TRECData\\sessiontrack2013.xml",13)

    # 按照topic划分
    sessionTrack12.divideAccordingTopic()
    sessionTrack13.divideAccordingTopic()

    # 先把state 打上标签，一个interaction对应一个state
    
    print("sssss")
