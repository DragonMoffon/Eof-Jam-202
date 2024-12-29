from .core.application import Window
from .core.context import context
from .views.root import RootView

def main() -> None:
    win = Window()
    context.window = win

    win.show_view(RootView())
    win.run()
