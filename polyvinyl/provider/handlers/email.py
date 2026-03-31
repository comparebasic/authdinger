"Email sending, generation is largely done using the same templ as page composition" 
from .. import user, session, templ, form as form_d, api as api_d
from ...auth import cli
from ...utils import chain, lin, token, config as config_d
from ...utils.exception import PolyVinylNotOk, PolyVinylError, PolyVinylKnockout
from smtplib import SMTP


def newsletter(req, indent, data):
    req.server.logger.debug("Newsletter signup {}".format(data))

def email(req, ident, data):
    "Send an email\n"
    config = req.server.config

    if not data.get('email-token'):
        data["email-token"] = lin.quote(data["email"]).encode("utf-8")

    data.update(user.get_subscription_urls(req, data["email-token"]))

    req.server.logger.debug("Data for email {} {}".format(ident, data))

    msg = templ.email_msg_from_ident(req, 
        ident,
        data,
        from_addr=config["system-email"],
        to_addrs=[data["email"]])

    try:
        with SMTP(config["smtp"]) as smtp:
            smtp.send_message(msg, from_addr=msg["From"], to_addrs=msg["To"])
    except Exception as err:
        req.server.logger.log(err, data)
        raise PolyVinylNotOk(err)


def set_token_url(req, ident, data):
    "Create the token url, usually for inclusion in an email\n"
    if not data.get('email-token'):
        data["email-token"] = lin.quote(data["email"]).decode("utf-8")
    
    data["login-url"] = "{}{}?email={}&six-code={}".format(
        data["url"], ident.name, data["email-token"], data["six-code"])
