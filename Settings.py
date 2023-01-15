import pygame

pygame.font.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 800
backgroundColor = (100, 0, 0)

screen = pygame.display.set_mode(SCREEN_SIZE)

standardFont = pygame.font.SysFont("Timesnewroman", 18)
bigFont = pygame.font.SysFont("Timesnewroman", 60)

tile_width, tile_height = 10, 10

gravity = 6
