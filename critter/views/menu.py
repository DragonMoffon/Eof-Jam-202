from critter.core.application import View

from arcade import draw_text

class MenuView(View):

    def __init__(self) -> None:
        super().__init__()

    def on_draw(self) -> None:
        self.clear()
        draw_text('I am here', self.center_x, self.center_y, anchor_x='center', anchor_y='center')

