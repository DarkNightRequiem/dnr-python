import logging


class ColorfulLogger:
    def __init__(self):
        pass

    def error(self,module_name,message):
        logging.log(logging.ERROR, module_name + ": " + message)

    def warning(self,module_name,message):
        logging.log(logging.WARNING, module_name+": "+message)

    def critical(self,module_name,message):
        logging.log(logging.CRITICAL, module_name + ": " + message)


# 利用模块的导入机制实现单例模式
logger=ColorfulLogger()