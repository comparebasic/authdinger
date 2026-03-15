import socket
from ..utils.exception import \
     DingerNotOk, DingerError, DingerKnockout, DingerReChain
from ..utils import bstream, user, session, templ
from ..utils.maps import mime_map
from smtplib import SMTP
import smtplib


def map(req, ident, data):
    kv = {}
    for field in ident.name.split(","):
        parts = field.split("/")
        key = parts[0]
        if len(parts) == 1:
            val_key = parts[0]
        elif len(parts) == 2:
            val_key = parts[1]
        else:
            raise DingerError("Unparsable fields definition", ident.name)

        kv[key] = val_key


    match ident.location:
        case "req":
            for k,v in kv.items():
                if not hasattr(req, v):
                    raise DingerKnockout("Field not found for req {}".format(ident))

            data[key] = getattr(req, v)
        case "query" | "form" | "data" | "cookie" | "session":
            match ident.location:
                case "query":
                    source = req.query_data
                case "form":
                    source = req.form_data
                case "data":
                    source = data 
                case "cookie":
                    source = req.cookie
                case "session":
                    source = req.session
                case "config":
                    source = config 

            for k,v in kv.items():
                if v.endswith("?"):
                    v = v[:-1]
                    if k.endswith("?"):
                        k = k[:-1]
                    data[k] = source.get(v)
                else:
                    if not source.get(v):
                        raise DingerKnockout("Field not found for query {}".format(ident))
                    data[k] = source[v]

    req.server.logger.log("After Map {}".format(data))


def get(req, ident, data):
    if req.command != "GET":
        raise DingerKnockout("Method mismatch")


def post(req, ident, data):
    if req.command != "POST":
        raise DingerKnockout("Method mismatch")

def content(req, ident, data):
    config = req.server.config

    parts = ident.name.split(".")
    ext = parts[-1]

    mime = mime_map.get(ext)
    if mime:
        req.header_stage["Content-Type"] = mime;
    req.content += templ.templFrom(config, ident, data)


def data_eq(req, ident, data):
    req.server.logger.log("data_eq {} vs {}".format(data.get(ident.location), ident.name))
    if not data.get(ident.location):
        raise DingerKnockout()

    if ident.name and data[ident.location] != ident.name:
        raise DingerKnockout()


inc = static = page = content

def redir(req, ident, data):
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
    

def pw_auth(req, ident, data):
    config = req.server.config
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
                "pw_auth={}@email".format(data["email-token"]),
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

def token_consume(req, ident, data):
    pass


def session_start(req, ident, data):
    session.start(req, data)

    cookie = "Ssid={}; Expires={}; HttpOnly; Secure; SameSite=Strict;".format(
        data["session-token"], data["session-expires"])
    del data["session-token"]
    del data["session-expires"]
    req.header_stage["Set-Cookie"] = cookie


def session_open(req, ident, data):
    session.load(req, data)
    req.server.logger.log("Session {}".format(req.session))


def pw_set(req, ident, data):
    config = req.server.config
    if data.get("send-email-auth"):
        req.server.logger.log("Skipping pw_set")
        return

    if config.get("auth-socket"): 
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(config["auth-socket"]) 

        email_token = bstream.quote(data["email"]).decode("utf-8")
        bstream.send(sock, (
            "ident", 
                "pw_set={}@email".format(email_token),
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


def register(req, ident, data):
    config = req.server.config
    try:
        user.create(req, config, data)
    except DingerNotOk as err:
        raise DingerNotOk("Unable to register", err.args[0])


def email(req, ident, data):
    config = req.server.config
    msg = templ.emailMsgFromIdent(config, 
        ident, data,
        from_addr=config["system-email"], to_addrs=[config["email"]])

    with SMTP(config["smtp"]) as smtp:
        smtp.send_message(msg, from_addr=msg["From"], to_addrs=msg["To"])


def get_token(req, ident, data):
    config = req.server.config

    if config.get("auth-socket"): 
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(config["auth-socket"]) 

        email_token = bstream.quote(data["email"]).decode("utf-8")
        bstream.send(sock, (
            "ident", 
                "token_create={}@email".format(email_token),
            ""))

        answer = bstream.read_next(sock) 
        if answer != b"ok":
            reason = bstream.read_next(sock)
            sock.close()
            raise DingerNotOk("Invalid", reason)

        token = bstream.read_next(sock)
        data["token"] = token
        sock.close()

    else:
        raise DingerNotOk("No Auth Service Defined")


def auth_email(req, ident, data):
    if data.get("send-email-auth"):
        send_auth_email(req, ident, data)


def redir(req, ident, data):
    req.send_response(302)
    req.send_header("Location", data["redir"])
    for k,v in req.header_stage.items():
        req.send_header(k, v)
    req.end_headers()

