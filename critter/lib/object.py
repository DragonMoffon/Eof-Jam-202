from __future__ import annotations
from typing import Deque, Any
from array import array
from collections import deque
from arcade import ArcadeContext, get_window

class Attribute[T]:
    
    def __init__(self, target: str):
        self.target = target

    def __get__(self, obj: Object, objtype=None) -> T:
        return obj.source.get(obj.idx, self.target)

    def __set__(self, obj: Object, value: T):
        obj.source.set(obj.idx, self.target, value)

class Object:

    def __init__(self, idx: int, source: ObjectList):
        self.idx: int = idx
        self.source: ObjectList = source


_CAPACITY_DEFAULT = 128
class SyncedArray:

    def __init__(self, dtype, step, size, ctx: ArcadeContext = None):
        self._size = size
        self._dtype = dtype
        self._step = step

        self._cpu_stale = False
        self._gpu_stale = False

        ctx = ctx or get_window().ctx
        self._buffer = ctx.buffer(reserve=4 * self._size * self._step)
        self._array = array(self._dtype, [0] * self._size * self._step)

    def sync(self, force_cpu: bool = False, force_gpu: bool = False):
        if self._gpu_stale or force_cpu:
            self._buffer.write(self._array.tobytes())
            self._gpu_stale = self._cpu_stale = False
        elif self._cpu_stale or force_gpu:
            self._array = array(self._dtype, self._buffer.read())
            self._gpu_stale = self._cpu_stale = False

    def extend(self, size: int, extend: int):
        self._array.extend([0] * extend * self._step)
        self._buffer.orphan(size=size)
        
        self._gpu_stale = True

    def __getitem__(self, idx: int) -> Any:
        return tuple(self._array[idx*self._step + i] for i in range(self._step))

    def __setitem__(self, idx: int, value: Any):
        for i in range(self._step):
            self._array[idx*self._step + i] = value[i]


class ObjectList:

    def __init__(self, targets: tuple[tuple[str, int], ...], capacity: int = _CAPACITY_DEFAULT, lazy: bool = True):
        self._lazy = lazy

        self._capacity = self._slot_capacity = abs(capacity) or _CAPACITY_DEFAULT
        self._freed_slots: Deque[int] = deque()
        self._used_slots: int = 0

        self._targets: dict[str, SyncedArray] = {}
    
    def _next_slot(self) -> int:
        """
        Get the next available slot in the buffers

        Returns:
            slot index
        """
        if self._freed_slots:
            return self._freed_slots.popleft()
        
        slot = self._used_slots
        self._used_slots += 1
        self._grow_buffers()
        return slot
    
    def _grow_buffers(self):
        if self._used_slots <= self._capacity:
            return
        
        extend_by = self._capacity
        self._capacity *= 2


    def new(self) -> int:
        pass

    def rem(self, idx: int) -> None:
        pass

    def get(self, idx: int, target: str) -> Any:
        pass

    def set(self, idx: int, target: str, value: Any):
        pass



class Sprite(Object):
    position = Attribute[tuple[int, int, int]]("position")
