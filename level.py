import pygame

from settings import SCALE_FACTOR
from tile_types import *

class Level:
    def __init__(self, path: str, screen: pygame.Surface):
        self.width = 0
        self.height = 0
        self.startX = 0
        self.startY = 0
        self.matrix = []
        self.obj_matrix = []
        self.holes = []
        self.load_from_file(path)
        self.screen = screen
        self.type = 0
        self.load_from_file(path)



    def load_from_file(self, path: str):
        self.matrix.clear()
        self.obj_matrix.clear()
        self.holes.clear()
        with open(path, 'r') as lvl_file:
            size = lvl_file.readline()
            start = lvl_file.readline()
            grass = lvl_file.readline()
            lvl_type = lvl_file.readline()
            self.startX, self.startY = map(int, start.split())
            self.width, self.height = map(int, size.split())
            self.grass_limit = int(grass)
            self.type = int(lvl_type)
            for i in range(self.height):    #reads the tile map
                line = lvl_file.readline()
                row = list(line.split())
                self.matrix.append(row)

            lvl_file.readline() #reads the empty line between cells and objects

            for i in range(self.height):    #reads the objects
                line = lvl_file.readline()
                row = list(line.split())
                self.obj_matrix.append(row)

    def draw_level(self):
        for i in range(self.height):
            for j in range(self.width):
                texture = int(self.matrix[i][j])
                obj_texture = int(self.obj_matrix[i][j])

                tile = pygame.image.load(f'assets/tiles/{tiles[texture]}').convert_alpha()
                tile = pygame.transform.scale_by(tile, SCALE_FACTOR)
                if obj_texture != 0:
                    item = pygame.image.load(f'assets/objects/{items[obj_texture]}').convert_alpha()
                    item = pygame.transform.scale_by(item, SCALE_FACTOR)

                self.screen.blit(tile, (j * 32 * SCALE_FACTOR, i * 32 * SCALE_FACTOR))
                if obj_texture != 0:
                    self.screen.blit(item, (j * 32 * SCALE_FACTOR, i * 32 * SCALE_FACTOR))

    def draw_text(self, text: str, font: pygame.font.Font, color, x, y):
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))