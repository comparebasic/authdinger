import os, bcrypt, time
from datetime import datetime
from ..utils.exception import DingerNotOk
from ..utils import bstream
from ..utils import token
from .. import SEEK_END, SEEK_CUR, SEEK_START


def get_authdir(config, email_token):
    return os.path.join(config["dirs"]["auth-data"], email_token)

def get_authfile(config, email_token):
    return os.path.join(get_authdir(config, email_token),
                "auth.linr")

def get_tokenfile(config, email_token, token):
    return os.path.join(
            os.path.join(
                get_authdir(config, email_token),
                "tokens"),
            token)


def pw_auth(req, ident, data):
    config = req.server.config
    req.server.logger.log("Auth Password {}".format(
        bstream.unquote(ident.name)))

    path = get_authfile(config, ident.name)

    with open(path, "rb") as f:
        f.seek(0, SEEK_END)
        
        if f.tell() == 0:
            raise DingerNotOk("Empty User File")

        value = bstream.latest_r(f, b"password-hash")

    req.server.logger.log("Auth Password data {} vs pw {}".format(data, value))

    if value != data["password-hash"]:
        raise DingerNotOk("password mismatch")


def pw_set(req, ident, data):
    config = req.server.config
    req.server.logger.log("Setting Password {}".format(
        bstream.unquote(ident.name)))


    dir_path = get_authdir(config, ident.name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        os.mkdir(os.path.join(dir_path, "tokens"))

    path = get_authfile(config, ident.name)
    with open(path, "wb") as f:
        f.seek(0, SEEK_END)
        details = ["password-hash", data["password-hash"]]
        bstream.send_r(f, details)


def register(req, ident, data):
    config = req.server.config
    req.server.logger.log("Register {}".format(
        bstream.unquote(ident.name)))

    dir_path = get_authdir(config, ident.name)
    if os.path.exists(dir_path):
        raise DingerNotOk("User already exists")

    os.mkdir(dir_path)
    os.mkdir(os.path.join(dir_path, "tokens"))

    path = get_authfile(config, ident.name)
    with open(path, "wb") as f:
        details = ["email-token", ident.name, 
            "register-time", token.time_bytes(time.time())]

        bstream.send_r(f, details)


def token_create(req, ident, data):
    config = req.server.config
    email_token = ident.name
    req.server.logger.log("Setting Token {}".format(
        bstream.unquote(ident.name)))

    dir_path = get_authdir(config, email_token)
    if not os.path.exists(dir_path):
        raise DingerNotOk("User dir not found")

    tk = token.get_short_token(email_token.encode("utf-8"))
    path = get_tokenfile(config, email_token, tk)

    with open(path, "w+") as f:
        f.write(token.rfc822(datetime.now()))

    return tk


def token_consume(req, ident, data):
    config = req.server.config
    req.server.logger.log("Consuming Token {}".format(
        bstream.unquote(ident.name)))

    email_token = ident.name
    dir_path = get_authdir(config, email_token)
    if not os.path.exists(dir_path):
        raise DingerNotOk("User dir not found", dir_path)

    tk = data["token"].decode("utf-8") 
    path = get_tokenfile(config, ident.name, tk)

    if not os.path.exists(path):
        raise DingerNotOk("Invalid", path)

    os.remove(path)
    del data["token"]

    req.server.logger.log("Token Consumed {}".format(path))
