import pygame
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

        self.tiles = {
            1: 'grass_tile.bmp',
            2: 'boulder_tile.bmp',
            3: 'eaten_grass_tile.bmp',
            4: 'burrow_tile.bmp',
            5: 'water_tile.bmp',
            6: 'mud_tile.bmp'
        }

        self.items = {
            0: 'transparent.png',
            1: 'fruit.bmp',
            2: 'win.bmp',
            3: 'marker.png'
        }

    def load_from_file(self, path: str):
        self.matrix.clear()
        self.obj_matrix.clear()
        self.holes.clear()
        with open(path, 'r') as lvl_file:
            size = lvl_file.readline()
            start = lvl_file.readline()
            self.startX, self.startY = map(int, start.split())
            self.width, self.height = map(int, size.split())
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

                tile = pygame.image.load(f'assets/tiles/{self.tiles[texture]}').convert_alpha()
                if obj_texture != 0:
                    item = pygame.image.load(f'assets/objects/{self.items[obj_texture]}').convert_alpha()

                self.screen.blit(tile, (j * 32, i * 32))
                if obj_texture != 0:
                    self.screen.blit(item, (j * 32, i * 32))

    def draw_text(self, text: str, font: pygame.font.Font, color, x, y):
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))