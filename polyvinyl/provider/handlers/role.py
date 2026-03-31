"Role assignemnts and updates, interacts the most with the Auth service"
from .. import user, session, templ, form as form_d, api as api_d
from ..maps import mime_map
from ...auth import cli
from ...utils import chain, lin, token, mapper as map_d,  config as config_d
from ...utils.exception import PolyVinylNotOk, PolyVinylError, PolyVinylKnockout


def get_token(req, ident, data):
    "Call the Auth service to create a new token\n"
    config = req.server.config

    if config.get("auth-socket"): 
        email_token = lin.quote(data["email"]).decode("utf-8")
        six_code = cli.query_path(config["auth-socket"], req.server.key, (
            "ident", 
                "get_signin_code={}@email".format(email_token),
        ))
        data["six-code"] = six_code.decode("utf-8")
    else:
        raise PolyVinylNotOk("No Auth Service Defined")

def pw_set(req, ident, data):
    "Call the Auth service to set a users password\n"
    config = req.server.config
    if config.get("auth-socket"): 
        if req.form_data.get("password"):
            email_token = lin.quote(data["email"]).decode("utf-8")
            password_hash = user.pw_hash(req, email_token, req.form_data["password"])
            cli.query_path(config["auth-socket"], req.server.key, (
                "ident", 
                    "pw_set={}@email".format(email_token),
                "password-hash",
                    password_hash 
            ))
    else:
        raise PolyVinylNotOk("No Auth Service Defined")


def register(req, ident, data):
    "Call the Auth service to register a new user\n"
    config = req.server.config
    try:
        user.create(req, config, data)
    except PolyVinylNotOk as err:
        raise PolyVinylNotOk("Unable to register", err.args[0])

    if config.get("auth-socket"): 
        email_token = lin.quote(data["email"]).decode("utf-8")
        cli.query_path(config["auth-socket"], req.server.key, (
            "ident", 
                "register={}@email".format(email_token),
            ))

        data["email-token"] = email_token
    else:
        raise PolyVinylNotOk("No Auth Service Defined")


def unsubscribe(req, ident, data):
    print("unsubscribe")


def pw_auth(req, ident, data):
    "Call the Auth service to validate a password\n"
    config = req.server.config
    if config.get("auth-socket"): 
        email_token = lin.quote(data["email"]).decode("utf-8")
        password_hash = user.pw_hash(req, email_token, req.form_data["password"])
        del req.form_data["password"]

        cli.query_path(config["auth-socket"], req.server.key, (
            "ident",     
                "pw_auth={}@email".format(email_token),
            "password-hash",
                password_hash
        ))
    else:
        raise PolyVinylNotOk("No Auth Service Defined")



def role(req, ident, data):
    "Call the Auth service to validate and consume a login six-code\n"
    config = req.server.config
    if req.role.get(ident.name):
        return

    if config.get("auth-socket"): 
        email_token = lin.quote(data["email"]).decode("utf-8")

        cli.query_path(config["auth-socket"], req.server.key, (
            "ident",     
                "role_check={}@{}".format(ident.name, email_token),
            "six-code",
                data["code"]
            ))

        del data["code"]

        up = {}
        up["email-token"] = email_token
        up[ident.name] = True
        req.role.update(up)

        raise PolyVinylNotOk("No Auth Service Defined")


def token_consume(req, ident, data):
    "Call the Auth service to validate and consume a login token\n"
    config = req.server.config
    if config.get("auth-socket"): 
        email_token = lin.quote(data["email"]).decode("utf-8")

        cli.query_path(config["auth-socket"], req.server.key, (
            "ident",     
                "token_consume={}@email".format(email_token),
            "token",
                data["code"],
            ))

        del data["token"]
    else:
        raise PolyVinylNotOk("No Auth Service Defined")


