from . import colors
from datetime import datetime

class Log(object):
    def __init__(self, color=False):
        self.color = color

    def _log(self, level, message, obj, color):
        if obj:
            if self.color and color:
                print("\x1b[{}m{} {}: {} {}\x1b[0m".format(
                    color, level, datetime.now(), message, obj))
            else:
                print("{} {}: {} {}".format(level, datetime.now(), message, obj))
        else:
            if self.color and color:
                print("\x1b[{}m{} {}: {}\x1b[0m".format(
                    color, level, datetime.now(), message))
            else: 
                print("{} {}: {}".format(level, datetime.now(), message))


    def debug(self, message, obj=None):
        self._log("Debug", message, obj, colors.PURPLE)

    def log(self, message, obj=None):
        self._log("Log", message, obj, colors.CYAN)

    def warn(self, message, obj=None):
        self._log("Warn", message, obj, colors.YELLOW)

    def error(self, message, obj=None):
        self._log("Error", message, obj, colors.RED)

def GetLogger(config):
    return Log(config.get("log-color"))
    
