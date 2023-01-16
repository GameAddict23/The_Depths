import pygame
from dataclasses import dataclass
from Settings import *
from SpriteSheet import spritesheet

skeleton_walking_right = spritesheet(spritesheet=pygame.image.load("Mobs/Monsters/Skeleton/Walk.png"), width=150, height=150, frames=4)
skeleton_walking_right = skeleton_walking_right.get_images()
skeleton_walking_left = [pygame.transform.flip(frame, True, False) for frame in skeleton_walking_right]

skeleton_attacking_right = spritesheet(spritesheet=pygame.image.load("Mobs/Monsters/Skeleton/Attack.png"), width=150, height=150, frames=8)
skeleton_attacking_right = skeleton_attacking_right.get_images()
skeleton_attacking_left = [pygame.transform.flip(frame, True, False) for frame in skeleton_attacking_right]

skeleton_hit_right = spritesheet(spritesheet=pygame.image.load("Mobs/Monsters/Skeleton/Take Hit.png"), width=150, height=150, frames=4)
skeleton_hit_right = skeleton_hit_right.get_images()
skeleton_hit_left = [pygame.transform.flip(frame, True, False) for frame in skeleton_hit_right]

skeleton_death_right = spritesheet(spritesheet=pygame.image.load("Mobs/Monsters/Skeleton/Death.png"), width=150, height=150, frames=4)
skeleton_death_right = skeleton_death_right.get_images()
skeleton_death_left = [pygame.transform.flip(frame, True, False) for frame in skeleton_death_right]

