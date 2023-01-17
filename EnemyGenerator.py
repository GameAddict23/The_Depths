import pygame
from random import random
from dataclasses import dataclass
from Settings import *
from Enemies import *

def true_or_false():
    num = 1+int(2*random())

    if num == 1:
        return True
    else:
        return False

@dataclass
class EnemyGenerator():
    enemy_type: str
    pos: tuple[int]
    limit: int = 10
    rate: int = 1000

    def __post_init__(self):
        self.enemy_type = self.enemy_type.lower()

        self.enemies = []
        self.last_generated = 0

    def generate(self):
        if len(self.enemies) < self.limit:
            match self.enemy_type:
                case "skeleton":
                    self.enemies.append(Skeleton(starting_pos=self.pos, left=true_or_false()))
                case "goblin":
                    self.enemies.append(Goblin(starting_pos=self.pos, left=true_or_false()))

    def main(self, level, shift_x, shift_y, player):
        if pygame.time.get_ticks() - self.last_generated >= self.rate:
            self.generate()
            self.last_generated = pygame.time.get_ticks()

        x = 0
        for i in range(len(self.enemies)):
            if self.enemies[i-x].dead:
                self.enemies.pop(i-x)
                x += 1
            self.enemies[i-x].move(level, shift_x, shift_y, player)

