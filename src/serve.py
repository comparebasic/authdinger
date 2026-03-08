import argparse, json, urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
import templ, ident, form, handlers
from log import GetLogger
from exception import DingerNotOk

class DingerServer(HTTPServer):
    def __init__(self, config, logger, address, port):
        self.config = config
        self.logger = logger
        if config.get("user_socket"):
            self.user_server = socket.socket(
                socket.AF_UNIX, socket.SOCK_STREAM)
            self.user_server.connect(config["user_socket"])
        else:
            self.user_server = None

        return super().__init__(address, port)

class DingerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        config = self.server.config

        path, query = form.parseUrl(self.path)

        route = config["routes"].get(path)
        if not route:
            self.send_response(404)
            route = config["routes"]["/not-found"]
        else:
            self.send_response(200)

        self.send_header("Content-type", "text/html")
        self.end_headers()

        data = {}

        data["action"] = path
        if query:
            params = form.parseFormData(query)
            data.update(params)
        else:
            data["redir"] = None
    
        if not data.get("error"):
            data["error"] = None
            
        print(data)
        content = ""
        for p in route:
            p_ident = ident.Ident(p)
            content += templ.templFrom(config, p_ident, data)

        self.wfile.write(bytes(content, "utf-8"))

    def do_POST(self):
        path, _ = form.parseUrl(self.path)

        config = self.server.config
        handler = config["handlers"].get(path)

        if not handler:
            self.path = "/not-found"
            return self.do_GET()

        data = {}

        length = self.headers.get("Content-Length")
        if length:
            content = self.rfile.read(int(length))

            params = form.parseFormData(content.decode("utf-8"))
            if params:
                for k,v in params.items():
                    params[k] = urllib.parse.unquote(v,
                        encoding=None, errors=None)
                data.update(params)
        
        for h in handler:
            h_ident = ident.Ident(h)
            try:
                handlers.Handle(self, config, h_ident, data)
            except DingerNotOk as err:
                knockout = config["knockouts"].get(path)
                if knockout:
                    k_ident = ident.Ident(knockout)
                    if k_ident.tag == "get":
                        data["error"] = err.args[0]
                        self.path = "{}?{}".format(
                            k_ident.source, 
                            form.toQuery(config, data))
                        self.do_GET()
                        return

                self.server.logger.error("handler error", err)
                self.server.logger.error("handler error", h_ident)
                self.path = "/error"
                return self.do_GET()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Authdinger.Serve",
        description="ECAuth Provider Server")
    parser.add_argument("--port")
    parser.add_argument("--config")
    arg = parser.parse_args()

    try:
        port = int(arg.port)
    except (ValueError, TypeError) as err:
        raise ValueError("Expected interger for port number", err)

    with open(arg.config, "r") as f:
        config = json.loads(f.read())
        handlers.setup(config)

    print("Serving AuthDinger.Serve on port {}".format(port))
    httpd = DingerServer(config,
        GetLogger(config), ('localhost', port), DingerHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
