from exception import DingerNotOk

def Handle(req, config, ident, data):
    func = None
    if ident.tag == "action":
        func = config["_handler-action"].get(ident.base)
    elif ident.tag == "func":
        func = config["_handler-func"].get(ident.base)

    if not func:
        raise DingerNotOk("Not func found for handler {}".format(ident))

    func(req, config, data)


def pw_auth(req, config, data):
    if data.get("password") == "password" and data.get("user") == "test":
        print("pw pass")
        return
    else:
        raise DingerNotOk("auth fail")


def redir(req, config, data):
    req.send_response(307)
    req.send_header("Location", data["redir"])
    req.end_headers()
    print("sending redir headers")


def setup(config):
    config["_handler-func"] = {
        "pw_auth": pw_auth,
    }
    config["_handler-action"] = {
        "redir": redir,
    }
    
