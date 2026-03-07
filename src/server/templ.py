import os
import ident

def templFrom(config, ident, data):
    with open(os.path.join(config["template-dir"], path) as f:
        content = f.read()
        if ident.ext == "format":
            return content.format(**data)
        else:
            return content
