import pygame

from settings import *
from level import *
from tile_types import *

class Player:
    def __init__(self, level: Level):
        self.sprite = pygame.image.load('assets/player_sprite.png')
        self.level = level
        self.x = level.startX
        self.y = level.startY
        self.in_hole = False
        self.last_direction = 'E'
        self.change_level = False

    def update(self, screen: pygame.Surface):
        screen.blit(self.sprite, (self.x * 32, self.y * 32))

    def move(self, dx=0, dy=0):
        test_x = self.x + dx
        test_y = self.y + dy

        if test_x < 0 or test_x >= self.level.width:
            return
        if test_y < 0 or test_y >= self.level.height:
            return

        next_space = int(self.level.matrix[test_y][test_x])

        if next_space in unpassable:
            return

        self.x = test_x
        self.y = test_y
        self.check_for_item()
        self.check_for_tile()

    def eat_grass(self):
        current_space = int(self.level.matrix[self.y][self.x])
        if current_space in eatable:
            self.level.matrix[self.y][self.x] = 3

    def dig_hole(self):
        current_space = int(self.level.matrix[self.y][self.x])
        if current_space in diggable:
            self.level.matrix[self.y][self.x] = 4

    def update_hole_list(self):
        self.level.holes.clear()
        for i in range(self.y - MAX_DIGGABLE_DIST, self.y + MAX_DIGGABLE_DIST + 1):
            for j in range(self.x - MAX_DIGGABLE_DIST, self.x + MAX_DIGGABLE_DIST + 1):
                if i < 0 or i >= self.level.height or j < 0 or j >= self.level.width:
                    continue
                if int(self.level.matrix[i][j]) in warpable:
                    self.level.holes.append((i, j))

    def enter_hole(self):
        current_space = int(self.level.matrix[self.y][self.x])
        if current_space in hole:
            self.update_hole_list()
            self.in_hole = True

    def exit_hole(self):
        self.in_hole = False

    def teleport_hole(self, x: int, y: int):
        self.x = x
        self.y = y
        self.level.matrix[y][x] = 4
        self.update_hole_list()

    def check_for_item(self):
        item_id = int(self.level.obj_matrix[self.y][self.x])
        #debug
        font = pygame.font.SysFont("Arial", 36)
        text_surface = font.render(f"Current item: {item_id}", True, (0,0,0))
        self.level.screen.blit(text_surface, (0, 0))

        match item_id:
            case 0:
                return
            case 1:
                self.level.obj_matrix[self.y][self.x] = 0
                self.x = self.x + 3
            case 2:
                self.change_level = True

    def check_for_tile(self):
        tile_id = int(self.level.matrix[self.y][self.x])
        if tile_id in slippery:
            match self.last_direction:
                case 'N':
                    self.move(dy=-1)
                case 'S':
                    self.move(dy=1)
                case 'V':
                    self.move(dx=-1)
                case 'E':
                    self.move(dx=1)
