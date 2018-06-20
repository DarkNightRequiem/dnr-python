# --------------------------------------------
# @File     : TestPrivateFunction.py
# @Time     : 2018/6/20 18:08
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 
# --------------------------------------------


class Test:
    def _fun1(self):
        print("保护方法")

    def __fun2(self):
        print("私有方法")


if __name__ == '__main__':
    t=Test()
    # 保护类型的方法可以访问
    t._fun1()
    # 私有方法无法访问
    t.__fun2()