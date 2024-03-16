# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"fleet"


from objr.handler import Client
from objr.runtime import Broker
from objr.threads import name


def flt(event):
    try:
        event.reply(Broker.all()[int(event.args[0])])
    except (IndexError, ValueError):
        event.reply(",".join([name(x).split(".")[-1] for x in Broker.all()]))


Client.add(flt)
