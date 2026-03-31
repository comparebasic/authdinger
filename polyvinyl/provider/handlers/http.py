"Http request details such as moving request data or verifying request mothod"
from ...utils.exception import PolyVinylKnockout


def set_query(req, ident, data):
    "Reset the Request.query object to the `<map>` body arguments provided" 
    req.query_data = {}
    if ident.name:
        _map(req, ident, data, req.query_data)


def get(req, ident, data):
    "Ensure Request method is GET"
    if req.command != "GET":
        raise PolyVinylKnockout("Method mismatch")


def post(req, ident, data):
    "Ensure Request method is POST"
    if req.command != "POST":
        raise PolyVinylKnockout("Method mismatch")
