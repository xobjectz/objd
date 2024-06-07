# This file is placed in the Public Domain.


"deferred exception handling."


import io
import traceback


class Errors: # pylint: disable=R0903

    "Errors"

    errors = []
    out    = None


def errors():
    "show exceptions"
    for exc in Errors.errors:
        out(exc)


def formatexc(exc):
    "format an exception"
    res = ""
    stream = io.StringIO(
                         traceback.print_exception(
                                                   type(exc),
                                                   exc,
                                                   exc.__traceback__
                                                  )
                        )
    for line in stream.readlines():
        res += line + "\n"
    return res


def later(exc):
    "add an exception"
    excp = exc.with_traceback(exc.__traceback__)
    Errors.errors.append(excp)


def out(exc):
    "check if output function is set."
    if Errors.out:
        Errors.out(formatexc(exc)) # pylint: disable=E1102


def setout(func):
    "set output function."
    Errors.out = func


def __dir__():
    return (
        'Errors',
        'errors',
        'later',
        'setout'
    )
