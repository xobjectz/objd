# This file is placed in the Public Domain.


"broker"


import _thread


from objx import Object, fqn, ident, items, keys, search, update
from objx import match as domatch


from .utils import fntime


lock = _thread.allocate_lock()


rpr = object.__repr__


class Broker:

    "Broker"

    fqns = []

    def __init__(self):
        self.objs = Object()

    def add(self, obj, name=None):
        "add an object to the broker."
        with lock:
            setattr(self.objs, ident(obj), obj)
            if name is None:
                name = fqn(obj)
            if name not in Broker.fqns:
                Broker.fqns.append(name)

    def all(self, name=None, deleted=False):
        "return all objects."
        with lock:
            name = self.long(name)
            for key, obj in items(self.objs):
                if name and name not in key:
                    continue
                if deleted and '__deleted__' in dir(obj):
                    continue
                yield key, obj

    def find(self, selector=None, index=None, deleted=False, match=None):
        "find objects stored in the broker."
        with lock:
            if match:
                match = self.long(match)
            if selector is None:
                selector = {}
            nrss = 0
            for key, obj in items(self.objs):
                if deleted and '__deleted__' not in dir(obj):
                    continue
                if match and not domatch(obj, match):
                    continue
                if selector and not search(obj, selector):
                    continue
                nrss += 1
                if index is not None and nrss != int(index):
                    continue
                yield (key, obj)

    def first(self):
        "return first object."
        for key in keys(self.objs):
            return getattr(self.objs, key)

    def get(self, orig):
        "return object by origin (repr)"
        return getattr(self.objs, orig, None)

    def last(self, obj, selector=None):
        "return last object saved."
        if selector is None:
            selector = {}
        result = sorted(self.all(fqn(obj)), key=lambda x: fntime(x[0]))
        res = None
        if result:
            inp = result[-1]
            res = inp[0]
            update(obj, res)
        return res

    def long(self, txt):
        "expand to full qualified name."
        if not txt:
            return txt
        for qual in Broker.fqns:
            if txt.lower() in qual.split(".")[-1].lower():
                return qual
        return txt

    def remove(self, obj):
        "remove object from broker"
        delattr(self.objs, rpr(obj))


def __dir__():
    return (
        'Broker',
    )
