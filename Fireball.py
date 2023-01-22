import pygame
from dataclasses import dataclass
from Projectile import Projectile

framesRIGHT = {}
for x in range(1, 60):
    framesRIGHT[x-1] = pygame.image.load(f"Effects/FXpack13/Effect3/{x}.png").convert_alpha()

framesLEFT = {}
for key in framesRIGHT.keys():
    framesLEFT[key] = pygame.transform.flip(framesRIGHT[key], True, False)

@dataclass
class Fireball(Projectile):
    offset_x: int = 15
    offset_y: int = 20
    offset_width: int = -40
    offset_height: int = -40
    left: bool = False

    def __post_init__(self):
        self.width, self.height = 64, 64
        self.pos = pygame.Rect(self.starting_pos, (self.width, self.height))
        self.hitbox = pygame.Rect((self.starting_pos[0]+self.offset_x, self.starting_pos[1]+self.offset_y), (self.width+self.offset_width, self.height+self.offset_height))

        self.last_updated = 0
        self.animation_counter = 0
        self.expired = False

        self.speed = 3
        self.damage = 10
        self.max_distance = 500

        self.framesRIGHT = framesRIGHT
        self.framesLEFT = framesLEFT

