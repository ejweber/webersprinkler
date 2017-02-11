# webersprinkler

webersprinkler is an amateur attempt to build an irrigation controller out of a Raspberry Pi 3 and a Sainsmart 8 channel relay. It is programmed entirely in Python (3.4.2) using only the Python standard library installed by default with Raspbian.

In this version, control over the relay is relegated to a daemon server running in the background of the Raspberry Pi. This allows for the creation of multiple interfaces. Each interface can communicate with the server and request that programs be run, but ultimately a single script has control over the relay.

textclient is the only interface built thus far. It uses a command line interface to modifiy saved sprinkler programs and communicate with the server. It can be run locally on the Raspberry Pi, but is intended to be used by other computers on the local area network.
