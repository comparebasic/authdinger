BSTREAM_MAX = 2048
SALT_BYTES = 64
SESS_BYTES = 64

SEEK_START = 0
SEEK_CUR = 1
SEEK_END = 2
SESSION_DAYS = 14

from .auth.serve import PolyVinylAuthServer
from .provider.serve import PolyVinylProviderServer
from .utils import chain, lin
from .utils.config import ParseConfig, ParseCli

__all__ = [
    "ParseConfig", "ParseCli", \
    "PolyVinylAuthServer", "PolyVinylProviderServer", \
    "ParseConfig", "ParseCli", "chain", "lin"
]

__version__ = "0"
__author__ = "Compare Basic"

