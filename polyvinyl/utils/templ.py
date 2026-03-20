import os
from datetime import datetime
from dateutil.tz import tzlocal
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..utils.token import rfc822
from ..utils import identifier
from ..utils.exception import PolyVinylError, PolyVinylReChain


def templFrom(config, ident, data):
    templ_dir = None
    if ident.location:
        templ_dir = config["dirs"].get(ident.location);
    else:
        templ_dir = config["dirs"].get("page");
            
    parts = ident.name.split(".")
    ext = parts[-1]
    try:
        with open(os.path.join(templ_dir, ident.name), "r") as f:
            content = f.read()
            if ext == "format":
                try:
                    return content.format(**data)
                except KeyError as err:
                    raise PolyVinylError("Key Error in templ", err) 
            else:
                return content
    except FileNotFoundError as err:
        raise PolyVinylError(err.args[0], err)


def emailMsgFromIdent(config, ident, data, from_addr, to_addrs):
    subject_ident = identifier.Ident(
        "content={}_subject.format@{}".format(ident.name, ident.location))
    subject = templFrom(config, subject_ident, data)

    text_ident = identifier.Ident(
        "content={}_txt.format@{}".format(ident.name, ident.location))
    text = templFrom(config, text_ident, data)

    html_ident = identifier.Ident(
        "content={}_html.format@{}".format(ident.name, ident.location))
    html = templFrom(config, html_ident, data)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ",".join(to_addrs)
    msg["Date"] = rfc822(datetime.now(tzlocal()))
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    return msg
