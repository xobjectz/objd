# This file is placed in the Public Domain.


"disk"


import os
import pathlib
import _thread


from objx import Default, Object, fqn, ident, read, search, update, write


from .utils  import fntime, strip


lock = _thread.allocate_lock()


class Workdir(Object): # pylint: disable=R0903

    "Workdir"

    workdir = ""


def fetch(obj, pth):
    "read object from disk."
    with lock:
        pth2 = store(pth)
        read(obj, pth2)
        return strip(pth)


def find(mtc, selector=None, index=None, deleted=False):
    "find object matching the selector dict."
    clz = mtc
    nrs = -1
    result = []
    for fnm in sorted(fns(clz), key=fntime):
        obj = Default()
        fetch(obj, fnm)
        if not deleted and '__deleted__' in dir(obj):
            continue
        if selector and not search(obj, selector):
            continue
        nrs += 1
        if index is not None and nrs != int(index):
            continue
        result.append((fnm, obj))
    return result


def fns(mtc=""):
    "show list of files."
    dname = ''
    pth = store(mtc)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            for dname in sorted(dirs):
                if dname.count('-') == 2:
                    ddd = os.path.join(rootdir, dname)
                    fls = sorted(os.listdir(ddd))
                    for fll in fls:
                        yield strip(os.path.join(ddd, fll))


def last(obj, selector=None):
    "return last object saved."
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    res = None
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        res = inp[0]
    return res


def lsstore():
    "return types stored."
    return os.listdir(store())


def skel():
    "create directory,"
    pth  = os.path.join(Workdir.workdir, "store", "")
    path = pathlib.Path(pth)
    path.mkdir(parents=True, exist_ok=True)


def store(pth=""):
    "return objects directory."
    return os.path.join(Workdir.workdir, "store", pth)


def sync(obj, pth=None):
    "sync object to disk."
    with lock:
        if pth is None:
            pth = ident(obj)
        pth2 = store(pth)
        write(obj, pth2)
        return pth


def __dir__():
    return (
        'fetch',
        'find',
        'last',
        'lsstore',
        'skel',
        'store',
        'sync'
    )
