from arcade import Camera2D
from resources import load_png

from critter.core.application import View
from critter.core.world import World, Room, Tile


class GameView(View):

    def __init__(self):
        super().__init__()
        self.world: World = World(self.window.ctx) # TODO: take from context

        texture_floor = load_png('tile_1')
        texture_slope_1 = load_png('tile_2')
        texture_slope_2 = load_png('tile_3')
        texture_block = load_png('tile_4')
        tiles = []
        for x in range(10, -11, -1):
            for y in range(10, -11, -1):
                if (x == -10 and y > 5) or y == 6:
                    tiles.append(Tile(texture_block, False, (x, y, 0)))
                    tiles.append(Tile(texture_floor, False, (x, y, 1)))
                elif y > 5:
                    tiles.append(Tile(texture_floor, False, (x, y, 1)))
                elif y == 5:
                    tiles.append(Tile(texture_slope_1, False, (x, y, 0)))
                elif y == 4:
                    tiles.append(Tile(texture_slope_2, False, (x, y, 0)))
                else:
                    tiles.append(Tile(texture_floor, False, (x, y, 0)))
                

        room = Room(
            'base',
            tiles
        )

        self.world.add_room(room)
        self.world.load_room('base')

        self.camera = Camera2D(position=(0.0, 0.0))
        self.camera.projection_near = -1000.0
        self.camera.projection_far = 1000.0

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            self.world.draw()

    def on_update(self, delta_time):
        self.world.update()