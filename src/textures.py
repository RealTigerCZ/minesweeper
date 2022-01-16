from typing import Tuple
from wrappers import *
import os, pygame


@dataclass
class Texture:
    """
    - represents one texture -> holds important values
    - no need to store every texture image in each 'Tile' separately
    """

    def __init__(self, name: str, ext: str, size: Tuple[int, int], path: os.path):
        self.name = name
        self.name_with_ext = name + "." + ext
        self.path = os.path.join(path, self.name_with_ext)
        self.size = size
        self.image = None


@dataclass
class Textures:
    """Data class Textures which holds path and 'Texture' objects"""

    def __init__(self, path: str):
        self.path = path

        # textures
        self.bomb_tile      = Texture("bomb_tile",     "png", (15, 15), path)
        self.bomb_tile_red  = Texture("bomb_tile_red", "png", (15, 15), path)
        self.flag_tile      = Texture("flag_tile",     "png", (512, 512), path)
        self.pressed_tile   = Texture("pressed_tile",  "png", (16, 16), path)
        self.covered_tile = Texture("covered_tile",  "png", (512, 512), path)

        # states
        self.loaded = False

    def __load_texture(self, texture: Texture):
        """Internal method of class 'Textures' used to load one Texture"""
        try:
            texture.image = pygame.image.load(texture.path)

        except pygame.error as message:
            print("Cannot load texture:", texture.name_with_ext)
            raise SystemExit(message)

        except FileNotFoundError as message:
            print("Cannot find texture:", texture.name_with_ext)
            raise SystemExit(message, f"Path: {texture.path}")

        if texture.image.get_size() != texture.size:
            raise SystemExit(f"Texture {texture.name_with_ext} cannot be loaded, because it has unexpexted size!\nExpected: {texture.size}, actual: {texture.image.get_size()}\n")

    def load_textures(self):
        """Method to load all Textures"""
        self.__load_texture(self.bomb_tile)
        self.__load_texture(self.bomb_tile_red)
        self.__load_texture(self.flag_tile)
        self.__load_texture(self.pressed_tile)
        self.__load_texture(self.covered_tile)

        self.loaded = True
