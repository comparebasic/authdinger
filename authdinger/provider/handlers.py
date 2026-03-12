import socket
from .. import DingerNotOk
from ..utils import bstream, user, session


def get(req, config, ident, data):
    if req.command != "GET":
        raise DingerKnockout("Method mismatch")


def post(req, config, ident, data):
    if req.command != "POST":
        raise DingerKnockout("Method mismatch")

def content(req, config, ident, data):
    mime = ext_mime.get(p_ident.location)
    if mime:
        req.header_stage["Content-Type"] = mime;
    req.content += templ.templFrom(config, p_ident, data)


def data(req, config, ident, data):
    if not data.get(ident.location):
        raise DingerKnockout()

    if ident.name and data[ident.location] != ident.name:
        raise DingerKnockout()


inc = static = page = content

def redir(req, config, ident, data):
    req.send_response(302)
    if ident.location == "data":
        location = data.get(ident.name)
    else:
        location = ident.name

    if not location:
        location = "/error"
        
    req.send_header("Location", location)
    for k,v in req.header_stage.items():
        req.send_header(k, v)
    req.end_headers()
    req.done = True
    

def pw_auth(req, config, ident, data):
    if data.get("send-email-auth"):
        req.server.logger.log("Skipping pw_auth")
        return

    if config.get("auth-socket"): 
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(config["auth-socket"]) 

        data["email-token"] = bstream.quote(data["email"]).decode("utf-8")
        password_hash = user.pw_hash(req, config, data)

        bstream.send(sock, (
            "ident",     
                "pw_auth@{}.email".format(data["email-token"]),
            "password-hash",
                password_hash, 
            ""))

        answer = bstream.read_next(sock) 
        if answer != b"ok":
            reason = bstream.read_next(sock)
            sock.close()
            raise DingerNotOk("Invalid", reason)

        sock.close()

    else:
        raise DingerNotOk("No Auth Service Defined")

def token_consume(req, config, ident, data):
    pass


def session_start(req, config, ident, data):
    session.start(req, config, ident, data)

    cookie = "Ssid={}; Expires={}; HttpOnly; Secure; SameSite=Strict;".format(
        data["session-token"], data["session-expires"])
    req.header_stage["Set-Cookie"] = cookie


def pw_set(req, config, ident, data):
    if data.get("send-email-auth"):
        req.server.logger.log("Skipping pw_set")
        return

    if config.get("auth-socket"): 
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(config["auth-socket"]) 

        email_token = bstream.quote(data["email"]).decode("utf-8")
        bstream.send(sock, (
            "ident", 
                "pw_set@{}.email".format(email_token),
            "password-hash",
                data["password-hash"], 
            ""))

        answer = bstream.read_next(sock) 
        if answer != b"ok":
            reason = bstream.read_next(sock)
            sock.close()
            raise DingerNotOk("Invalid", reason)

        sock.close()

    else:
        raise DingerNotOk("No Auth Service Defined")


def gather_user(req, config, ident, data):
    pass


def register(req, config, ident, data):
    try:
        user.create(req, config, data)
    except DingerNotOk as err:
        raise DingerNotOk("Unable to register", err.args[0])


def send_email(req, config, ident, data):
    pass


def send_auth_email(req, config, ident, data):
    req.server.logger.log("Send auth email")
    return


def auth_email(req, config, ident, data):
    if data.get("send-email-auth"):
        send_auth_email(req, config, ident, data)


def redir(req, config, ident, data):
    req.send_response(302)
    req.send_header("Location", data["redir"])
    for k,v in req.header_stage.items():
        req.send_header(k, v)
    req.end_headers()

