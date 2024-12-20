from __future__ import annotations

class Attribute:
    
    def __init__(self, target: str):
        self.target = target

    def __get__(self, obj: Object, objtype=None):
        return obj.source[self.target][obj.idx]

    def __set__(self, obj: Object, value):
        obj.source[self.target][obj.idx] = value

class Object:

    def __init__(self, idx: int, source: ObjectList):
        self.idx: int = 0
        self.source: ObjectList = None


class ObjectList:

    def __init__(self, capacity: int = 1024, lazy: bool = True):
        self._slots
    
    def __get_item__(self, key):
        pass

    def new(self) -> int:
        pass