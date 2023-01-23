import pygame
from dataclasses import dataclass
from Settings import *

@dataclass
class Projectile():
    starting_pos: tuple[int]
    offset_x: int = 0
    offset_y: int = 0
    offset_width: int = 0
    offset_height: int = 0
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

        self.framesLEFT = []
        self.framesRIGHT = []

    def update_hitbox(self, shift_x, shift_y):
        if self.left:
            self.hitbox.x = self.pos.x+self.offset_x+shift_x
        else:
            self.hitbox.x = self.pos.x+self.offset_x+shift_x+13

        self.hitbox.y = self.pos.y+self.offset_y+shift_y

    def update_counter(self):
        if pygame.time.get_ticks() - self.last_updated >= 25:
            if self.animation_counter+1 > len(self.framesLEFT)-1:
                self.animation_counter = 0
            else:
                self.animation_counter += 1
            self.last_updated = pygame.time.get_ticks()

    def animate(self):
        if self.left:
            screen.blit(self.framesLEFT[self.animation_counter], (self.hitbox.x-self.width/2+15, self.hitbox.y-20))
        else:
            screen.blit(self.framesRIGHT[self.animation_counter], (self.hitbox.x-self.width/2+10, self.hitbox.y-20))

        self.update_counter()

    def detect_right_collision(self, level):
        for key in level.hitboxes.keys():
            hitbox = level.hitboxes[key][0]
            if self.hitbox.top <= hitbox.top and self.hitbox.bottom > hitbox.top or self.hitbox.bottom >= hitbox.bottom and self.hitbox.top < hitbox.bottom:
                if (hitbox.left <= self.hitbox.right+self.speed <= hitbox.right):
                    return True
        return False

    def detect_left_collision(self, level):
        for key in level.hitboxes.keys():
            hitbox = level.hitboxes[key][0]
            if self.hitbox.top <= hitbox.top and self.hitbox.bottom > hitbox.top or self.hitbox.bottom >= hitbox.bottom and self.hitbox.top < hitbox.bottom:
                if (hitbox.left <= self.hitbox.left-self.speed <= hitbox.right):
                    return True
        return False

    def draw_hitbox(self):
        pygame.draw.rect(screen, rect=self.hitbox, color=(255, 255, 255), width=1)

    def move(self, level, shift_x, shift_y):
        self.update_hitbox(shift_x, shift_y)

        self.expired = self.detect_left_collision(level) or self.detect_right_collision(level) or abs((self.starting_pos[0]+shift_x)-self.hitbox.x) >= self.max_distance
        if not(self.expired):
            if self.left:
                self.pos.x -= self.speed
                self.hitbox.x -= self.speed
            elif not(self.left):
                self.pos.x += self.speed
                self.hitbox.x += self.speed

        self.animate()
