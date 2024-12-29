from typing import Callable
from threading import Lock, Thread

from time import sleep

class Task:
    
    def __init__(self):
        self._compelete: bool = False
        self._interface_lock: Lock = Lock()

    def begin(self):
        pass

    def finish(self):
        pass

    @property
    def complete(self) -> bool:
        with self._interface_lock:
            return self._compelete

    @property
    def fraction(self) -> float | None:
        with self._interface_lock:
            return None
        
    def task(self):
        pass
        

class SleepTask(Task):
    # A debug task that creates a thread to sleep

    def __init__(self, finish: Callable, duration: float):
        Task.__init__(self)
        self.thread = Thread(target=self.task, daemon=True)
        self.duration = duration
        self.finish = finish
        
    def begin(self):
        if not self.thread.is_alive():
            self.thread.start()
    
    def task(self):
        sleep(self.duration)
        with self._interface_lock:
            self._compelete = True