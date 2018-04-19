import pprint as pp
import numpy as np
from pomdp.sessionsearch import IDX_S_NRR,IDX_S_NRT,IDX_S_RR,IDX_S_RT

"""
iteration： 数据进行一次前向-后向的训练（也就是更新一次参数）
batchsize：每次迭代（iteration）训练图片的数量
epoch：1个epoch就是将所有的训练图像全部通过网络训练一次
例如：假如有1280000张图片，batchsize=256，则1个epoch需要1280000/256=5000次iteration
假如它的max-iteration=450000，则共有450000/5000=90个epoch
"""


class SessionSearchModel:
    def __init__(self,argDict):
        # state number, in this case,4
        self.stateNum=argDict["stateNum"]
        # initialize the belief space
        self.space=self.getInitBeliefSpace()


    def getInitBeliefSpace(self):
        bp=np.zeros(self.stateNum,dtype=np.float)
        # 论文中一开始都认定是在NRR的状态.所以一开始是1，可以根据情况修改
        bp[IDX_S_NRR]=1
        bp[IDX_S_NRT]=0
        bp[IDX_S_RR]=0
        bp[IDX_S_RT]=0
        print("Initial Belief Space:",bp)
        return bp

