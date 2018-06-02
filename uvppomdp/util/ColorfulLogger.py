import logging


class ColorfulLogger:
    def __init__(self):
        pass

    def error(self,module_name,message):
        logging.getLogger(module_name).log(logging.ERROR,message)

    def warning(self,module_name,message):
        logging.getLogger(module_name).log(logging.WARNING, message)

    def critical(self,module_name,message):
        logging.getLogger(module_name).log(logging.CRITICAL, message)


# 利用模块的导入机制实现单例模式
logger=ColorfulLogger()