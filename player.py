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
        self.slipping = False
        self.last_direction = 'E'
        self.change_level = -1
        self.fruit_count = 0

    def update(self, screen: pygame.Surface):
        if self.in_hole:
            self.sprite = pygame.image.load('assets/player_in_hole.png')
        else:
            match self.last_direction:
                case 'E':
                    self.sprite = pygame.image.load('assets/player_east.png')
                case 'V':
                    self.sprite = pygame.image.load('assets/player_west.png')
                case 'N':
                    self.sprite = pygame.image.load('assets/player_north.png')
                case 'S':
                    self.sprite = pygame.image.load('assets/player_south.png')
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
            return -1
        if y < 0 or y >= self.level.height:
            return -1

        item_id = int(self.level.obj_matrix[y][x])

        match item_id:
            case 0:
                return 0
            case 1 | 19:
                self.level.obj_matrix[self.y][self.x] = 0
                self.fruit_count += 1
            case 2 | 12 | 16 | 20 | 21 | 22 | 23:
                self.change_level = int(item_id)
        # self.change level determines the action the game will do when the player touches an item
        # the Game class checks if the change level is different from -1, if so it changes level depending on the item
            case 24:
                match self.last_direction:
                    case 'N':
                        if self.valid_tile(self.y - 2, self.x):
                            # pushes the object to the next position
                            self.level.obj_matrix[self.y - 2][self.x] = self.level.obj_matrix[self.y - 1][self.x]
                            self.level.obj_matrix[self.y - 1][self.x] = 0
                        else: self.move(dy=+1)
                    case 'S':
                        if self.valid_tile(self.y + 2, self.x):
                            self.level.obj_matrix[self.y + 2][self.x] = self.level.obj_matrix[self.y + 1][self.x]
                            self.level.obj_matrix[self.y + 1][self.x] = 0
                        else: self.move(dy=-1)
                    case 'V':
                        if self.valid_tile(self.y, self.x - 2):
                            self.level.obj_matrix[self.y][self.x - 2] = self.level.obj_matrix[self.y][self.x - 1]
                            self.level.obj_matrix[self.y][self.x - 1] = 0
                        else: self.move(dx=+1)
                    case 'E':
                        if self.valid_tile(self.y, self.x + 2):
                            self.level.obj_matrix[self.y][self.x + 2] = self.level.obj_matrix[self.y][self.x + 1]
                            self.level.obj_matrix[self.y][self.x + 1] = 0
                        else: self.move(dx=-1)
        return item_id

    def valid_tile(self, y: int, x: int) -> bool:
        if y >= self.level.height or y < 0:
            return False
        if x >= self.level.width or x < 0:
            return False
        if int(self.level.obj_matrix[y][x]) != 0:
            return False

        return True


    def check_for_tile(self):
        tile_id = int(self.level.matrix[self.y][self.x])
        if tile_id in slippery:
            self.slipping = True
            match self.last_direction:
                case 'N':
                    if self.valid_tile(self.y - 1, self.x):
                        self.move(dy=-1)
                case 'S':
                    if self.valid_tile(self.y + 1, self.x):
                        self.move(dy=1)
                case 'V':
                    if self.valid_tile(self.y, self.x - 1):
                        self.move(dx=-1)
                case 'E':
                    if self.valid_tile(self.y, self.x + 1):
                        self.move(dx=1)

        else:
            self.slipping = False