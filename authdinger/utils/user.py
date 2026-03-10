import os, urllib, random, bcrypt
from ..utils import bstream
from .exception import DingerNotOk 
from .. import SALT_BYTES, SEEK_END, SEEK_CUR, SEEK_START

def get_userdir(config, email_token):
    return os.path.join(config["dirs"]["user-data"], email_token)

def get_userfile(config, email_token):
    return os.path.join(get_userdir(config, email_token),
                "details.linr")

def create(req, config, data):
    email_token = bstream.quote(data["email"])
    path = get_userfile(config, email_token.decode("utf-8"))

    req.server.logger.log("Email Token Value {}".format(
        bstream.unquote(email_token)))

    if os.path.exists(path):
        req.server.logger.log("User Exists {}".format(path))
        raise DingerNotOk("User Exists")
    
    data["salt"] = bcrypt.gensalt()
    data["password-hash"] = bcrypt.hashpw(
        data["password"].encode("utf-8"), data["salt"])
    del data["password"]

    details = [
        "email-token", email_token,
        "email", data["email"],
        "fullname", data["fullname"],
        "salt", data["salt"]]

    req.server.logger.log("Create User {}".format(details))
    os.mkdir(get_userdir(config, email_token.decode("utf-8")))
    with open(path, "wb+") as f:
        bstream.send_r(f, details) 

        
def pw_hash(req, config, data):
    path = get_userfile(config, data["email-token"])

    with open(path, "rb") as f:
        f.seek(0, SEEK_END)
        
        if f.tell() == 0:
            raise DingerNotOk("Empty User File")

        value = bstream.latest_r(f, b"salt")
        password = data["password"].encode("utf-8")
        del data["password"]

        return bcrypt.hashpw(password, value)
