import pygame
from dataclasses import dataclass
from Settings import *
from Level import *

@dataclass
class Player():
    velocity: list[float]
    frames: list[list[pygame.Surface]]
    name: str
    width: int
    height: int
    starting_pos: tuple[float]
    fly: bool

    def __post_init__(self):
        self.pos = pygame.Rect(self.starting_pos, (self.width, self.height))
        self.direction = 0

        self.label = standardFont.render(self.name, 1, (0, 0, 0))
        self.dead = False
        self.lastFrameSet = self.frames[0]
        self.horizontalMovement = True

    def move(self, shift, frame_counter: int, up=False, down=False, right=False, left=False):
        if self.fly:
            if up:
                self.lastFrameSet = self.frames[0]
                if self.pos.top - self.velocity[1] > 0:
                    self.pos.top -= self.velocity[1]                                                # the top of the screen has a position value of 1,
                                                                                                    # thus the value of our top position should decrease if we want to move up
            if down:
                self.lastFrameSet = self.frames[1]
                if self.pos.bottom + self.velocity[1] < SCREEN_HEIGHT:
                    if type(self.velocity[1]) == float: self.pos.bottom += (self.velocity[1]+1)
                    else: self.pos.bottom += self.velocity[1]                                       # the bottom of the screen has a position value of the SCREEN_HEIGHT,

        if shift >= 0 or shift <= -SCREEN_WIDTH:
            self.horizontalMovement = True
        else:
            self.horizontalMovement = False
                                                                                                    # thus the value of our bottom position should increase if we want to move down
        if left:
            self.lastFrameSet = self.frames[2]
            if self.horizontalMovement and self.pos.left - self.velocity[0] > 0:
                self.pos.left -= self.velocity[0]

        if right:
            self.lastFrameSet = self.frames[3]
            if self.horizontalMovement and self.pos.right + self.velocity[0] < SCREEN_WIDTH:
                if type(self.velocity[0]) == float: self.pos.right += (self.velocity[0]+1)
                else: self.pos.right += self.velocity[0]

        #draw name on top of NPC
        screen.blit(self.label, (self.pos.x+10, self.pos.y-10))
        #self.drawHitBox()

        #showing NPC on screen
        screen.blit(self.lastFrameSet[frame_counter], (self.pos.x, self.pos.y))

    def drawHitBox(self):
        pygame.draw.rect(screen, rect=self.pos, color=(0, 0, 0))

