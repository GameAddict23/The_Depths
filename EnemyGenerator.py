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

        self.enemies = {}
        for i in range(self.limit):
            self.enemies[i] = 0
        self.last_generated = 0

    def generate(self):
        enemy = 0
        match self.enemy_type:
            case "skeleton":
                enemy = Skeleton(starting_pos=self.pos, left=true_or_false())
            case "goblin":
                enemy = Goblin(starting_pos=self.pos, left=true_or_false())
        for key in self.enemies.keys():
            if self.enemies[key] == 0:
                self.enemies[key] = enemy
                break

    def main(self, level, shift_x, shift_y, player):
        if pygame.time.get_ticks() - self.last_generated >= self.rate:
            self.generate()
            self.last_generated = pygame.time.get_ticks()

        for key in self.enemies.keys():
            if self.enemies[key] != 0:
                if self.enemies[key].dead:
                    self.enemies[key] = 0
                else:
                    self.enemies[key].move(level, shift_x, shift_y, player)

