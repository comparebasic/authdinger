import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..utils.token import rfc822
from ..utils import identifier


def templFrom(config, ident, data):
    templ_dir = None
    if ident.location:
        templ_dir = config["dirs"].get(ident.location);
    else:
        templ_dir = config["dirs"].get("page");
            
    parts = ident.name.split(".")
    ext = parts[-1]
    with open(os.path.join(templ_dir, ident.name), "r") as f:
        content = f.read()
        if ext == "format":
            try:
                return content.format(**data)
            except KeyError as err:
                raise DingerError("Key Error in templ", err, data) 
        else:
            return content


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

    msg = MIMEMultiplart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ",".join(to_addrs)
    msg["Date"] = rfc822(datetime.now())
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    return msg
