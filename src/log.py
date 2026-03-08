class Log(object):
    def log(self, message, obj):
        print("Log: {} {}".format(message, obj))

    def error(self, message, obj):
        print("\x1b[31mError: {} {}\x1b[0m".format(message, obj))

def GetLogger(config):
    return Log()
    
