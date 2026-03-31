from ..utils.exception import PolyVinylError, PolyVinylKnockout

def kv_from_ident(ident):
    kv = {}
    for field in ident.name.split(","):
        parts = field.split("/")
        key = parts[0]
        if len(parts) == 1:
            val_key = parts[0]
        elif len(parts) == 2:
            val_key = parts[1]
        else:
            raise PolyVinylError("Unparsable fields definition", ident.name)

        kv[key] = val_key
    return kv


def map(kv, source, dest):
    for k,v in kv.items():
        if v.endswith("?"):
            v = v[:-1]
            if k.endswith("?"):
                k = k[:-1]
            dest[k] = source.get(v)
        else:
            if not source.get(v):
                raise PolyVinylKnockout("Field not found for query {}".format(v))
            dest[k] = source[v]
