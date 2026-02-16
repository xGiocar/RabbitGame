import pygame

from settings import *
from level import *
from tile_types import *

class Player:
    def __init__(self, level: Level):
        self.sprite = pygame.image.load('assets/player_east.png')
        self.level = level
        self.x = level.startX
        self.y = level.startY
        self.in_hole = False
        self.last_direction = 'E'
        self.change_level = False
        self.fruit_count = 0

    def update(self, screen: pygame.Surface):
        match self.last_direction:
            case 'E':
                self.sprite = pygame.image.load('assets/player_east.png')
            case 'V':
                self.sprite = pygame.image.load('assets/player_west.png')
            case 'N':
                self.sprite = pygame.image.load('assets/player_east.png')
            case 'S':
                self.sprite = pygame.image.load('assets/player_west.png')
        new_sprite = pygame.transform.scale_by(self.sprite, SCALE_FACTOR)
        screen.blit(new_sprite, (self.x * 32 * SCALE_FACTOR, self.y * 32 * SCALE_FACTOR))



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
        self.check_for_item(self.x, self.y)
        self.check_for_tile()

    def eat_grass(self) -> bool:
        current_space = int(self.level.matrix[self.y][self.x])
        if current_space in eatable:
            self.level.matrix[self.y][self.x] = self.level.type * 10 + 3
            return True
        return False

    def dig_hole(self):
        current_space = int(self.level.matrix[self.y][self.x])
        if current_space in diggable:
            self.level.matrix[self.y][self.x] = self.level.type * 10 + 4

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
        self.level.matrix[y][x] = self.level.type * 10 + 4
        self.update_hole_list()

    def check_for_item(self, x, y) -> int:
        if x < 0 or x >= self.level.width:
            return
        if y < 0 or y >= self.level.height:
            return

        item_id = int(self.level.obj_matrix[y][x])
        #debug
        font = pygame.font.SysFont("Arial", 36)
        text_surface = font.render(f"Current item: {item_id}", True, (0,0,0))
        self.level.screen.blit(text_surface, (0, 0))

        match item_id:
            case 0:
                return 0
            case 1:
                self.level.obj_matrix[self.y][self.x] = 0
                self.fruit_count += 1
            case 2:
                self.change_level = True

        return item_id


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
