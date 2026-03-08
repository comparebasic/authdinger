import socketserver, argparse, json, os, select
from log import GetLogger
from exception import DingerNotOk
from user_handler import Handler
import ident, bstream

STATE_LENGTH = "length"
STATE_KEY = "key"
STATE_VALUE = "value"
states = [STATE_LENGTH, STATE_KEY, STATE_VALUE]

class DingerUserHandler(socketserver.StreamRequestHandler):
    def handle(self):
        config = self.server.config

        more = True
        state = STATE_LENGTH
        content_state = STATE_KEY
        first = None

        data = {}

        content = b""
        while more != False:
            if state == STATE_LENGTH:
                length = 2
            cont = self.rfile.read(length)
            content += cont
            if len(content) == length:
                if state == STATE_LENGTH:
                    length = (int(content[0]) * 255) + int(content[1])
                    state = content_state
                elif state == STATE_KEY:
                    key = content
                    if key == b"end":
                        more = False
                    if not first:
                        first = key
                    content_state = STATE_VALUE
                    state = STATE_LENGTH 
                elif state == STATE_VALUE:
                    data[key] = content
                    content_state = STATE_KEY
                    state = STATE_LENGTH 

                content = b""
        
        if first:
            try:
                Handler(self, config, ident.Ident(first), data)
            except DingerNotOk as err:
                resp = bstream.add(b"", "ok")
                self.wfile.write(resp)

class DingerUserServer(socketserver.UnixStreamServer):
    def __init__(self, config, logger, handler_cls, bind_and_activate=True):
        self.config = config
        self.logger = logger
        return super().__init__(config["socket"], handler_cls, bind_and_activate)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Authdinger.User",
        description="ECAuth Socket Server")
    parser.add_argument("--config")
    arg = parser.parse_args()

    with open(arg.config, "r") as f:
        config = json.loads(f.read())

    print("Serving AuthDinger.Serve on {}".format(config["socket"]))
    streamd = DingerUserServer(config, GetLogger(config), DingerUserHandler) 

    try:
        streamd.serve_forever()
    except KeyboardInterrupt:
        pass
    streamd.server_close()
    os.remove(config["socket"])
    
