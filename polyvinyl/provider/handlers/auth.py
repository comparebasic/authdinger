"Page or asset level permission gates"
from ...utils.exception import PolyVinylKnockout, PolyVinylNoAuth
from .. import perms as perms_d
 

def auth(req, ident, data):
    if not hasattr(perms_d, ident.name):
        raise PolyVinylNoAuth(ident)
    
    func = getattr(perms_d, ident.name)
    func(req, req.role, data)


def try_auth(req, ident, data):
    try:
        auth(req, ident, data)
    except PolyVinylNoAuth as no_auth:
        raise PolyVinylKnockout(ident, *no_auth.args)
