# This file is placed in the Public Domain.


"fleet"


from objd.iface import Handler, named
from objd.run   import broker


def flt(event):
    "list of bots."
    bots = []
    for obj in broker.all():
        if not isinstance(obj, Handler):
            continue
        bots.append(obj)
    try:
        event.reply(bots[int(event.args[0])])
    except (IndexError, ValueError):
        event.reply(",".join([named(x).split(".")[-1] for x in bots]))
