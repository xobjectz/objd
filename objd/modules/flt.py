# This file is placed in the Public Domain.


"fleet"


from objr     import Handler, name
from objr.run import broker


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
        event.reply(",".join([name(x).split(".")[-1] for x in bots]))
