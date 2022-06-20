import pygame as pg
from math import sqrt, sin, cos, radians
from pg_funcs import *
from main import FRAME_RATE


class Player:
    def __init__(self, x, y, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width, self.height = 16, 16
        self.color = color
        self.velX = 0
        self.velY = 0
        self.speed = 1
        self.leftPressed = False
        self.rightPressed = False
        self.upPressed = False
        self.downPressed = False
        self.running = False
        self.controls = {'left': pg.K_a, 'right': pg.K_d, 'up': pg.K_w, 'down': pg.K_s, 'sprint': pg.K_LSHIFT}
        self.move_state = {control: False for control in self.controls.values()}
        self.animation = load_animation_sequence('static/animation/player', (0, 0, 0))
        self.animation_timer, self.animation_index = 0, 0
        self.player_angle = 0

    def draw(self, win):
        if any((move for key, move in self.move_state.items() if key in
                (v for k, v in self.controls.items() if k in ['left', 'right', 'up', 'down']))):
            self.animation_timer += 1
            if self.move_state[self.controls['sprint']]:
                self.animation_timer += 1
            if self.animation_timer >= FRAME_RATE//6:
                self.animation_index += 1
                if self.animation_index == len(self.animation):
                    self.animation_index = 0
                self.animation_timer = 0
        else:
            self.animation_timer, self.animation_index = 0, 0

        win.blit(rotate_image(self.animation[self.animation_index], self.player_angle),
                             (self.x - self.width//2, self.y - self.height//2))



    def handle_key_press(self, key, down):
        self.move_state[key] = down

    def update(self):
        self.velX = 0
        self.velY = 0

        # Button presses
        if self.move_state[self.controls['left']]:
            self.velX -= self.speed
        if self.move_state[self.controls['right']]:
            self.velX += self.speed
        if self.move_state[self.controls['up']]:
            self.velY -= self.speed
        if self.move_state[self.controls['down']]:
            self.velY += self.speed

        # Character is running (LSHIFT) is pressed
        if self.move_state[self.controls['sprint']]:
            self.velX *= 2
            self.velY *= 2

        # Character is running diagonally (to keep same speed in all directions)
        if self.velX != 0 and self.velY != 0:
            self.velX /= sqrt(2)
            self.velY /= sqrt(2)

        # Borders of screen cancel character move
        screen_width, screen_height = pg.display.get_window_size()
        if self.x + self.velX < 0:
            self.velX = -self.x
        if self.x + self.velX + self.width > screen_width:
            self.velX = screen_width - self.width - self.x
        if self.y + self.velY < 0:
            self.velY = -self.y
        if self.y + self.velY + self.height > screen_height:
            self.velY = screen_height - self.height - self.y

        # Move x, y values by velocities
        self.x += self.velX
        self.y += self.velY

        # set player angle
        if self.velX == 0:
            if self.velY > 0:
                self.player_angle = 180
            elif self.velY < 0:
                self.player_angle = 0
        elif self.velY == 0:
            if self.velX > 0:
                self.player_angle = 270
            elif self.velX < 0:
                self.player_angle = 90
        else:
            if self.velX > 0 and self.velY > 0:
                self.player_angle = 225
            elif self.velX > 0 > self.velY:
                self.player_angle = 315
            elif self.velX < 0 < self.velY:
                self.player_angle = 135
            elif self.velX < 0 and self.velY < 0:
                self.player_angle = 45


class Enemy:
    def __init__(self, x, y, color=(100, 250, 100), fov_angle=90, fov_range=25, aud_range=15, att_range=2):
        self.x = x
        self.y = y
        self.width, self.height = 16, 16
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.velX = 0
        self.velY = 0
        self.speed = 0.5
        self.running = False
        self.sleeping = False
        self.sleep_timer = 0
        self.enemy_angle = 270
        self.rot_angle = 45
        self.fov_angle = fov_angle
        self.fov_range = fov_range
        self.aud_range = aud_range
        self.att_range = att_range
        self.animation = load_animation_sequence('static/animation/enemy', (0, 0, 0))
        self.animation_timer, self.animation_index = 0, 0
        self.hit_box = 0

    def draw(self, win):

        # Draws enemies FOV
        x1 = self.x
        y1 = self.y
        x2 = x1 - sin(radians(self.enemy_angle + (self.fov_angle / 2))) * self.fov_range
        y2 = y1 - cos(radians(self.enemy_angle + (self.fov_angle / 2))) * self.fov_range
        x3 = x1 - sin(radians(self.enemy_angle - (self.fov_angle / 2))) * self.fov_range
        y3 = y1 - cos(radians(self.enemy_angle - (self.fov_angle / 2))) * self.fov_range
        fov_points = [(x1, y1), (x2, y2), (x3, y3)]
        pg.draw.polygon(win, (200, 200, 200), fov_points)

        if not self.sleeping:
            self.animation_timer += 1
            if self.running:
                self.animation_timer += 3
            if self.animation_timer >= FRAME_RATE // 6:
                self.animation_index += 1
                if self.animation_index == len(self.animation):
                    self.animation_index = 0
                self.animation_timer = 0
        else:
            self.animation_timer, self.animation_index = 0, 0

        win.blit(rotate_image(self.animation[self.animation_index], self.enemy_angle),
                 (self.x - self.width // 2, self.y - self.height // 2))

    def update(self):
        pass

    def boundary_check(self):
        pass


