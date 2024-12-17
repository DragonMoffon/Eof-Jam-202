from .core.application import Window
from .views.root import RootView

def main() -> None:
    win = Window()
    root = RootView()

    win.show_view(root)
    win.run()
