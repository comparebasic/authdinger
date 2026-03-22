import urllib, json

from ..utils import identifier

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


def render_item(ident, optional=False, content=""):
    name = ident.location
    value = None 
    if ident.tag == "radio" or ident.tag == "button":
        parts = name.split("/")
        if len(parts) == 2:
            name = parts[1]
            value = parts[0]

    if ident.tag == "button":
        return "<button type=\"submit\" name=\"{}\" value=\"{}\">{}</button><br />".format(
            " name={}".format(name) if name else "",
            " value={}".format(value) if value else "",
            ident.name)

    if ident.tag == "fieldset":
        return "\n<fieldset>{}</fieldset>".format(content)
    elif ident.tag == "input" or ident.tag == "password":
        return "{}<label{}><span class=\"label-text\">{}</span><input type=\"{}\" name=\"{}\"{} /><span class=\"marker valid\">&check;</span><span class=\"marker invalid\">&#10005;</span>{}{}</label><br />".format(
            "<br/>" if optional else "",
            " class=\"optional\"" if optional else "",
            ident.name,
            ident.tag,
            name,
            " value=\"{}\"".format(value) if value else "",
            "<span class=\"marker eye\">&#128065;</span>" if ident.tag == "password" else "",
            content)
    else:
        return "{}<label{}><input type=\"{}\" name=\"{}\"{} /><span class=\"label-text\">{}</span>{}</label><br />".format(
            "<br/>" if optional else "",
            " class=\"optional\"" if optional else "",
            ident.tag,
            name,
            " value=\"{}\"".format(value) if value else "",
            ident.name,
            content)


def rev_gen_loop(ident, chain, data, content=""):
    top = len(chain)-1
    for i, v in enumerate(reversed(chain)):
        print(v)
        print(content)
        if isinstance(v, (list)):
            content += gen_loop(ident, data, v)
        else:
            print(v)
            ident = identifier.Ident(v)
            content = render_item(ident, i < top, content)

    return content


def gen_loop(ident, data, chain):
    content = ""
    for v in chain:
        content += "\n"
        if isinstance(v, (str)):
            ident = identifier.Ident(v)
            match ident.tag:
                case "input" | "checkbox" | "button" | "option" | \
                        "radio" | "fieldset" | "password":
                    content += render_item(ident)
        elif isinstance(v, (list)):
            content += rev_gen_loop(ident, v, data)

    return content

def gen_script(ident, form_jsid, validation):
    content = "<script type=\"text/javascript\">"
    content += "window._polyvinyl.form.register(\"{}\", {})".format(
        form_jsid,
        json.dumps(validation)
    )
    content += "</script>"
    return content


def gen_html(req, ident, data, config_data):
    form_jsid = "form_jsid{}".format(req.get_unique())
    req.content += "<form id=\"{}\" method=\"POST\" action=\"{}\">".format(
        form_jsid,
        config_data["action"])
    req.content += gen_loop(ident, data, config_data["idents"])
    req.content += gen_script(ident, form_jsid, config_data["validation"])
    req.content += "</form>"


def process_form(req, ident, data):
    # process form fields.json 
    pass
