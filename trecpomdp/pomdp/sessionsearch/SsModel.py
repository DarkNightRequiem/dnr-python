import pomdp.Model as md

"""
iteration： 数据进行一次前向-后向的训练（也就是更新一次参数）
batchsize：每次迭代（iteration）训练图片的数量
epoch：1个epoch就是将所有的训练图像全部通过网络训练一次
例如：假如有1280000张图片，batchsize=256，则1个epoch需要1280000/256=5000次iteration
假如它的max-iteration=450000，则共有450000/5000=90个epoch
"""


class SessionSearchModel(md.Model):
    def getActions(self):
        pass

    def __init__(self,argDict):
        super(SessionSearchModel,self).__init__(argDict)
