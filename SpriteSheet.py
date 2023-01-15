import pygame
from dataclasses import dataclass

@dataclass
class spritesheet:
    spritesheet: pygame.Surface
    width: float
    height: float
    frames: int               # number of frames per strip
    scale: float = 1
    strips: tuple[int] = (0)  # a tuple of the number of strips in the format (up, down, left, right)
                              # if an index holds a value less than 0, then it is ignored
    generate_list: bool = False

    def __post_init__(self):
        if self.generate_list:
            if self.strips[0] >= 0:
                self.up = self.get_images(self.strips[0])
            if self.strips[1] >= 0:
                self.down = self.get_images(self.strips[1])
            if self.strips[2] >= 0:
                self.left = self.get_images(self.strips[2])
            if self.strips[3] >= 0:
                self.right = self.get_images(self.strips[3])

    def get_image(self, frame, strip=0, color=(0, 0, 0)):
        image = pygame.Surface((self.width, self.height))
        image.blit(self.spritesheet, (0, 0), (self.width * frame, strip * self.height, self.width, self.height))
        image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
        image.set_colorkey(color)
        return image

    def get_images(self, strip=0, color=(0, 0, 0)):
        return [self.get_image(frame, strip, color) for frame in range(self.frames)]

@dataclass
class Tileset():
    tileset: pygame.Surface
    tile_dimensions: tuple[int]

    def __post_init__(self):
        pass

    def get_tile(self, pos: tuple[int], dimensions: tuple[int], tile_type: int, color=(0, 0, 0)):
        tile = pygame.Surface(dimensions)
        tile.blit(self.tileset, (0, 0), (pos, dimensions))
        tile = pygame.transform.scale(tile, self.tile_dimensions)
        tile.set_colorkey(color)

        return (tile, self.tile_dimensions, tile_type)

