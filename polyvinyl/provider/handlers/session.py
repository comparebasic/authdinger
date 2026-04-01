"Session opening/closing and creation"
from .. import perms as perms_d, user, session, templ, form as form_d, maps,api as api_d
from ...auth import cli
from ...utils import token, mapper as map_d, config as config_d, chain, lin
from ...utils.exception import PolyVinylNotOk, PolyVinylError, PolyVinylKnockout


def session_start(req, ident, data):
    "Start a new session, assuming previous functions have validated the user\n"
    session.start(req)

    cookie = "Ssid={}; Expires={}; HttpOnly; Secure; SameSite=Lax;".format(
        data["session-token"], data["session-expires"])
    del data["session-token"]
    del data["session-expires"]
    req.header_stage["Set-Cookie"] = cookie


def session_open(req, ident, data):
    "Open an existing session, assuming previous functions have validated the user\n"
    session.load(req, data)
    req.server.logger.log("Session {}".format(req.session))


def session_close(req, ident, data):
    "Close a session, and remove the cookie from the browser\n"
    session.close(req, ident)
    cookie = "Ssid=; Expires={}; HttpOnly; Secure; SameSite=Strict;".format(
        "Thu, 01 Jan 1970 00:00:00 GMT")
    req.header_stage["Set-Cookie"] = cookie
