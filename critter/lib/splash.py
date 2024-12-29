from __future__ import annotations
from typing import NamedTuple
from enum import Enum, auto
from math import cos, pi

class Action(Enum):
    INCREASE = auto()
    DECREASE = auto()
    PULSE = auto()
    NONE = auto()

    @staticmethod
    def func(a: Action, f: float):
        match a:
            case Action.INCREASE:
                return 0.5 - cos(pi * f)*0.5
            case Action.DECREASE:
                return cos(pi * f)*0.5 + 0.5
            case Action.PULSE:
                return 0.5 - cos(2 * pi * f)*0.5
            case _:
                return 1.0

class Splash(NamedTuple):
    icon: str
    duration: float
    pixelated: bool
    scale_action: Action = Action.INCREASE
    alpha_action: Action = Action.DECREASE
    scale_b: float = 0.5
    scale_v: float = 0.5
    alpha_b: float = 0.0
    alpha_v: float = 1.0

    def scale(self, t: float):
        s = Action.func(self.scale_action, t / self.duration)
        return self.scale_b + self.scale_v * s
            
    def alpha(self, t: float):
        a = Action.func(self.alpha_action, t / self.duration)
        return int(255 * (self.alpha_b + self.alpha_v * a))
