from ..utils.exception import PolyVinylNoAuth


def session(req, ident, data):
    if not req.session:
        raise PolyVinylNoAuth("session", req.session)


def no_session(req, ident, data):
    if req.session:
        raise PolyVinylNoAuth("no session")


def user(req, ident, data):
    if req.role.get("user") and req.role["user"] != ident.location:
        raise PolyVinylNoAuth("Not user", ident)


def member(req, ident, data):
    if req.role.get("group") and req.role["group"].index(ident.location) == -1:
        raise PolyVinylNoAuth("Not member", ident)

    user(req, ident, data)
