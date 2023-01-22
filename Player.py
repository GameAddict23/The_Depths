import pygame
from dataclasses import dataclass
from Settings import *
from Level import *
from Fireball import Fireball

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
    framesHIT_l: list[pygame.Surface]
    framesHIT_r: list[pygame.Surface]
    framesDYING_l: list[pygame.Surface]
    framesDYING_r: list[pygame.Surface]
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
        self.last_updated_attack = 0
        self.last_updated_hit = 0
        self.walking_counter = 0
        self.idle_counter = 0
        self.jump_animation_counter = 0
        self.fall_animation_counter = 0
        self.attack_animation_counter = 0
        self.hit_animation_counter = 0
        self.dying_animation_counter = 0

        self.left = False
        self.isIdle = True
        self.jumping = False
        self.falling = False
        self.attacking = False
        self.hit = False
        self.dying = False
        self.dead = False
        self.scrolling_x = False
        self.scrolling_y = False

        self.falling_momentum = 0
        self.jumping_momentum = 0
        self.jump_update_time = 0
        self.jump_count = 0
        self.fell_at_time = 0
        self.count = 0

        self.level = 0
        self.exp = 0
        self.exp_cap = 10
        self.unlocked_fireballs = False
        self.fireballs = {}
        self.fireball_limit = 1
        for i in range(self.fireball_limit):
            self.fireballs[i] = 0
        self.fireball_cooldown = 1000
        self.last_fired = 0
        self.attack_cooldown = 200
        self.last_attacked = 0
        self.max_health = 100
        self.health = self.max_health
        self.damage = 50

        x, y = font_1.size(f"lvl.{self.level}")
        self.exp_bar = pygame.Rect((x+5, y/2), (100, 10))
        self.exp_filled = pygame.Rect((x+5, y/2), ((self.exp/self.exp_cap)*self.exp_bar.width, 10))
        self.health_bar_green = pygame.Rect((5, self.exp_bar.y+self.exp_bar.height+5), (self.health, 10))
        self.health_bar_red = pygame.Rect((self.health_bar_green.x, self.health_bar_green.y), (self.max_health, self.health_bar_green.height))
        self.hub_area = pygame.Surface((300, 100))
        self.hub_area.set_alpha(126)

        self.message_sent = 0

    def render_hud(self):
        screen.blit(self.hub_area, (0, 0))
        pygame.draw.rect(screen, (255, 255, 255), self.hub_area.get_rect(), width=1)

        level = font_1.render(f"lvl.{self.level}", 1, (255, 255, 255))
        x, y = font_1.size(f"lvl.{self.level}")
        self.exp_bar.x, self.exp_bar.y = x+5+5, y/2
        self.exp_filled.x, self.exp_filled.y = self.exp_bar.x, self.exp_bar.y

        screen.blit(level, (5, 0))

        self.exp_filled.width = (self.exp/self.exp_cap)*self.exp_bar.width
        pygame.draw.rect(screen, (100, 100, 100), self.exp_bar)
        pygame.draw.rect(screen, (100, 150, 255), self.exp_filled)
        pygame.draw.rect(screen, (255, 255, 255), self.exp_bar, width=1)

        self.health_bar_green.width = self.health
        pygame.draw.rect(screen, (255, 0, 0), self.health_bar_red)
        pygame.draw.rect(screen, (0, 255, 0), self.health_bar_green)
        pygame.draw.rect(screen, (255, 255, 255), self.health_bar_red, width=1)

        if self.unlocked_fireballs:
            count = 0
            for key in self.fireballs.keys():
                if self.fireballs[key] == 0:
                    pygame.draw.circle(screen, (255, 0, 0), (15+25*count, self.health_bar_red.bottom+15), 10)
                    count += 1

    def send_message(self, message: str, limit: int):
        if self.message_sent == 0:
            return
        elif pygame.time.get_ticks() - self.message_sent <= limit:
            width, height = font_2.size(message)
            message = font_2.render(message, 1, (255, 100, 100))

            screen.blit(message, ((SCREEN_WIDTH-width)/2, 5+height))
            return

        self.message_sent = 0

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
        if pygame.time.get_ticks() - self.last_updated_hit >= 150 and self.hit:
            if self.hit_animation_counter+1 > len(self.framesHIT_l)-1:
                self.hit_animation_counter = 0
                self.hit = False
            else:
                self.hit_animation_counter += 1
            self.last_updated_hit = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.last_updated_attack >= 50 and self.attacking:
            if self.attack_animation_counter+1 > len(self.framesATTACK_l)-1:
                self.attack_animation_counter = 0
                self.attacking = False
            else:
                self.attack_animation_counter += 1
            self.last_updated_attack = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.last_updated >= 60:
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
            elif self.falling:
                if self.fall_animation_counter+1 > len(self.framesFALL_l)-1:
                    self.fall_animation_counter = 0
                else:
                    self.fall_animation_counter += 1
            elif self.dying:
                if self.dying_animation_counter+1 > len(self.framesDYING_l)-1:
                    self.dead = True
                else:
                    self.dying_animation_counter += 1
            else:
                if self.walking_counter+1 > len(self.framesLEFT)-1:
                    self.walking_counter = 0
                else:
                    self.walking_counter += 1

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

    def animate_hit(self):
        if self.left:
            screen.blit(self.framesHIT_l[self.hit_animation_counter], (self.pos))
        else:
            screen.blit(self.framesHIT_r[self.hit_animation_counter], (self.pos))

        self.update_counter()

    def animate_dying(self):
        if self.left:
            screen.blit(self.framesDYING_l[self.dying_animation_counter], (self.pos))
        else:
            screen.blit(self.framesDYING_r[self.dying_animation_counter], (self.pos))

        self.update_counter()

    def animate(self):
        if self.dying:
            self.animate_dying()
        elif self.hit:
            self.animate_hit()
        elif self.isIdle:
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
        for key in level.hitboxes.keys():
            hitbox = level.hitboxes[key][0]
            if (hitbox.left <= self.hitbox.left+movement_x <= hitbox.right or hitbox.left <= self.hitbox.right+movement_x <= hitbox.right):
                if hitbox.top <= self.hitbox.bottom+movement_y <= hitbox.center[1] or level.moving_tiles[key] and hitbox.top-1 <= self.hitbox.bottom+movement_y <= hitbox.center[1]:
                    self.hitbox.bottom = self.pos.bottom = hitbox.top
                    self.update_hitbox()
                    return True
        return False

    def detect_right_collision(self, level):
        for key in level.hitboxes.keys():
            hitbox = level.hitboxes[key][0]
            if self.hitbox.top <= hitbox.top and self.hitbox.bottom > hitbox.top or self.hitbox.bottom >= hitbox.bottom and self.hitbox.top < hitbox.bottom:
                if (hitbox.left <= self.hitbox.right+self.velocity[0] <= hitbox.right):
                    return True
        return False

    def detect_left_collision(self, level):
        for key in level.hitboxes.keys():
            hitbox = level.hitboxes[key][0]
            if self.hitbox.bottom >= hitbox.bottom and self.hitbox.top < hitbox.bottom:
                if (hitbox.left <= self.hitbox.left-self.velocity[0] <= hitbox.right):
                    return True
        return False

    def detect_top_collision(self, level, y_movement=0):
        for key in level.hitboxes.keys():
            hitbox = level.hitboxes[key][0]
            if (hitbox.left <= self.hitbox.left <= hitbox.right or hitbox.left <= self.hitbox.right <= hitbox.right):
                if self.hitbox.bottom >= hitbox.bottom and self.hitbox.top <= hitbox.bottom:
                    return True
        return False

    def on_tile(self, level, row, tile):
        hitbox = level.hitboxes[(row, tile)][0]
        is_moving = level.moving_tiles[(row, tile)]
        self.update_hitbox()
        if (hitbox.left <= self.hitbox.left <= hitbox.right or hitbox.left <= self.hitbox.right <= hitbox.right):
            if hitbox.top <= self.hitbox.bottom <= hitbox.center[1] or is_moving and hitbox.top-1 <= self.hitbox.bottom <= hitbox.center[1]:
                self.hitbox.bottom = self.pos.bottom = hitbox.top
                self.update_hitbox()
                return True
        return False

    def collide_right(self, hitbox, account_for_velocity=True):
        if self.hitbox.top <= hitbox.top and self.hitbox.bottom > hitbox.top or self.hitbox.bottom >= hitbox.bottom and self.hitbox.top < hitbox.bottom:
            if account_for_velocity:
                if (hitbox.left <= self.hitbox.right+self.velocity[0] <= hitbox.right):
                    return True
            else:
                if (hitbox.left <= self.hitbox.right <= hitbox.right):
                    return True
        return False

    def collide_left(self, hitbox, account_for_velocity=True):
        if self.hitbox.bottom >= hitbox.bottom and self.hitbox.top < hitbox.bottom:
            if account_for_velocity:
                if (hitbox.left <= self.hitbox.left-self.velocity[0] <= hitbox.right):
                    return True
            else:
                if (hitbox.left <= self.hitbox.left <= hitbox.right):
                    return True
        return False

    def take_damage(self, amount):
        self.hit = True
        self.last_updated_hit = pygame.time.get_ticks()
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.dying = True

    def die(self):
        self.return_to_start()
        self.dead = False
        self.dying = False
        self.left = False
        self.dying_animation_counter = 0
        self.level = 0
        self.max_health = 100
        self.health = self.max_health
        self.health_bar_red.width = self.max_health
        self.unlocked_fireballs = False

    def attack_connected(self, enemy):
        if enemy.collide_right(self.attack_area, account_for_velocity=False) or enemy.collide_left(self.attack_area, account_for_velocity=False):
            return True
        return False

    def fall(self, level, boost=0):
        if self.falling:
            if self.falling_momentum < 10:
                self.falling_momentum = gravity * (pygame.time.get_ticks()-self.fell_at_time)*(1/500) + boost
            else:
                self.falling_momentum = 10
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

    def check_for_level_up(self):
        if self.exp >= self.exp_cap:
            self.level += 1
            self.exp = 0
            self.exp_cap += 10
            self.max_health = 100+5*self.level
            self.health = self.max_health
            self.health_bar_red.width = self.max_health

            if self.level == 1:
                self.unlocked_fireballs = True
                self.message_sent = pygame.time.get_ticks()
            elif 3 <= self.level <= 4:
                self.fireball_limit += 1
                self.fireballs[self.fireball_limit-1] = 0
                self.fireball_cooldown -= 10

    def main(self, level, shift_x, shift_y, right=False, left=False, jump=False, attack=False, fire=False, enemy_dict={}):
        if self.dead:
            self.die()

        self.check_for_level_up()

        self.send_message("Fireballs unlocked! Press 1 to fire!", 2000)

        if self.detect_bottom_collision(level) or self.falling and self.detect_bottom_collision(level, movement_y=self.falling_momentum):
            self.fell_at_time = 0
            self.falling_momentum = 0
            self.falling = False
        elif not(self.jumping):
            if self.fell_at_time == 0:
                self.fell_at_time = pygame.time.get_ticks()
            self.falling = True
            self.fall(level)

        if not(self.dying or self.hit):
            if not(self.attacking):
                if left:
                    if not(self.scrolling_x or self.detect_left_collision(level)):
                        self.pos.left -= self.velocity[0]
                    self.left = True
                    self.idle_counter = 0
                elif right:
                    if not(self.scrolling_x or self.detect_right_collision(level)):
                        self.pos.right += self.velocity[0]
                    self.left = False
                    self.idle_counter = 0

                if not(self.falling or self.jumping) and pygame.time.get_ticks() - self.last_attacked >= self.attack_cooldown and attack:
                    self.attacking = True
                    self.walking_counter = 0
                    self.idle_counter = 0
                    self.jump_animation_counter = 0
                    self.fall_animation_counter = 0
                    self.attack_animation_counter = 0
                    self.last_attacked = 0
                elif jump:
                    if self.detect_bottom_collision(level) and not(self.detect_top_collision(level)):
                        self.jumping = True
                        self.walking_counter = 0
                        self.idle_counter = 0
                        self.jump_animation_counter = 0
                        self.fall_animation_counter = 0

                if self.unlocked_fireballs and fire and pygame.time.get_ticks() - self.last_fired >= self.fireball_cooldown:
                    if self.left:
                        fireball = Fireball(starting_pos=(self.hitbox.x-self.width-shift_x, self.hitbox.y-10-shift_y), left=self.left)
                    else:
                        fireball = Fireball(starting_pos=(self.hitbox.x-shift_x, self.hitbox.y-10-shift_y), left=self.left)
                    for key in self.fireballs.keys():
                        if self.fireballs[key] == 0:
                            self.fireballs[key] = fireball
                            break
                    self.last_fired = pygame.time.get_ticks()
            elif self.attack_animation_counter+1 > len(self.framesATTACK_l)-1:
                for key in enemy_dict.keys():
                    if enemy_dict[key] != 0 and not(enemy_dict[key].dying) and self.attack_connected(enemy_dict[key]):
                        enemy_dict[key].take_damage(self.damage)
                        if enemy_dict[key].dying:
                            self.exp += enemy_dict[key].exp_reward
                self.attack_animation_counter = 0
                self.attacking = False
                self.last_attacked = pygame.time.get_ticks()

        for fireball in self.fireballs.keys():
            if self.fireballs[fireball] != 0:
                for enemy in enemy_dict.keys():
                    if enemy_dict[enemy] != 0 and not(enemy_dict[enemy].dying):
                        if enemy_dict[enemy].collide_left(self.fireballs[fireball].hitbox, account_for_velocity=False) or enemy_dict[enemy].collide_right(self.fireballs[fireball].hitbox, account_for_velocity=False):
                            enemy_dict[enemy].take_damage(self.fireballs[fireball].damage)
                            if enemy_dict[enemy].dying:
                                self.exp += enemy_dict[key].exp_reward
                            self.fireballs[fireball].expired = True
                if self.fireballs[fireball].expired:
                    self.fireballs[fireball] = 0
                else:
                    self.fireballs[fireball].move(level, shift_x, shift_y)

        self.isIdle = not(left or right or self.attacking or self.jumping or self.falling or self.hit or self.dying)

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
