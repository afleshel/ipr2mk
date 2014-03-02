
from inspect import getmro
from itertools import chain

def _getslots(c):
    return chain.from_iterable(getattr(c2, '__slots__', ()) for c2 in getmro(c))

class RecordMetaclass(type):
    def __new__(meta, name, bases, dict):
        if '__slots__' not in dict:
            dict['__slots__'] = ()
        return type.__new__(meta, name, bases, dict)


class _Record(object):
    __metaclass__ = RecordMetaclass
    
    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])
    
    def __repr__(self):
        return self.__class__.__name__ + "(" + str.join(", ", (k+"="+repr(getattr(self,k,None)) for k in _getslots(self.__class__))) + ")"
    
    __str__ = __repr__


def Record(*fields):
    class Record(_Record):
        __slots__ = fields    
    return Record


