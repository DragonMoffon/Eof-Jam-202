from arcade import Camera2D

from critter.core.application import View
from critter.core.context import context

class GameView(View):

    def __init__(self):
        super().__init__()
        context.active.world.load_room('Entrance')
        context.active.world.load_room('Level_1')
        context.active.world.load_room('Level_2')

        self.camera = Camera2D(position=(0.0, 0.0))
        self.camera.projection_near = -1000.0
        self.camera.projection_far = 1000.0

    def on_mouse_drag(self, x, y, dx, dy, _buttons, _modifiers):
        pos = self.camera.position
        self.camera.position = pos[0] - dx, pos[1] - dy

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            context.active.world.draw()

    def on_update(self, delta_time):
        context.active.world.update()