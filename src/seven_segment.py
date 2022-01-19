from turtle import width
from wrappers import *
import colors
import pygame
import time

class SevenSegment():
    def __init__(self, pos: V2i, width: int, height: int, thickness: int):
        self.pos = pos
        self.height = height
        self.width = width
        self.thickness = thickness
        self.__create_tiles()
        self.state = 0
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
        self.state = 0

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

class SevenSegmentDisplay():
    def __init__(self, pos: V2i, width: int, height: int, thickness: int, segmentCount: int):
        self.segmentCount = segmentCount
        self.segments = [SevenSegment(pos + V2i(width * i, 0), width, height, thickness) for i in range(segmentCount)]
        self.__state = 0

    def render(self, screen):
        for s in self.segments:
            s.render(screen)

    def updateState(self, state):
        self.__state = state
        for idx, s in enumerate(reversed(self.segments)):
            s.state = state % 10
            state = state // 10
    
    def updateStateBy(self, inc):
        self.updateState(self.__state + inc)


class SevenSegmentTime():
    def __init__(self, pos: V2i, width: int, height: int, thickness: int):
        self.minuteSegment = SevenSegmentDisplay(pos, width, height, thickness, 2)
        self.secondSegment = SevenSegmentDisplay(pos + V2i(width * 2 + thickness * 3, 0), width, height, thickness, 2)

        self.pos = pos
        self.width = width
        self.height = height
        self.thickness = thickness

        self.start_time = time.time()

    def render(self, screen):
        t = time.time() - self.start_time
        self.__render_dots(screen, (t * 10) % 10 < 5)
        t = round(t)

        self.secondSegment.updateState(t%60)
        self.minuteSegment.updateState(t // 60)

        self.secondSegment.render(screen)
        self.minuteSegment.render(screen)

        
    
    def __render_dots(self, screen, active):
        c = colors.seven_segment_light if active else colors.seven_segment_dark
        
        pygame.draw.rect(screen, colors.seven_segment_background,
        pygame.Rect(self.pos.x + self.width * 2, self.pos.y, self.thickness * 3, self.height))
        
        dot = pygame.Rect(0, 0, self.thickness, self.thickness)
        dot.x = self.pos.x + self.width * 2 + self.thickness
        dot.y = self.pos.y + self.height // 3 - self.thickness // 2
        pygame.draw.rect(screen, c, dot)

        dot.y = self.pos.y + self.height - self.height // 3 - self.thickness // 2
        pygame.draw.rect(screen, c, dot)

    def reset(self):
        self.start_time = time.time()
