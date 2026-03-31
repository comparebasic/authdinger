"Data minipulation, usually moving form or query string informaion to the data object"
from ...utils import mapper
from ...utils.exception import PolyVinylNotOk, PolyVinylError, PolyVinylKnockout

def query_eq(req, ident, data):
    if not req.query_data.get(ident.location):
        raise PolyVinylKnockout()

    if ident.name and req.query_data[ident.location] != ident.name:
        raise PolyVinylKnockout()

def query_neq(req, ident, data):
    try:
        query_eq(req, ident, data)
    except PolyVinylKnockout:
        return

    raise PolyVinylKnockout()

def data_eq(req, ident, data):
    "Ensure a `data` key and value is present\n"
    "<name> is the value\n"
    "<location> is the key\n"
    req.server.logger.log("data_eq {} vs {}".format(data.get(ident.location), ident.name))
    if not data.get(ident.location):
        raise PolyVinylKnockout()

    if ident.name and data[ident.location] != ident.name:
        raise PolyVinylKnockout()


def data_neq(req, ident, data):
    "Ensure a `data` key and value is NOT present\n"
    "<name> is the value\n"
    "<location> is the key\n"
    try:
        data_eq(req, ident, data)
    except PolyVinylKnockout:
        return

    raise PolyVinylKnockout()


def form_eq(req, ident, data):
    req.server.logger.log("data_eq {} vs {}".format(data.get(ident.location), ident.name))
    if not req.form_data.get(ident.location):
        raise PolyVinylKnockout()

    if ident.name and req.form_data[ident.location] != ident.name:
        raise PolyVinylKnockout()


def form_neq(req, ident, data):
    try:
        form_eq(req, ident, data)
    except PolyVinylKnockout:
        return

    raise PolyVinylKnockout()

def map(req, ident, data):
    "Map key/value pairs to the `data` object\n"
    "<name> can be a comma seperated list of slash seperated key/value pairs \n"
    "<location> is the object to pull from\n"

    config = req.server.config
    kv = mapper.kv_from_ident(ident) 

    match ident.location:
        case "req":
            for k,v in kv.items():
                if not hasattr(req, v):
                    raise PolyVinylKnockout("Field not found for req {}".format(ident))

            data[key] = getattr(req, v)
        case "query" | "form" | "data" | "cookie" | "session" | "config":
            match ident.location:
                case "query":
                    source = req.query_data
                case "form":
                    source = req.form_data
                case "data":
                    source = data 
                case "cookie":
                    source = req.cookie
                case "session":
                    source = req.session
                case "config":
                    source = config 
                case _:
                    raise PolyVinylError("Map source not defined", ident)

    mapper.map(kv, source, data)
    req.server.logger.log("After Map {} {}".format(ident, data))
