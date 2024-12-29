from arcade import SpriteList, BasicSprite, ArcadeContext, Vec2, Vec3, Texture
from arcade.types import Box, LRBTNF

from critter.lib.pool import Pool

from critter.lib.utils import get_window

from resources import load_png


class Tile:

    def __init__(self, texture: Texture, transparent: bool, position: tuple):
        self.texture = texture
        self.transparent: bool = transparent
        self.position: tuple[float, float, float] = position

        self.current_sprite: BasicSprite = None

    def set_sprite(self, sprite: BasicSprite):
        if self.current_sprite is not None:
            self.free_sprite()
        self.current_sprite = sprite

        sprite.visible = True
        sprite.position = self.position[0], self.position[1]
        sprite.depth = self.position[1]
        sprite.texture = self.texture

    def free_sprite(self):
        self.current_sprite.visible = False
        self.current_sprite.position = (0, 0)
        self.current_sprite.depth = 0

class Interactable:

    def __init__(self):
        # ???
        pass

class Room:
    
    def __init__(self):
        self.name: str = ""
        self.tiles: list[Tile] = []
        self.size = len(self.tiles)
        self.transparent_count = len((t for t in self.tiles if t.transparent))
        self.interactable: set[Interactable] = set()
        self.bounds: Box = LRBTNF(0, 1, 0, 1, 0, 1)

class World:
    
    def __init__(self, ctx: ArcadeContext = None):
        self.ctx = ctx or get_window().ctx

        default_texture = load_png('tile_1')

        self.tiles: Pool[BasicSprite] = Pool([BasicSprite(default_texture, 1.0, visible = False) for _ in range(1024)])
        self.tile_sprites = SpriteList(capacity=1024)
        self.tile_sprites.extend(self.tiles.source)

        self.transparent: Pool[BasicSprite] = Pool([BasicSprite(default_texture, 1.0, visible=False) for _ in range(128)])
        self.transparent_sprites = SpriteList(capacity=128)
        self.transparent_sprites.extend(self.transparent.source)

        self.interactables: set = set()
        self.rooms: dict[str, Room] = {}
        self.loaded_rooms: set[str] = set()
        self.current_room: Room | None

    def load_room(self, name: str):
        if name not in self.rooms:
            print(f'{name} does not exsist')

        if name in self.loaded_rooms:
            print(f'{name} already loaded')
            return
                
        room = self.rooms[name]

        if self.tiles.remaining < room.size or self.transparent.remaining < room.transparent_count:
            print(f'{name} cannot be loaded due to lack of sprites')
            return

        for tile in room.tiles:
            if tile.transparent:
                sprite = self.transparent.get()
            else:
                sprite = self.tiles.get()
            
            tile.set_sprite(sprite)

        if room.transparent_count:
            self.transparent_sprites.sort(key=lambda t: t.x + t.y)

        self.interactables.update(room.interactable)

        self.loaded_rooms.add(name)

    def unload_room(self, name: str):
        if name not in self.rooms:
            print(f'{name} does not exsist')
        
        if name not in self.loaded_rooms():
            print(f'{name} is not loaded')

        room = self.rooms[name]

        self.interactables.difference_update(room.interactable)
        for tile in room.tiles:
            if tile.transparent:
                self.transparent.give(tile.current_sprite)
            else:
                self.tiles.give(tile.current_sprite)
            tile.free_sprite()

        self.loaded_rooms.remove(name)

    def enter_room(self, name: str):
        pass # TODO: load rooms around and below the current room

    def location(self, position: Vec3) -> str:
        if self.current_room is not None and self.current_room.bounds.point_in_box(position):
            return self.current_room.name
        
        for room in self.rooms.values():
            if room.bounds.point_in_box(position):
                return room.name

    def update(self):
        pass
 
    def draw(self):
        with self.ctx.enabled(self.ctx.DEPTH_TEST):
            self.tile_sprites.draw(pixelated=True)
            self.transparent_sprites.draw(pixelated=True) # TODO: sort transparent sprites