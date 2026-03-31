import json, types
from .maps import mime_map

def handlers(req, mod):
    print(mod)
    data = {
        "module-name": mod.__name__,
        "module-desc": mod.__doc__
    }
    for k,v in mod.__dict__.items():
        if isinstance(v, (types.FunctionType)) and not v.__name__.startswith("_"):
            data[k] = {
                "name": k,
                "desc": v.__doc__
            }

    req.header_stage["Content-Type"] = mime_map["json"]
    return json.dumps(data)


def config(req, mod):
    req.header_stage["Content-Type"] = mime_map["json"]
    return json.dumps(config)
