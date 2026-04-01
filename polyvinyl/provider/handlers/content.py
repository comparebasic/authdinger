"Content composition including submitting and loading forms or composing pages" 
import sys, json
from .. import perms as perms_d, user, session, templ, form as form_d, api as api_d
from ..maps import mime_map
from ...utils import chain, lin,  token, config as config_d
from ...utils.exception import PolyVinylNotOk, PolyVinylError, PolyVinylKnockout
from ...auth import cli


def idents(req, ident, data):
    "Inject identifiers that are listed in a file into the chain during runtime\n"
    "Any directory can have a file listing Identifiers.\n"
    "If <location> is `user` the user folder will be used and a user must be set in the session\n"
    chain.idents(req, ident, data)

def title(req, ident, data):
    data["title"] = ident.name


def content(req, ident, data):
    "Load and process content from templates into the Requests output response buffer\n"
    "Expected <location> types are `stache`, `format` or web file extension `html/css/js/txt`\n"
    config = req.server.config

    parts = ident.name.split(".")
    ext = parts[-1]

    mime = mime_map.get(ext)
    if mime:
        req.header_stage["Content-Type"] = mime;
    req.content += templ.templ_from(req, ident, data)


def save_amend(req, ident, data):
    return save_form(req, ident, data, amend=True)

def form(req, ident, data):
    config = req.server.config
    path, ext = config_d.get_path_ext(config, ident)
    if ext == "json":
        with open(path, "r") as f:
            config_data = json.loads(f.read())
            form_d.gen_html(req, ident, data, config_data)


def redir(req, ident, data):
    "Populate the Request headers for a redirect to another url\n"

    if ident.location == "data":
        location = data.get(ident.name)
    else:
        location = ident.name

    req.server.logger.warn("Redir 304 {}".format(location))
    session.redir(req, location)


def api(req, ident, data):
    "Returns data about the handlers and the configuration"
    config = req.server.config
    if ident.name == "handlers":
        req.content += api_d.handlers(req, sys.modules.get(__name__))

    if ident.name == "config":
        req.content  += api_d.config(req, sys.modules(__name__))


def end(req, ident, data):
    "Set the request complete and ready to respond\n"
    req.done = True
    raise PolyVinylKnockout()



inc = static = page = content
