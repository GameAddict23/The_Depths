import pygame
from dataclasses import dataclass
from Settings import *

def func():
    return

@dataclass
class Button:
    icon: pygame.Surface
    icon_hover: pygame.Surface
    width: int
    height: int
    pos: tuple[int]
    action: type(func)

    def __post_init__(self):
        self.rect = pygame.Rect(self.pos, (self.width, self.height))
        self.clicked = False
        self.timer = pygame.time.get_ticks()

    def main(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.left < x < self.rect.right and self.rect.top < y < self.rect.bottom:
            screen.blit(self.icon_hover, self.rect)
            self.clicked = pygame.mouse.get_pressed(num_buttons=3)[0]
        else:
            screen.blit(self.icon, self.rect)

        if pygame.time.get_ticks() - self.timer >= 250 and self.clicked:
            self.action(self)
            self.timer = pygame.time.get_ticks()


