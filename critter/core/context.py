from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .application import Window, View
    from .world import World

class Persistent:
    # Data which saves between launches
    pass

class Active:
    # Data which is specific to this launch
    
    def __init__(self):
        self.world: World = None

class Context:
    WINDOW_TITLE: str = "Little Dungeon"
    WINDOW_WIDTH: int = 1280 
    WINDOW_HEIGHT: int = 720

    # throbber constants
    THROBBER_SIZE: int = 48
    THROBBER_SPEED: int = 80 # ms / frame
    THROBBER_FADE: float = 200 # ms
    
    def __init__(self):
        self.persistent: Persistent = None
        self.win: Window = None
        self.active: Active = None

    def load(self):
        self.persistent = Persistent()

    def refresh(self):
        pass

context: Context = Context()