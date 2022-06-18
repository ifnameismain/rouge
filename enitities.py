import pygame as pg
from math import sqrt


class Player:
    def __init__(self, x, y, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width, self.height = 16, 16
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.velX = 0
        self.velY = 0
        self.speed = 2
        self.leftPressed = False
        self.rightPressed = False
        self.upPressed = False
        self.downPressed = False
        self.running = False
        self.controls = {'left': pg.K_a, 'right': pg.K_d, 'up': pg.K_w, 'down': pg.K_s, 'sprint': pg.K_LSHIFT}
        self.move_state = {control: False for control in self.controls.values()}

    def draw(self, win):
        pg.draw.rect(win, self.color, self.rect)

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
        if self.running:
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

        self.rect = pg.Rect(self.x, self.y, self.width, self.height)