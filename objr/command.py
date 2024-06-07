# This file is placed in the Public Domain.


"client"


import inspect


from objx import Object


from .errors  import later
from .parse   import parse


class Command(Object): # pylint: disable=R0903

    "Command"

    cmds = Object()


def add(func):
    "add command."
    setattr(Command.cmds, func.__name__, func)


def command(bot, evt):
    "check for and run a command."
    parse(evt)
    func = getattr(Command.cmds, evt.cmd, None)
    if func:
        try:
            func(evt)
        except Exception as exc: # pylint: disable=W0718
            later(exc)
    bot.show(evt)
    evt.ready()


def scan(mod) -> None:
    "scan module for commands."
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in cmd.__code__.co_varnames:
            add(cmd)


def __dir__():
    return (
        'Command',
        'add',
        'command',
        'scan'
    )
