import argparse, json

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
