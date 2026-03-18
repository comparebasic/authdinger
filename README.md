# PolyVinyl

Two services, one for a authentication and one for a web services management framework.

## Auth 

This service is starts with a UNIX socket server using the a protocal that
communicates content length in two bytes, followed by content, to transmit a
series of tokens. The response is communicated in similar tokens.

found in the [auth](polyvinyl/auth) folder of the source folder.

## Provider 

This is a configuration based web services framework powerd by the JSON
configuration found at [example/config.json](example/config.json).

found in the [provider](polyvinyl/provider) folder of the source folder.
