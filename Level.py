import pygame
from dataclasses import dataclass
from Settings import *

@dataclass
class Level():
    mapped_tiles: list[list[pygame.Surface]]
    name: str
    tile_types: list[tuple[int]]

    def __post_init__(self):
        self.hitboxes: list[list[pygame.Rect]] = []
        self.has_types = len(self.tile_types)
        for row in range(len(self.mapped_tiles)):
            self.hitboxes.append([])
            for tile in self.mapped_tiles[row]:
                if type(tile) == tuple:
                    self.hitboxes[row].append(pygame.Rect((self.mapped_tiles[row].index(tile)*tile[1][0], row*tile[1][1]+self.tile_types[tile[2]][1]), (tile[1][0], tile[1][1]-self.tile_types[tile[2]][1])))

        self.moving_tiles = [[False for tile in row] for row in self.hitboxes]
        self.original_hitboxes = [[pygame.Rect((tile.x, tile.y), (tile.width, tile.height)) for tile in row] for row in self.hitboxes]
        self.moving_hitboxes = [[self.hitboxes[row][tile] if self.moving_tiles[row][tile] else 0 for tile in range(len(self.hitboxes[row]))] for row in range(len(self.hitboxes))]
        self.shift_xx, self.shift_yy = 0, 0

    def render(self, offset=(0, 0), draw_hitboxes=False):
        row_count, tile_count = 0, 0
        for row in self.mapped_tiles:
            for tile in row:
                if type(tile) == tuple:
                    screen.blit(tile[0], (self.hitboxes[row_count][tile_count].x-self.tile_types[tile[2]][0], self.hitboxes[row_count][tile_count].y-self.tile_types[tile[2]][1]))
                    if draw_hitboxes:
                        pygame.draw.rect(screen, (255, 0, 0), self.hitboxes[row_count][tile_count], width=1)
                    tile_count += 1
            tile_count = 0
            row_count += 1

    def update_hitboxes(self, shift_x, shift_y):
        for row in range(len(self.hitboxes)):
            for tile in range(len(self.hitboxes[row])):
                self.hitboxes[row][tile].x = self.original_hitboxes[row][tile].x+shift_x
                self.hitboxes[row][tile].y = self.original_hitboxes[row][tile].y+shift_y
