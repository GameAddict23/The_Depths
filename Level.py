import pygame
from dataclasses import dataclass
from Settings import *

@dataclass
class Level():
    mapped_tiles: list[list[pygame.Surface]]
    name: str
    tile_types: list[tuple[int]]

    def __post_init__(self):
        self.hitboxes: dict[pygame.Rect] = {}
        self.original_hitboxes: dict[pygame.Rect] = {}
        self.moving_tiles: dict[bool] = {}

        for row in range(len(self.mapped_tiles)):
            for tile in self.mapped_tiles[row]:
                if type(tile) == tuple:
                    self.hitboxes[(row, self.mapped_tiles[row].index(tile))] = pygame.Rect((self.mapped_tiles[row].index(tile)*tile[1][0], row*tile[1][1]+self.tile_types[tile[2]][1]), (tile[1][0], tile[1][1]-self.tile_types[tile[2]][1])), self.tile_types[tile[2]][1], tile[0]

        for key in self.hitboxes.keys():
            self.original_hitboxes[key] = pygame.Rect((self.hitboxes[key][0].x, self.hitboxes[key][0].y), (self.hitboxes[key][0].width, self.hitboxes[key][0].height))
            self.moving_tiles[key] = False

    def render(self, offset=(0, 0), draw_hitboxes=False):
        for key in self.hitboxes.keys():
            screen.blit(self.hitboxes[key][2], (self.hitboxes[key][0].x, self.hitboxes[key][0].y-self.hitboxes[key][1]))
            if draw_hitboxes:
                pygame.draw.rect(screen, (255, 0, 0), self.hitboxes[key][0], width=1)

    def update_hitboxes(self, shift_x, shift_y):
        for key in self.hitboxes.keys():
            self.hitboxes[key][0].x = self.original_hitboxes[key].x+shift_x
            self.hitboxes[key][0].y = self.original_hitboxes[key].y+shift_y
