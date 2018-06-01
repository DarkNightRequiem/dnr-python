import os
import platform
import yaml


if __name__== '__main__':
    """
    测试python读取yaml配置文件
    """

    # 项目根目录
    root=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    # 配置文件路径
    cfgFile=""
    if platform.system()== "Windows":
        cfgFile=root+"\\config.yaml"
    elif platform.system()== "Linux":
        cfgFile=root+"/config.yaml"

    # 读取配置文件,打开方式必须是rb(只读二进制)，否则遇到yaml中中文注释会报错
    cfg=yaml.load(open(cfgFile,"rb"))

    # 编译日志目录
    cmpl_dir=cfg.get("compile.log")["dir"]
    cmpl_files=os.listdir(cmpl_dir)

    # 浏览日志目录
    brws_dir=cfg.get("search.log")["dir"]
    brws_files=os.listdir(brws_dir)

    print(cmpl_dir)
    print(brws_dir)