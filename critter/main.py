from .core.application import Window
from .core.context import context, Persistent, Active
from .core.world import World

from .views.root import RootView

from resources import load_level

def main() -> None:
    win = Window()
    context.window = win

    context.persistent = Persistent()
    context.active = Active()

    context.active.world_data = load_level(context.WORLD_NAME)
    context.active.world = World(win.ctx)

    context.active.world.load_world() # TODO: move to when the game starts. Pick save (or create new) etc

    win.show_view(RootView())
    win.run()
