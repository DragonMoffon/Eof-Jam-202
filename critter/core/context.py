from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from critter.core.application import Window

class GameContext:
    
    def __init__(self):
        self.window: Window = None
        self.player:
        self.map:
        self.rooms: 
        