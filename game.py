import pygame

from level import Level
from player import Player
from sys import exit
from settings import *
from tile_types import blocked_items, level_list


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Joc pentru iub")
        pygame.key.set_repeat(500, 200)

        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = False
        self.fullscreen = False
        self.current_level = 5
        self.canvas = pygame.Surface((GRID_W * 64, GRID_H * 64))
        self.level = Level(level_list[self.current_level], self.canvas)
        self.player = Player(self.level)

        self.color = (0, 0, 0)

    def start(self):
        self.running = True
        hole_select_counter = 0

        while self.running:
            #print(self.level.text)
            item = self.player.change_level
            if self.player.change_level != -1:
                self.player.change_level = -1
                match item:
                    case 16:
                        # self.current_level = 11
                        pass
                    case 20 | 21 | 22 | 23:
                        self.current_level = 5
                    case _:
                        self.current_level += 1
                    
                self.level = Level(level_list[self.current_level], self.canvas)
                hole_select_counter = 0
                self.player = Player(self.level)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode((1920, 1200), pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode((1280, 720))

                    if self.player.in_hole:
                        size = len(self.level.holes)
                        sel_y, sel_x = self.level.holes[hole_select_counter]
                        self.level.obj_matrix[sel_y][sel_x] = 3

                        if event.key == pygame.K_e:
                            self.level.obj_matrix[sel_y][sel_x] = 0
                            self.player.exit_hole()

                        if event.key == pygame.K_q:
                            self.player.teleport_hole(sel_x, sel_y)
                            self.level.obj_matrix[sel_y][sel_x] = 0
                            hole_select_counter = 0 # needs to be recalculated because of the changing surrounding holes
                            size = len(self.level.holes)

                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.level.obj_matrix[sel_y][sel_x] = 0
                            hole_select_counter = (hole_select_counter + 1) % size
                            sel_y, sel_x = self.level.holes[hole_select_counter]
                            self.level.obj_matrix[sel_y][sel_x] = 3

                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.level.obj_matrix[sel_y][sel_x] = 0
                            hole_select_counter = (hole_select_counter - 1) if ((hole_select_counter - 1) > -1) else size - 1
                            sel_y, sel_x = self.level.holes[hole_select_counter]
                            self.level.obj_matrix[sel_y][sel_x] = 3

                    else:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.player.last_direction = 'N'
                            item_id = self.player.check_for_item(self.player.x, self.player.y - 1)
                            if item_id not in blocked_items:
                                self.player.move(dy=-1)
                        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.player.last_direction = 'S'
                            item_id = self.player.check_for_item(self.player.x, self.player.y + 1)
                            if item_id not in blocked_items:
                                self.player.move(dy=1)
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.player.last_direction = 'V'
                            item_id = self.player.check_for_item(self.player.x - 1, self.player.y)
                            if item_id not in blocked_items:
                                self.player.move(dx=-1)
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.player.last_direction = 'E'
                            item_id = self.player.check_for_item(self.player.x + 1, self.player.y)
                            if item_id not in blocked_items:
                                self.player.move(dx=1)
                        if event.key == pygame.K_e:
                            self.player.enter_hole()
                            self.player.dig_hole()
                            if self.level.grass_limit > 0:
                                if self.player.eat_grass():
                                    self.level.grass_limit -= 1
                        if event.key == pygame.K_LSHIFT and self.player.fruit_count > 0:

                            match self.player.last_direction:
                                case 'N':
                                    self.player.move(dy=-2)
                                    self.player.fruit_count -= 1
                                case 'S':
                                    self.player.move(dy=2)
                                    self.player.fruit_count -= 1
                                case 'E':
                                    self.player.move(dx=2)
                                    self.player.fruit_count -= 1
                                case 'V':
                                    self.player.move(dx=-2)
                                    self.player.fruit_count -= 1
                        if event.key == pygame.K_r:
                            self.level.load_from_file(level_list[self.current_level])
                            self.player.x, self.player.y = (self.level.startX, self.level.startY)

            self.canvas.fill(self.color)
            self.level.draw_level()
            self.player.update(screen=self.canvas)

            center_x = (RESOLUTION[0] - self.level.width * 32 * SCALE_FACTOR) // 2
            center_y = (RESOLUTION[1] - self.level.height * 32 * SCALE_FACTOR) // 2
            self.screen.fill(color=(0,0,0))

            self.screen.blit(self.canvas, (center_x, center_y))


            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.start()