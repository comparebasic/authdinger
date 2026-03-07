import argparse, json
from http.server import BaseHTTPRequestHandler, HTTPServer
import templ, ident

class PageHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        print("HEAD {}".format(self))

    def do_GET(self):
        print(self.server)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><head><title>Example Login</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Authdinger.Serve",
        description="OAuth Provider Server")
    parser.add_argument("--port", "--config")
    arg = parser.parse_args() 

    try:
        port = int(arg.port)
    except:
        raise ValueError("Expected interger for port number", port)

    with open(arg.config, "r") as f:
        config = json.loads(f.read())

    print("Serving AuthDinger.Serve on port {}".format(port))
    httpd = HTTPServer(('localhost', port), PageHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
