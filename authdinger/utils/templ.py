import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..utils.token import rfc822

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
            return content.format(**data)
        else:
            return content

def emailMsgFromIdent(config, ident, data, from_addr, to_addrs):
    subject_ident = "content={}.subject@{}".format(ident.name, ident.location)
    subject = templ.templFrom(config, subject_ident, data)

    text_ident = "content={}.txt@{}".format(ident.name, ident.location)
    text = templ.templFrom(config, text_ident, data)

    html_ident = "content={}.html@{}".format(ident.name, ident.location)
    html = templ.templFrom(config, html_ident, data)

    msg = MIMEMultiplart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ",".join(to_addrs)
    msg["Date"] = rfc822(datetime.now())
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    return msg
