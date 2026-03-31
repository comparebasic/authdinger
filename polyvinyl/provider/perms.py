from ..utils.exception import PolyVinylNoAuth

def make_nav(req, ident, data, path):
    nav_kv = {}
    for _, nav in req.server.nav.lookup.items():
        if nav.perms:
            try:
                for inst in nav.perms:
                    # knockout if permission fails
                    inst.func(req, ident, data) 
            except PolyVinylNoAuth:
                continue

        if nav.path == path:
            nav_kv[nav.name] = True
        else:
            nav_kv[nav.name] = nav.path

    return nav_kv


def ident_perm(req, ident):
    pass 


def role(req, ident, _):
    role_name = ident.name
    if not req.role.get(role_name):
        raise PolyVinylNoAuth(ident)


def session(req, ident, _):
    if not req.session or not req.role.get("signin"):
        raise PolyVinylNoAuth(ident)
        

def no_session(req, ident, _):
    if req.session and req.role.get("signin"):
        raise PolyVinylNoAuth(ident)
