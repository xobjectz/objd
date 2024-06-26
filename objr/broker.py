# This file is placed in the Public Domain.


"broker"


import os
import _thread


from objx        import Object, fqn, ident, keys, search, update
from objr.utils  import fntime


lock = _thread.allocate_lock()


class Broker:

    "Broker"

    fqns = []

    def __init__(self):
        self.objs = Object()

    def add(self, obj):
        "add an object to the broker."
        with lock:
            ids = ident(obj)
            setattr(self.objs, ids, obj)
            name = ids.split(os.sep, maxsplit=1)[0]
            if name not in Broker.fqns:
                Broker.fqns.append(name)
            return ids

    def all(self, name=None, deleted=False):
        "return all objects."
        with lock:
            if name:
                name = self.long(name)
            for key in self.keyz(name):
                obj = getattr(self.objs, key)
                if deleted and '__deleted__' in dir(obj):
                    continue
                yield key, obj

    def find(self, name, selector, index=None, deleted=False):
        "find objects stored in the broker."
        nrss = 0
        with lock:
            for key in self.keyz(self.long(name)):
                obj = getattr(self.objs, key)
                if deleted and '__deleted__' not in dir(obj):
                    continue
                if not search(obj, selector):
                    continue
                nrss += 1
                if index is not None and nrss != int(index):
                    continue
                yield (key, obj)

    def first(self, name):
        "return first object."
        key = sorted(self.keyz(self.long(name)), key=fntime)
        return getattr(self.objs, key)

    def get(self, orig):
        "return object by origin (repr)"
        return getattr(self.objs, orig, None)


    def keyz(self, key):
        "return all matching keys."
        return [x for x in keys(self.objs) if key == x.split(os.sep)[0]]

    def last(self, obj):
        "return last object saved."
        kyz = sorted(self.keyz(fqn(obj)), key=fntime)
        if kyz:
            update(obj, getattr(self.objs, kyz[-1]))

    def long(self, txt):
        "expand to full qualified name."
        for qual in Broker.fqns:
            if txt.lower() == qual.split(".")[-1].lower():
                return qual
        return txt


def __dir__():
    return (
        'Broker',
        'fntime'
    )
