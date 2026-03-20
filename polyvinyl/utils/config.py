import argparse, json
from ..utils import identifier
from ..lin import unquote

def ParseConfig(path):
    with open(path, "r") as f:
        config = json.loads(f.read())
        return config

def ParseCli():
    parser = argparse.ArgumentParser(
        prog="PolyVinyl",
        description="PolyVinyl Server")
    parser.add_argument("--config")
    parser.add_argument("--log-color", action="store_true")
    parser.add_argument("--type", choices=["provider", "auth", "sasl"], required=False)
    return parser.parse_args()

def map_keys(keys, items, data):
    print(data)
    for k, v in items.items():
        if not keys:
            if isinstance(v, (bytes)):
                v = v.decode("utf-8")
            data[k] = v 

        elif keys[k]:
            value = v
            if isinstance(keys[k], (str)):
                ident = identifier.Ident(keys[k])
                if ident.tag == "unquote":
                    print("unquoting {}".format(ident))
                    value = unquote(value)
                if ident.name:
                    k = ident.name

            if isinstance(value, (bytes)):
                value = value.decode("utf-8")
            print("Assigning {} -> {}".format(k, value))
            data[k] = value 
    print(data)
    return data
