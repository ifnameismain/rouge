import pygame as pg
import sys
from math import sin, cos, radians, pi
from random import randint

SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
FPS = 60

pg.init()
clock = pg.time.Clock()

win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class EnTest:
    def __init__(self, width, x_pos, y_pos, mov_speed, rot_speed, fov_dir, fov_angle, fov_range, aud_range, att_range):
        self.width = width
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.mov_speed = mov_speed
        self.rot_speed = rot_speed
        self.fov_dir = fov_dir
        self.fov_angle = fov_angle
        self.fov_range = fov_range
        self.aud_range = aud_range
        self.att_range = att_range
        self.awake = True
        self.left_right = randint(0, 1)
        self.sleep_counter = 0

    def update(self):
        if not randint(0, 999):
            self.awake = False
        if self.awake:

            x_amount = self.mov_speed*sin(radians(self.fov_dir+90))
            y_amount = self.mov_speed*cos(radians(self.fov_dir+90))
            self.left_right = randint(0, 1)
            if self.x_pos - self.width < abs(x_amount):
                self.x_pos -= x_amount - (self.x_pos - self.width) + 0.01
                self.turn(10)
            elif self.x_pos + self.width + x_amount > SCREEN_WIDTH:
                self.x_pos += (SCREEN_WIDTH - (self.x_pos + self.width)) - 0.01
                self.turn(10)
            else:
                self.x_pos += x_amount
                if not randint(0, 79):
                    self.turn(3)
            if self.y_pos - self.width < abs(y_amount):
                self.y_pos -= y_amount - (self.y_pos - self.width) + 0.01
                self.turn(10)
            elif self.y_pos + self.width + y_amount > SCREEN_HEIGHT:
                self.y_pos += (SCREEN_HEIGHT - (self.y_pos + self.width)) - 0.01
                self.turn(10)
            else:
                self.y_pos += y_amount
                if not randint(0, 79):
                    self.turn(3)
        else:
            sleep_time = randint(4000, 10000)
            self.sleep(sleep_time)

    def draw(self):

        line_length = 50
        # direction line
        line_x = line_length * sin(radians(self.fov_dir + 90))
        line_y = line_length * cos(radians(self.fov_dir + 90))
        pg.draw.line(win, (200, 200, 200), (self.x_pos, self.y_pos), (line_x+self.x_pos, line_y+self.y_pos))
        # FOV area
        # FOV lines
        fov_left_x = self.fov_range * sin(radians(self.fov_dir + 90 + self.fov_angle/2))
        fov_left_y = self.fov_range * cos(radians(self.fov_dir + 90 + self.fov_angle/2))
        fov_right_x = self.fov_range * sin(radians(self.fov_dir + 90 - self.fov_angle / 2))
        fov_right_y = self.fov_range * cos(radians(self.fov_dir + 90 - self.fov_angle / 2))
        pg.draw.line(win, (125, 125, 125), (self.x_pos, self.y_pos), (self.x_pos+fov_left_x, self.y_pos+fov_left_y))
        pg.draw.line(win, (125, 125, 125), (self.x_pos, self.y_pos), (self.x_pos+fov_right_x, self.y_pos+fov_right_y))
        # FOV arc
        fov_triangle_height = self.fov_range * cos(self.fov_angle/2)
        fov_arc_height = self.fov_range - fov_triangle_height
        fov_arc_width = 2 * (self.fov_range * sin(self.fov_angle/2))
        arc_rect = pg.Rect(self.x_pos + fov_left_x, self.y_pos + fov_left_y, fov_arc_width, fov_arc_height)
        pg.draw.arc(win, (255, 0, 0), arc_rect, 0, pi/2, 5)


        pg.draw.circle(win, (50, 50, 50), (self.x_pos, self.y_pos), self.width)

    def detect(self, fov_dir):
        pass

    def turn(self, turn_amount):
        if self.left_right == 1:
            for _ in range(turn_amount):
                self.fov_dir += self.rot_speed
            print(self.fov_dir)
        else:
            for _ in range(turn_amount):
                self.fov_dir -= self.rot_speed
            print(self.fov_dir)

    def sleep(self, sleep_time):
        if self.sleep_counter <= (sleep_time/1000)*FPS:
            self.sleep_counter += 1
        else:
            self.sleep_counter = 0
            self.awake = True


test = EnTest(24, 100, 100, 2, 5, 190, 100, 48, 10, 2)


if __name__ == '__main__':
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        win.fill((0, 0, 0))
        test.update()
        test.draw()
        pg.display.flip()
        clock.tick(FPS)