##############################################################################################################################
@dataclass
class Revised():
    velocity: list[int]
    framesUP: list[pygame.Surface]
    framesDOWN: list[pygame.Surface]
    framesLEFT: list[pygame.Surface]
    framesRIGHT: list[pygame.Surface]
    framesIDLE_l: list[pygame.Surface]
    framesIDLE_r: list[pygame.Surface]
    framesJUMP_r: list[pygame.Surface]
    framesJUMP_l: list[pygame.Surface]
    framesFALL_l: list[pygame.Surface]
    framesFALL_r: list[pygame.Surface]
    framesATTACK_l: list[pygame.Surface]
    framesATTACK_r: list[pygame.Surface]
    width: int
    height: int
    offset_x: int = 0
    offset_y: int = 0
    offset_width: int = 0
    offset_height: int = 0
    starting_pos: tuple[int] = (0, 0)
    return_pos: tuple[int] = starting_pos
    fly: bool = False

    def __post_init__(self):
        self.pos = pygame.Rect(self.starting_pos, (self.width, self.height))
        self.hitbox = pygame.Rect((self.pos.x+self.offset_x, self.pos.y+self.offset_y), (self.width+self.offset_width, self.height+self.offset_height))
        self.attack_area = pygame.Rect((self.pos.x+self.offset_x, self.pos.y+self.offset_y), ((self.width+self.offset_width)*2, self.height+self.offset_height))

        self.last_updated = 0
        self.walking_counter = 0
        self.idle_counter = 0
        self.jump_animation_counter = 0
        self.fall_animation_counter = 0
        self.attack_animation_counter = 0

        self.left = False
        self.isIdle = True
        self.jumping = False
        self.falling = False
        self.attacking = False
        self.dead = False
        self.scrolling_x = False
        self.scrolling_y = False

        self.last_y = 0

        self.falling_momentum = 0
        self.jumping_momentum = 0
        self.jump_update_time = 0
        self.jump_count = 0
        self.fell_at_time = 0
        self.count = 0

        self.health = 100
        self.damage = 50
        self.health_bar_green = pygame.Rect((0, 0), (100*self.health*0.01, 10))
        self.health_bar_red = pygame.Rect((self.health_bar_green.x+self.health_bar_green.width, self.health_bar_green.y), (100-self.health_bar_green.width, 10))

    def render_health_bar(self):
        self.health_bar_green.width = 100*self.health*0.01
        self.health_bar_red.width = 100-self.health_bar_green.width
        self.health_bar_red.x = self.health_bar_green.x+self.health_bar_green.width

        pygame.draw.rect(screen, (255, 0, 0), self.health_bar_red)
        pygame.draw.rect(screen, (0, 255, 0), self.health_bar_green)

    def return_to_start(self):
        self.pos.x, self.pos.y = self.starting_pos
        self.update_hitbox()
        self.scrolling_x = False
        self.scrolling_y = False

    def update_hitbox(self):
        if self.left:
            self.hitbox.x = self.pos.x+self.offset_x+11.5
            self.attack_area.x = self.hitbox.x-self.width*1.4
        else:
            self.hitbox.x = self.pos.x+self.offset_x
            self.attack_area.x = self.hitbox.x+self.width*0.70
        self.hitbox.y = self.pos.y+self.offset_y
        self.attack_area.y = self.hitbox.y

    def update_counter(self):
        if pygame.time.get_ticks() - self.last_updated >= 75:
            if not(self.jumping) and not(self.falling) and not(self.isIdle) and not(self.attacking):
                if self.walking_counter+1 > len(self.framesLEFT)-1:
                    self.walking_counter = 0
                else:
                    self.walking_counter += 1
            else:
                if self.jumping:
                    if self.jump_animation_counter+1 > len(self.framesJUMP_l)-1:
                        self.jump_animation_counter = 0
                    else:
                        self.jump_animation_counter += 1
                elif self.isIdle:
                    if self.idle_counter+1 > len(self.framesIDLE_l)-1:
                        self.idle_counter = 0
                    else:
                        self.idle_counter += 1
                elif self.attacking:
                    if self.attack_animation_counter+1 > len(self.framesATTACK_l)-1:
                        self.attack_animation_counter = 0
                        self.attacking = False
                    else:
                        self.attack_animation_counter += 1
                else:
                    if self.fall_animation_counter+1 > len(self.framesFALL_l)-1:
                        self.fall_animation_counter = 0
                    else:
                        self.fall_animation_counter += 1
            self.last_updated = pygame.time.get_ticks()

    def animate_walk(self):
        if self.left:
            screen.blit(self.framesLEFT[self.walking_counter], self.pos)
        else:
            screen.blit(self.framesRIGHT[self.walking_counter], self.pos)
        self.update_counter()

    def animate_jump(self):
        if self.left:
            screen.blit(self.framesJUMP_l[self.jump_animation_counter], self.pos)
        else:
            screen.blit(self.framesJUMP_r[self.jump_animation_counter], self.pos)

        self.update_counter()

    def animate_idle(self):
        if self.left:
            screen.blit(self.framesIDLE_l[self.idle_counter], self.pos)
        else:
            screen.blit(self.framesIDLE_r[self.idle_counter], self.pos)

        self.update_counter()

    def animate_fall(self):
        if self.left:
            screen.blit(self.framesFALL_l[self.fall_animation_counter], self.pos)
        else:
            screen.blit(self.framesFALL_r[self.fall_animation_counter], self.pos)

        self.update_counter()

    def animate_attack(self):
        if self.left:
            screen.blit(self.framesATTACK_l[self.attack_animation_counter], (self.pos))
        else:
            screen.blit(self.framesATTACK_r[self.attack_animation_counter], (self.pos))

        self.update_counter()

    def animate(self):
        if self.isIdle:
            self.animate_idle()
        elif self.jumping:
            self.animate_jump()
        elif self.falling:
            self.animate_fall()
        elif self.attacking:
            self.animate_attack()
        else:
            self.animate_walk()

    def detect_bottom_collision(self, level, movement_x=0, movement_y=0):
        for row in level.hitboxes:
            for hitbox in row:
                self.update_hitbox()
                if (hitbox.left <= self.hitbox.left+movement_x <= hitbox.right or hitbox.left <= self.hitbox.right+movement_x <= hitbox.right):
                    if hitbox.top <= self.hitbox.bottom+movement_y <= hitbox.center[1] or level.moving_tiles[level.hitboxes.index(row)][row.index(hitbox)] and hitbox.top-1 <= self.hitbox.bottom+movement_y <= hitbox.center[1]:
                        # print(hitbox.top <= self.hitbox.bottom <= hitbox.bottom, movement_y)
                        # print("On ground!", self.hitbox.bottom, self.pos.bottom, hitbox.top, hitbox.bottom, [level.hitboxes.index(row), row.index(hitbox)])
                        self.hitbox.bottom = self.pos.bottom = hitbox.top
                        self.update_hitbox()
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
                self.hitbox.bottom = self.pos.bottom = hitbox.top
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

    def move(self, level, right=False, left=False, jump=False, attack=False, enemy_list=[]):
        if self.dead:
            self.die()

        if not(self.scrolling_y):
            self.last_y = self.hitbox.y

        if self.detect_bottom_collision(level) or self.falling and self.detect_bottom_collision(level, movement_y=self.falling_momentum):
            self.fell_at_time = 0
            self.falling_momentum = 0
            self.falling = False
        elif not(self.jumping):
            if self.fell_at_time == 0:
                self.fell_at_time = pygame.time.get_ticks()
            self.falling = True
            self.fall(level)

        if not(self.attacking):
            if left:
                if not(self.scrolling_x) and not(self.detect_left_collision(level)):
                    self.pos.left -= self.velocity[0]
                self.left = True
                self.idle_counter = 0
            elif right:
                if not(self.scrolling_x) and not(self.detect_right_collision(level)):
                    self.pos.right += self.velocity[0]
                self.left = False
                self.idle_counter = 0

            if attack:
                self.attacking = True
                self.walking_counter = 0
                self.idle_counter = 0
                self.jump_animation_counter = 0
                self.fall_animation_counter = 0
                self.attack_animation_counter = 0
            elif jump:
                if self.detect_bottom_collision(level) and not(self.detect_top_collision(level)):
                    self.jumping = True
                    self.walking_counter = 0
                    self.idle_counter = 0
                    self.jump_animation_counter = 0
                    self.fall_animation_counter = 0
        elif self.attack_animation_counter == 2:
            self.update_hitbox()
            for enemy in enemy_list:
                # print(self.attack_connected(enemy))
                self.attack(enemy)
            self.attack_animation_counter = 0
            self.attacking = False

        self.isIdle = not(left or right) and not(self.attacking or self.jumping or self.falling)

        if self.isIdle:
            self.walking_counter = 0
            self.jump_animation_counter = 0
            self.fall_animation_counter = 0

        if self.jumping:
            self.isIdle = False
            if self.jump_update_time == 0:
                self.jump_update_time = pygame.time.get_ticks()
            self.jump(level)

        self.animate()

        self.update_hitbox()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.dead = True

    def die(self):
        self.return_to_start()
        self.dead = False
        self.health = 100

    def attack_connected(self, enemy):
        if enemy.collide_right(self.attack_area) or enemy.collide_left(self.attack_area):
            # print("ATTACKING")
            return True
        return False

    def attack(self, enemy):
        if self.attack_connected(enemy):
            enemy.take_damage(self.damage)
        else:
            return

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
            elif not(self.scrolling_y):
                self.pos.bottom += self.falling_momentum
            self.update_hitbox()

    def jump(self, level):
        self.jumping_momentum = self.velocity[1] - self.jump_count*0.1
        if self.jumping_momentum >= 0 and not(self.detect_top_collision(level, self.jumping_momentum)):
            if not(self.scrolling_y):
                self.pos.bottom -= self.jumping_momentum
            self.jump_count += 1
            self.jump_update_time = pygame.time.get_ticks()
        else:
            self.jumping = False
            self.jump_update_time = 0
            self.jump_count = 0
            if self.detect_top_collision(level, self.jumping_momentum):
                self.fell_at_time = pygame.time.get_ticks()
                self.falling = True
                self.fall(level, boost=1)
            self.jumping_momentum = 0
            self.update_hitbox()

    def draw_hitbox(self):
        pygame.draw.rect(screen, rect=self.attack_area, color=(0, 0, 255), width=1)
        pygame.draw.rect(screen, rect=self.hitbox, color=(0, 255, 0), width=1)

