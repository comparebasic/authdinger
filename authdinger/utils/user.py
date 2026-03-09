import os, urllib, random, bcrypt
from .bstream import quote, unquote, send_r, read_next_r
from .exception import DingerNotOk 
from .. import SALT_BYTES

def create(req, config, data):
    email_token = quote(data["email"])
    req.server.logger.log("Email Token {}".format(email_token))
    fname = "{}.rseg".format(email_token.decode("utf-8"))
    path = os.path.join(config["dirs"]["user-data"],fname)

    req.server.logger.log("Email Token Value {}".format(unquote(email_token)))

    if os.path.exists(path):
        req.server.logger.log("User Exists {}".format(path))
        raise DingerNotOk("User Exists")
    
    data["salt"] = bcrypt.gensalt()
    data["password-hash"] = bcrypt.hashpw(
        data["password"].encode("utf-8"), data["salt"])
    del data["password"]

    details = [
        "email-token", email_token,
        "fullname", data["fullname"],
        "salt", data["salt"]]

    req.server.logger.log("Create User {}".format(details))
    with open(path, "wb+") as f:
        send_r(f, details) 

        
