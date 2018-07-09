# --------------------------------------------
# @File     : TestOther.py
# @Time     : 2018/6/20 18:08
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 
# --------------------------------------------


class Test:
    def _fun1(self):
        print("保护方法")

    def __fun2(self):
        print("私有方法")


# encode = (chardet.detect(data))["encoding"] \
#     if (chardet.detect(data))["encoding"] is not None \
#     else "utf-8"

if __name__ == '__main__':
    # t=Test()
    # # 保护类型的方法可以访问
    # t._fun1()
    # # 私有方法无法访问
    # t.__fun2()

    # Unix时间戳（毫秒级）可以直接比较
    t1=1522680351095
    t2=1522680365178
    print(t1>t2)