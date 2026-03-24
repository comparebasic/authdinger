from ..utils import nav as nav_d
from . import perms

def nav(server):
    nav_d.setup_nav(server, perms)
