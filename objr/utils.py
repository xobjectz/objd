# This file is placed in the Public Domain.


"utilities"


import time
import uuid
import _thread


def fntime(daystr):
    "convert file name to it's saved time."
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return timed


def forever():
    while True:
        try:
            time.sleep(1.0)
        except Exception as ex:
            _thread.interrupt_main()


def shortid():
    "create short id."
    return str(uuid.uuid4())[:8]


def skip(name, skipp):
    "check for skipping"
    for skp in spl(skipp):
        if skp in name:
            return True
    return False


def spl(txt):
    "split comma separated string into a list."
    try:
        res = txt.split(',')
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]


def __dir__():
    return (
        'fntime',
        'forever',
        'shortid',
        'skip',
        'spl'
    )
