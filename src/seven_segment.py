from wrappers import *
import pygame

def SevenSegment():
    def __init__(self, pos: V2i, height: int, width: int, thickness: int):
        self.pos = pos
        self.h = height
        self.w = width
        self.thick = thickness
        self.__create_tiles()
        self.state = None
        """LAYOUT
        #     --     F               
        #    |  |  E   A
        #     --     G
        #    |  |  D   B
        #     ¯¯     C  """#   A  B  C  D  E  F  G
        self.binaryNumbers = [[1, 1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 0, 0, 0], [1, 0, 1, 1, 0, 1, 1], 
                              [1, 1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1], [0, 1, 1, 0, 1, 1, 1], 
                              [0, 1, 1, 1, 1, 0, 1], [1, 1, 0, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1], 
                              [1, 1, 1, 0, 1, 1, 1]]

    def __create_tiles(self):
        pass

    def reset(self):
        pass

    def render(self):
        pass

    def resize(self):
        pass

    def Tile():
        def __init__(self, segment, pos: V2i, width, height):
            self.segment = segment
            self.pos = pos
            self.w = width
            self.h = height
        
        def render(self):
            pass