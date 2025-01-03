from __future__ import annotations

from arcade import Texture

from resources import load_png


class TileTexture:

    def __init__(self, target: str, sub: tuple[str, ...] = ()):
        self.target = target
        self.sub = sub
        self.texture: Texture = None

    def get(self):
        if self.texture is None:
            self.texture = load_png(self.target, self.sub)
        return self.texture

    def __set_name__(self, owner, name):
        owner.__targets__[name] = self
    
    def __get__(self, obj, typ) -> Texture:
        return self.get()

    def __set__(self, obj, value: Texture):
        self.texture = value

    def __del__(self):
        self.texture = None


class Tiles:
    __targets__: dict[str, TileTexture] = {}
    def __new__(cls, name: str, *, source: bool = False):
        try:
            tile_texture =  cls.__targets__[name]
        except KeyError:
            raise KeyError(f'There is no texture with name {name} defined')
        if source:
            return tile_texture.target, tile_texture.sub
        return tile_texture.get()

    ground = TileTexture('tile_1')
    bridge = TileTexture('tile_2')
    stair_upper = TileTexture('tile_3')
    stair_lower = TileTexture('tile_4')
    block = TileTexture('tile_5')
    water = TileTexture('tile_6')
    water_fall = TileTexture('tile_7')
    water_column = TileTexture('tile_8')
    default = TileTexture('tile_10')