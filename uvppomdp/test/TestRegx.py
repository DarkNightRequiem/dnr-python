# --------------------------------------------
# @File     : TestRegx.py
# @Time     :
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : Generated Before I set template
# --------------------------------------------
import re


def isjunk(line):
    junk_patterns = [
        re.compile(r"\s*[\s{}]\s*"),
        re.compile(r""),
        re.compile(r"(\s*)(/+)([^/]*)")
    ]

    for jp in junk_patterns:
        if re.sub(jp, "", line) == "":
            return True
    return False


def test1():
    lines=[
        "    ",
        "   { ",
        "{   ",
        "}",
        "{",
        "     }",
        "  }  ",
        " // \u53c2\u6570",
        "   // / \u5bfc\u822a\u5230\u7279\u5b9a\u9875\u5931\u8d25\u65f6\u8c03\u7528",
        " // ",
        "   <Application>",
        "private void OnSuspending(object sender, SuspendingEventArgs e)",
        "var deferral = e.SuspendingOperation.GetDeferral();"
        "using Windows.ApplicationModel.Activation;"
    ]

    # 测试正则表达式
    for line in lines:
        print(isjunk(line))

    # 测试利用正则表达式从行中抽取出方法
    lines2=[
        "using Windows.UI.Xaml.Navigation;",
        "            this.InitializeComponent();",
        "rootFrame.Navigate(typeof(MainPage), e.Arguments);",
        "command.Connection = db;"

    ]

    pattern=re.compile(r"[a-zA-Z0-9].[a-zA-Z0-9]*")
    for line in lines2:
        it=re.finditer(pattern,line)
        it2=re.findall(pattern,line)
        print("kk")


def test2():
    """
    测试去除泛型
    """
    protos=[
        "IAsyncOperation<TResult>",
        "IAsyncOperation<TResult<ASDVFFFFF>>",
        "IAsyncddddd<TResult<DDDDD<FFFFF<lll>>>"
    ]
    pattern=re.compile(r"<.*>")

    for proto in protos:
        proto=re.sub(pattern,"",proto)
        print(proto)


if __name__=='__main__':
    """
    测试代码比对中使用的正则表达式
    """
    test2()

