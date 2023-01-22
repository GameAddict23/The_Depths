import pygame

pygame.font.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 800
# backgroundColor = (100, 0, 0)

screen = pygame.display.set_mode(SCREEN_SIZE)
game_screen = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))

font_1 = pygame.font.SysFont("Timesnewroman", 30)
font_2 = pygame.font.SysFont("Timesnewroman", 25)
# bigFont = pygame.font.SysFont("Timesnewroman", 60)

tile_width, tile_height = 10, 10

gravity = 6