@dataclass
class Skeleton():
    width: int = 90
    height: int = 100
    offset_x: int = 40
    offset_y: int = 50
    offset_width: int = -40
    offset_height: int = -50
    starting_pos: tuple[int] = (0, 0)
    return_pos: tuple[int] = starting_pos
    fly: bool = False

    def __post_init__(self):
        self.pos = pygame.Rect(self.starting_pos, (self.width, self.height))
        self.hitbox = pygame.Rect((self.pos.x+self.offset_x, self.pos.y+self.offset_y), (self.width+self.offset_width, self.height+self.offset_height))
        self.attack_area = pygame.Rect((self.pos.x+self.offset_x, self.pos.y+self.offset_y), ((self.width+self.offset_width)*0.75, self.height+self.offset_height))

        self.velocity = [2, 1]
        self.framesLEFT = skeleton_walking_left
        self.framesRIGHT = skeleton_walking_right
        self.framesATTACK_l = skeleton_attacking_left
        self.framesATTACK_r = skeleton_attacking_right
        self.framesHIT_l = skeleton_hit_left
        self.framesHIT_r = skeleton_hit_right
        self.framesDEATH_l = skeleton_death_left
        self.framesDEATH_r = skeleton_death_right
        self.framesIDLE_l = []
        self.framesIDLE_r = []
        self.last_updated = 0
        self.walking_counter = 0
        self.idle_counter = 0
        self.attack_animation_counter = 0
        self.hit_counter = 0
        self.dying_counter = 0

        self.left = True
        self.isIdle = False
        self.falling = False
        self.attacking = False
        self.hit = False
        self.dying = False
        self.dead = False

        self.falling_momentum = 0
        self.fell_at_time = 0
        self.count = 0

        self.shift_x = 0
        self.shift_y = 0

        self.health = 150
        self.damage = 25

    def die(self):
        if self.dead:
            self.pos.x, self.pos.y = self.starting_pos
            self.update_hitbox()
            self.dead = False

    def update_hitbox(self, y=None):
        if self.left:
            self.hitbox.x = self.pos.x+self.offset_x+self.shift_x
            self.attack_area.x = self.hitbox.x-self.width*0.40
        else:
            self.hitbox.x = self.pos.x+self.offset_x+self.shift_x+13
            self.attack_area.x = self.hitbox.x+self.width*0.55
        self.hitbox.y = self.pos.y+self.offset_y+self.shift_y
        self.attack_area.y = self.hitbox.y

    def update_counter(self):
        if pygame.time.get_ticks() - self.last_updated >= 100:
            if not(self.attacking) and not(self.isIdle) and not(self.hit):
                if self.walking_counter+1 > len(self.framesLEFT)-1:
                    self.walking_counter = 0
                else:
                    self.walking_counter += 1
            else:
                if self.attacking:
                    if self.hit or self.attack_animation_counter+1 > len(self.framesATTACK_l)-1:
                        self.attack_animation_counter = 0
                        self.attacking = False
                    else:
                        self.attack_animation_counter += 1
                elif self.dying:
                    if self.dying_counter+1 > len(self.framesDEATH_l)-1:
                        self.dead = True
                    else:
                        self.dying_counter += 1
                elif self.hit:
                    if self.hit_counter+1 > len(self.framesHIT_l)-1:
                        self.hit_counter = 0
                        self.hit = False
                    else:
                        self.hit_counter += 1
                else:
                    if self.idle_counter+1 > len(self.framesIDLE_l)-1:
                        self.idle_counter = 0
                    else:
                        self.idle_counter += 1

            self.last_updated = pygame.time.get_ticks()

    def animate_walk(self):
        if self.left:
            screen.blit(self.framesLEFT[self.walking_counter], (self.hitbox.x-self.width/2, self.hitbox.y-self.height/2))
        else:
            screen.blit(self.framesRIGHT[self.walking_counter], (self.hitbox.x-self.width/2-13, self.hitbox.y-self.height/2))

        self.update_counter()

    def animate_idle(self):
        if self.left:
            screen.blit(self.framesIDLE_l[self.idle_counter], self.pos)
        else:
            screen.blit(self.framesIDLE_r[self.idle_counter], self.pos)

        self.update_counter()

    def animate_attack(self):
        if self.left:
            screen.blit(self.framesATTACK_l[self.attack_animation_counter], (self.hitbox.x-self.width/2, self.hitbox.y-self.height/2))
        else:
            screen.blit(self.framesATTACK_r[self.attack_animation_counter], (self.hitbox.x-self.width/2-13, self.hitbox.y-self.height/2))

        self.update_counter()

    def animate_hit(self):
        if self.left:
            screen.blit(self.framesHIT_l[self.hit_counter], (self.hitbox.x-self.width/2, self.hitbox.y-self.height/2))
        else:
            screen.blit(self.framesHIT_r[self.hit_counter], (self.hitbox.x-self.width/2-13, self.hitbox.y-self.height/2))

        self.update_counter()

    def animate_death(self):
        if self.left:
            screen.blit(self.framesDEATH_l[self.dying_counter], (self.hitbox.x-self.width/2, self.hitbox.y-self.height/2))
        else:
            screen.blit(self.framesDEATH_r[self.dying_counter], (self.hitbox.x-self.width/2-13, self.hitbox.y-self.height/2))

        self.update_counter()

    def animate(self):
        if not(self.dying) and not(self.isIdle) and not(self.attacking) and not(self.hit):
            self.animate_walk()
        elif self.dying:
            self.animate_death()
        elif self.attacking:
            self.animate_attack()
        elif self.hit:
            self.animate_hit()
        else:
            pass

    def detect_bottom_collision(self, level, movement_x=0, movement_y=0):
        for row in level.hitboxes:
            for hitbox in row:
                self.update_hitbox()
                if (hitbox.left <= self.hitbox.left+movement_x <= hitbox.right or hitbox.left <= self.hitbox.right+movement_x <= hitbox.right):
                    if hitbox.top <= self.hitbox.bottom+movement_y <= hitbox.center[1] or level.moving_tiles[level.hitboxes.index(row)][row.index(hitbox)] and hitbox.top-1 <= self.hitbox.bottom+movement_y <= hitbox.center[1]:
                        # print(hitbox.top <= self.hitbox.bottom <= hitbox.bottom, movement_y)
                        # print("On ground!", self.hitbox.bottom, self.pos.bottom, hitbox.top, hitbox.bottom, [level.hitboxes.index(row), row.index(hitbox)])
                        self.hitbox.bottom = hitbox.top
                        self.pos.bottom = level.original_hitboxes[level.hitboxes.index(row)][row.index(hitbox)].top
                        return True
        return False

    def detect_right_collision(self, level):
        for row in level.hitboxes:
            for hitbox in row:
                if self.hitbox.top <= hitbox.top and self.hitbox.bottom > hitbox.top or self.hitbox.bottom >= hitbox.bottom and self.hitbox.top < hitbox.bottom:
                    if (hitbox.left <= self.hitbox.right+self.velocity[0] <= hitbox.right):
                        return True
        return False

    def detect_left_collision(self, level):
        for row in level.hitboxes:
            for hitbox in row:
                if self.hitbox.bottom >= hitbox.bottom and self.hitbox.top < hitbox.bottom:
                    if (hitbox.left <= self.hitbox.left-self.velocity[0] <= hitbox.right):
                        return True
        return False

    def detect_top_collision(self, level, y_movement=0):
        for row in level.hitboxes:
            for hitbox in row:
                if (hitbox.left <= self.hitbox.left <= hitbox.right or hitbox.left <= self.hitbox.right <= hitbox.right):
                    if self.hitbox.bottom >= hitbox.bottom and self.hitbox.top <= hitbox.bottom:
                        return True
        return False

    def on_tile(self, level, row, tile):
        hitbox = level.hitboxes[row][tile]
        is_moving = level.moving_tiles[row][tile]
        self.update_hitbox()
        if (hitbox.left <= self.hitbox.left <= hitbox.right or hitbox.left <= self.hitbox.right <= hitbox.right):
            if hitbox.top <= self.hitbox.bottom <= hitbox.center[1] or is_moving and hitbox.top-1 <= self.hitbox.bottom <= hitbox.center[1]:
                # print(hitbox.top <= self.hitbox.bottom <= hitbox.bottom, movement_y)
                # print("On ground!", self.hitbox.bottom, self.pos.bottom, hitbox.top, hitbox.bottom, [level.hitboxes.index(row), row.index(hitbox)])
                self.pos.bottom = hitbox.top
                self.update_hitbox()
                return True
        return False

    def collide_right(self, hitbox):
        if self.hitbox.top <= hitbox.top and self.hitbox.bottom > hitbox.top or self.hitbox.bottom >= hitbox.bottom and self.hitbox.top < hitbox.bottom:
            if (hitbox.left <= self.hitbox.right+self.velocity[0] <= hitbox.right):
                return True
        return False

    def collide_left(self, hitbox):
        if self.hitbox.bottom >= hitbox.bottom and self.hitbox.top < hitbox.bottom:
            if (hitbox.left <= self.hitbox.left-self.velocity[0] <= hitbox.right):
                return True
        return False

    def move(self, level, shift_x, shift_y, player, right=False, left=False, jump=False):
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.update_hitbox()

        if self.detect_bottom_collision(level) or self.falling and self.detect_bottom_collision(level, movement_y=self.falling_momentum):
            self.fell_at_time = 0
            self.falling_momentum = 0
            self.falling = False
        else:
            if self.fell_at_time == 0:
                self.fell_at_time = pygame.time.get_ticks()
            self.falling = True
            self.fall(level)

        if self.hit:
            self.attacking = False
            self.attack_animation_counter = 0

        if not(self.dying) and not(self.hit):
            if not(self.attacking):
                if self.left and not(self.detect_left_collision(level)):
                    self.pos.left -= self.velocity[0]
                    self.hitbox.left -= self.velocity[0]
                    self.left = True
                    self.idle_counter = 0
                else:
                    self.left = False

                if not(self.left) and not(self.detect_right_collision(level)):
                    self.pos.right += self.velocity[0]
                    self.hitbox.right += self.velocity[0]
                    self.left = False
                    self.idle_counter = 0
                else:
                    self.left = True

                if not(self.falling) and not(player.dying) and self.left and self.collide_left(player.hitbox) or not(self.left) and self.collide_right(player.hitbox):
                    self.attacking = True
            else:
                self.attack(player)

        self.update_hitbox()
        self.animate()

    def take_damage(self, amount):
        print(self.attack_animation_counter)
        self.hit = True
        self.attacking = False
        self.attack_animation_counter = 0
        self.health -= amount
        if self.health <= 0:
            self.dying = True

    def attack_connected(self, player):
        if player.collide_right(self.attack_area) or player.collide_left(self.attack_area):
            return True
        return False

    def attack(self, player):
        if self.attack_animation_counter+1 > len(self.framesATTACK_l)-1:
            if self.attack_connected(player):
                player.take_damage(self.damage)
            self.attack_animation_counter = 0
            self.attacking = False

    def fall(self, level, boost=0):
        if self.falling:
            if self.falling_momentum < 10:
                self.falling_momentum = gravity * (pygame.time.get_ticks()-self.fell_at_time)*(1/500) + boost
            else:
                self.falling_momentum = 10
            # print(f"fall function: {self.falling_momentum}, {self.hitbox.bottom+self.falling_momentum}")
            if self.detect_bottom_collision(level, movement_y=self.falling_momentum):
                self.fell_at_time = 0
                self.fall_animation_counter = 0
                self.falling = False
                self.falling_momentum = 0
            else:
                self.pos.bottom += self.falling_momentum
                self.hitbox.bottom += self.falling_momentum
            self.update_hitbox()

    def draw_hitbox(self):
        pygame.draw.rect(screen, rect=self.hitbox, color=(255, 0, 0), width=1)
        pygame.draw.rect(screen, rect=self.attack_area, color=(100, 100, 0), width=1)
        # pygame.draw.rect(screen, rect=self.pos, color=(255, 0, 0), width=1)

