import urllib

def parseFormData(s):
    data = {}
    for x in s.split("&"):
        pairs = x.split("=", 2)
        print(pairs)
        if len(pairs) == 2:
            k = pairs[0]
            v = pairs[1]
            data[k] = urllib.parse.unquote_plus(v, encoding=None, errors=None)
    print("{} -> {}".format(s, data))
    return data

def toQuery(config, data):
    query = ""
    for k, v in data.items():

        if query:
            query += "&"
        query += "{}={}".format(
            urllib.parse.quote(k, encoding=None, errors=None),
            urllib.parse.quote(v, encoding=None, errors=None))
    return query

def parseUrl(s):
    t = s.split("?")
    if len(t) == 1:
        return (t[0], None)
    return (t[0], t[1])

def compare_digest(config, ident, form, html, fields):
    h = hashlib.sha256()
    h.update(form)
    h.update(fields)
    h.update(html)
    digest = h.hexdigest()
    # compare to digets on disk


def gen_from(config, ident, content):
    # compare form json with cached form html
        # produce if mismatch
    # generate fields.json
        # produce if mismatch
    pass


def process_form(req, ident, data):
    # process form fields.json 
    pass
