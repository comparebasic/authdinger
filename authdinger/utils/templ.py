import os

def templFrom(config, ident, data):
    templ_dir = None
    if ident.location:
        templ_dir = config["dirs"].get(ident.location);
    else:
        templ_dir = config["dirs"].get("page");
            
    parts = ident.name.split(".")
    ext = parts[-1]
    with open(os.path.join(templ_dir, ident.name), "r") as f:
        content = f.read()
        if ext == "format":
            return content.format(**data)
        else:
            return content
