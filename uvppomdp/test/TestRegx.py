import re


def isjunk(line):
    junk_patterns = [
        re.compile(r"\s*[\s{}]\s*"),
        re.compile(r"")
    ]

    for jp in junk_patterns:
        if re.sub(jp, "", line) == "":
            return True
    return False


if __name__=='__main__':
    """
    测试代码比对中使用的正则表达式
    """

    lines=[
        "    ",
        "   { ",
        "{   ",
        "}",
        "{",
        "     }",
        "  }  "
    ]

    # 测试正则表达式
    for line in lines:
        print(isjunk(line))


