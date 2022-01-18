from wrappers import *
import colors
import pygame

class SevenSegment():
    def __init__(self, pos: V2i, width: int, height: int, thickness: int):
        self.pos = pos
        self.height = height
        self.width = width
        self.thickness = thickness
        self.__create_tiles()
        self.state = 3
        """LAYOUT
        #     --     F               
        #    |  |  E   A
        #     --     G
        #    |  |  D   B
        #     ¯¯     C  """#   A  B  C  D  E  F  G
        self.binaryNumbers = [[1, 1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 0, 0, 0], [1, 0, 1, 1, 0, 1, 1], 
                              [1, 1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1], [0, 1, 1, 0, 1, 1, 1], 
                              [0, 1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1], 
                              [1, 1, 1, 0, 1, 1, 1]]

    def __create_tiles(self):
        self.tiles = [] #A -> G        
        self.segment_data = {} #height, width, pos

        tile_width = self.width - self.thickness * 2 - self.width // 6
        self.segment_data["width"] = self.width - self.width // 6

        tile_height = (self.height - self.thickness * 3 - self.height // 12) // 2
        self.segment_data["height"] = tile_height * 2 + self.thickness * 3

        relative_pos = self.pos + \
            V2i(self.width // 12, (self.height - self.segment_data["height"]) // 2)

        #A
        self.tiles.append(self.Tile(self, V2i(self.thickness + tile_width,
                          self.thickness), tile_height, self.thickness, relative_pos))
        #B
        self.tiles.append(self.Tile(self, V2i(self.thickness + tile_width,
                          self.thickness * 2 + tile_height), tile_height, self.thickness, relative_pos))
        #C
        self.tiles.append(self.Tile(self, V2i(self.thickness,
                          self.thickness * 2 + tile_height * 2), self.thickness, tile_width, relative_pos))
        #D
        self.tiles.append(self.Tile(self, V2i(0,
                          self.thickness * 2 + tile_height), tile_height, self.thickness, relative_pos))
        #E
        self.tiles.append(self.Tile(self, V2i(0, self.thickness),
                          tile_height, self.thickness, relative_pos))
        #F
        self.tiles.append(self.Tile(self, V2i(self.thickness,
                          0), self.thickness, tile_width, relative_pos))
        #G
        self.tiles.append(self.Tile(self, V2i(self.thickness,
                          self.thickness + tile_height), self.thickness, tile_width, relative_pos))


    def reset(self):
        pass

    def render(self, screen):
        pygame.draw.rect(screen, colors.seven_segment_background, (self.pos.x, self.pos.y, self.width, self.height))
        for idx, tile in enumerate(self.tiles):
            tile.render(screen, self.binaryNumbers[self.state][idx])


    def resize(self):
        pass

    class Tile():
        def __init__(self, segment, pos: V2i, width, height, relative_pos):
            self.segment = segment
            self.pos = pos + relative_pos
            self.w = height
            self.h = width
        
        def render(self, screen, active):
            c = colors.seven_segment_light if active else colors.seven_segment_dark
            pygame.draw.rect(screen, c, (self.pos.x, self.pos.y, self.w, self.h))