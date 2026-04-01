import os
from polyvinyl import  PolyVinylAuthServer, PolyVinylProviderServer
from polyvinyl.utils.log import GetLogger
from polyvinyl.utils.config import ParseConfig, ParseCli


def run_auth(config, logger):
    logger.log("Serving PolyVinyl Auth Auth on socket {}".format(config["auth-socket"]))
    streamd = PolyVinylAuthServer(config, logger) 

    try:
        streamd.serve_forever()
    finally:
        streamd.server_close()
        os.remove(config["auth-socket"])


def run_provider(config, logger):
    try:
        port = int(config["port"])
    except (ValueError, TypeError) as err:
        raise ValueError("Expected interger for port number", err)

    logger.log("Serving PolyVinyl Provider on port {}".format(port))
    httpd = PolyVinylProviderServer(config,
        GetLogger(config), ('localhost', port))

    try:
        httpd.serve_forever()
    finally:
        httpd.server_close()


if __name__ == "__main__":
    cli = ParseCli()
    config = ParseConfig(cli.config)
    config["log-color"] = cli.log_color
    config["type"] = cli.type 
    config["verbose"] = cli.verbose

    logger = GetLogger(config)
    if cli.type == "auth" or cli.type == "sasl":
        run_auth(config, logger)

    if not cli.type or cli.type == "provider":
        run_provider(config, logger)
