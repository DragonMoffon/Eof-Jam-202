from critter.core.application import View

from critter.core.world import World

class GameView(View):

    def __init__(self):
        super().__init__()
        self.world: World = None

    def setup(self):
        self.world = World(self.window.ctx)
    
    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        pass