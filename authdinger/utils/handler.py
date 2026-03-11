
def do_chain(req, chain, data fmap):
    "This function goes through the chain, and tries each branch until one"
    "completes or there are no more to try."
    if req.done:
        return

    for h in chain:
        if isinstance(h, (list)):
            try:
                # go through this branch of the chain
                return do_chain(req, h, data, hmap)
            except DingerNotOk as err:
                # go to the next branch
                data["error"] = err.args[0]
                continue

        h_ident = ident.Ident(h)
        try:

            match h_ident.tag:
                case "get":
                    if req.command != "GET":    
                        raise DingerNotOk("Method mismatch")
                case "post":
                    if req.command != "POST":
                        raise DingerNotOk("Method mismatch")

                case "inc" | "static" | "page":
                    mime = ext_mime.get(p_ident.ext)
                    if mime:
                        self.header_stage["Content-Type"] = mime;
                    content += templ.templFrom(config, p_ident, data)

                case "func":
                    if fmap.get(h_ident.base): 
                        func(req, config, data)
                    else:
                        raise DingerNotOk("Not func found for handler {}".format(ident))

                case "redir":
                    req.send_response(302)
                    location = h_ident.base
                    if h_ident.tag == "data":
                        location = data.get(h_ident.base)

                    if not location:
                        location = "/error"
                        
                    req.send_header("Location", location)
                    for k,v in req.header_stage.items():
                        req.send_header(k, v)
                    req.end_headers()
                    req.done = True

            if not func:

        except DingerNotOk as err:
            data["error"] = err.args[0]
            raise

def Handle(req, chain, data, fmap):
    try:
        do_chain(req, chain, data, fmap)
    except DingerNotOk as err:
       raise 

    if not req.done:
        for k,v in self.header_stage.items():
            self.send_header(k, v)
        self.end_headers()

        self.wfile.write(bytes(content, "utf-8"))

    req.done = True
