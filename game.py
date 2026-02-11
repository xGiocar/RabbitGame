import pygame

from level import Level
from player import Player
from sys import exit
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Joc pentru iub")
        pygame.key.set_repeat(500, 200)

        self.screen = pygame.display.set_mode((GRID_W * 32, GRID_H * 32))
        self.clock = pygame.time.Clock()
        self.running = False
        self.fullscreen = False
        self.current_level = 'levels/level1'
        self.level = Level(self.current_level)
        self.canvas = pygame.Surface((GRID_W * 32, GRID_H * 32))
        self.player = Player(self.level.startX, self.level.startY, self.level)

        self.color = (0, 0, 0)

    def start(self):
        self.running = True
        counter = 0

        while self.running:
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
                        sel_y, sel_x = self.level.holes[counter]
                        self.level.matrix[sel_y][sel_x] = 2

                        if event.key == pygame.K_e:
                            self.level.matrix[sel_y][sel_x] = 4
                            self.player.exit_hole()

                        if event.key == pygame.K_q:
                            self.player.teleport_hole(sel_x, sel_y)
                            counter = 0 # needs to be recalculated because of the changing surrounding holes
                            size = len(self.level.holes)

                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.level.matrix[sel_y][sel_x] = 4
                            counter = (counter + 1) % size
                            sel_y, sel_x = self.level.holes[counter]
                            self.level.matrix[sel_y][sel_x] = 2

                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.level.matrix[sel_y][sel_x] = 4
                            counter = (counter - 1) if ((counter - 1) > -1) else size - 1
                            sel_y, sel_x = self.level.holes[counter]
                            self.level.matrix[sel_y][sel_x] = 2

                    else:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.player.move(dy=-1)
                        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.player.move(dy=1)
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.player.move(dx=-1)
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.player.move(dx=1)
                        if event.key == pygame.K_e:
                            self.player.enter_hole()
                            self.player.dig_hole()
                            self.player.eat_grass()
                        if event.key == pygame.K_r:
                            self.level.load_from_file(self.current_level)
                            self.player.x, self.player.y = (self.level.startX, self.level.startY)

            self.canvas.fill(self.color)
            self.level.draw_level(self.canvas)
            self.player.update(screen=self.canvas)

            screen_w, screen_h = self.screen.get_size()
            scale = min(screen_w // GRID_W, screen_h // GRID_H)

            scaled_size = (GRID_W * scale, GRID_H * scale)

            scaled_surface = pygame.transform.scale(self.canvas, scaled_size)

            self.screen.blit(scaled_surface, (0, 0))

            pygame.display.update()
            self.clock.tick(60)
