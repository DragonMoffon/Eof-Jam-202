from typing import Any

from arcade import SpriteList, BasicSprite, ArcadeContext, Vec2, Vec3, Texture
from arcade.types import Box, LRBTNF

from critter.lib.pool import Pool
from critter.lib.loading import Task
from critter.lib.utils import get_window

from resources import load_png, load_program
from resources.LDtk import LDtkRoot, TilesetDefintion, Level

from .context import context
from .tile import Tiles


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
        sprite.depth = self.position[2]
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
    
    def __init__(self, name: str, tiles: tuple[Tile, ...] = (), interactables: tuple[Interactable, ...] = (), bounds: Box = None):
        self.name: str = name
        self.tiles: tuple[Tile, ...] = tiles
        self.size = len(self.tiles)
        self.transparent_count = len([t for t in self.tiles if t.transparent])
        self.interactable: set[Interactable] = set(interactables)

        # TODO: EW
        if bounds is None:
            min_x = 1000000
            max_x = -1000000
            min_y = 1000000
            max_y = -1000000
            min_z = 1000000
            max_z = -1000000

            for tile in tiles:
                x, y, z = tile.position
                min_x = min(x - 0.5, min_x)
                max_x = max(x + 0.5, max_x)
                min_y = min(y - 0.5, min_y)
                max_y = max(y + 0.5, max_y)
                min_z = min(z - 0.5, min_z)
                max_z = max(z + 0.5, max_z)
            
            bounds = LRBTNF(min_x, max_x, min_y, max_y, min_z, max_z)

        self.bounds: Box = bounds

class World:
    
    def __init__(self, ctx: ArcadeContext = None):
        self.ctx = ctx or get_window().ctx
        self.raw_data: LDtkRoot = None

        default_texture = Tiles.ground

        program = load_program(
            self.ctx,
            vertex_shader='isometric_sprite_vs',
            geometry_shader='isometric_sprite_gs',
            fragment_shader='isometric_sprite_fs'
        )
        program['uv_texture'] = 1
        program['scale'] = 32, 16, 35

        self.tiles: Pool[BasicSprite] = Pool([BasicSprite(default_texture, 1.0, visible=False) for _ in range(8192)])
        self.tile_sprites = SpriteList(capacity=1024)
        self.tile_sprites.extend(self.tiles.source)

        self.transparent: Pool[BasicSprite] = Pool([BasicSprite(default_texture, 1.0, visible=False) for _ in range(1024)])
        self.transparent_sprites = SpriteList(capacity=128)
        self.transparent_sprites.extend(self.transparent.source)

        self.tile_sprites.program = self.transparent_sprites.program = program

        self.interactables: set = set()
        self.rooms: dict[str, Room] = {}
        self.loaded_rooms: set[str] = set()
        self.current_room: Room | None

        self.tile_textures: dict[int, tuple[Texture, bool]] = {}
        self.tile_names: dict[int, str] = {}

    def load_world(self):
        for room in self.loaded_rooms:
            self.unload_room(room)
        self.current_room = None
        self.rooms = {}
        self.tile_textures = {}
        self.tile_names = {}

        self.raw_data = context.active.world_data

        for tileset in self.raw_data.defs.tilesets:
            self.add_tileset(tileset)

        for level in self.raw_data.levels:
            self.add_room(level)


    def add_tileset(self, definition: TilesetDefintion):
        for tile in definition.custom_data:
            tile_name, *other = tile.data.split('\n')
            tile_transparent = 'transparent' in other
            try:
                tile_texture = Tiles(tile_name)
            except KeyError:
                continue
            self.tile_textures[tile.tile_id] = tile_texture, tile_transparent
            self.tile_names[tile.tile_id] = tile_name 

    def add_room(self, data: Level):
        print(data.identifier)
        wx, wy, wz = data.world_x / 4, data.world_y / 4, data.world_depth * 5
        layers = {layer.identifier: layer for layer in data.layer_instances}

        self.rooms[data.identifier] = None
        heights = layers['HeightOffset'].int_grid_csv
        terrain_tiles = layers['Terrain'].grid_tiles

        r_width = layers['Terrain'].c_width
        r_height = layers['Terrain'].c_height

        tiles = []
        for terrain in terrain_tiles:
            tx = int(terrain.pos_x / 4)
            ty = int(terrain.pos_y / 4)

            idx = ty * r_width + tx
            height = heights[idx]

            t_name = self.tile_names[terrain.tile_id]

            tile_texture, tile_transparent = self.tile_textures[terrain.tile_id]
            
            # -- Column --
            
            # Check surrounding heights or at the edge of room to choose whether to generate a column
            at_edge = 0 == tx or tx == r_width-1 or ty == 0 or ty == r_height-1
            at_ledge = False if at_edge else (min(heights[idx + 1], heights[idx - 1], heights[idx + r_width], heights[idx - r_width]) < height)
            is_valid = t_name != 'bridge'
            if (at_edge or at_ledge) and is_valid:
                column_texture, column_transparent = Tiles.block, False
                column_start, column_end = 0, height
                if t_name == 'water':
                    column_texture, column_transparent = Tiles.water_column, True
                    tile_texture = Tiles.water_fall
                    column_start = 1
                for h in range(column_start, column_end):
                    tiles.append(Tile(column_texture, column_transparent, (wx + tx, wy + ty, wz + h)))

            # Top Layer
            tiles.append(Tile(tile_texture, tile_transparent, (wx + tx, wy + ty, wz + height)))

        print(len(tiles))

        self.rooms[data.identifier] = Room(data.identifier, tuple(tiles))

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
            self.transparent_sprites.sort(key=lambda t: 1.1*t.depth - (t.center_x + t.center_y))

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