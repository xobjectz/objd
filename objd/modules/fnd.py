# This file is placed in the Public Domain.


"locate"


from objx import fmt


from objr.run import broker


def fnd(event):
    "locate objects."
    if not event.args:
        event.reply("fnd <type>")
        return
    otype = event.args[0]
    clz = broker.long(otype)
    nmr = 0
    for _fnm, obj in broker.find(event.gets, match=clz):
        event.reply(f"{nmr} {fmt(obj)}")
        nmr += 1
    if not nmr:
        event.reply("no result")
