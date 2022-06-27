import config
import pygame as pg


class StationaryCamera:
    def __init__(self):
        pass

    def update_player(self, x, y):
        pass

    def update_camera(self):
        pass

    def player_pos(self, x, y):
        return x, y

    def object_pos(self, x, y):
        return x, y


class PlayerCamera:
    def __init__(self):
        self.cx, self.cy = config.UNSCALED_SIZE[0] // 2, config.UNSCALED_SIZE[1] // 2
        self.player_x, self.player_y = 0, 0
        self.player_width, self.player_height = 0, 0
        self.origin_x, self.origin_y = 0, 0

    def update_player(self, x, y):
        self.player_x, self.player_y = x, y

    def update_camera(self):
        pass

    def player_pos(self, x, y):
        return self.cx, self.cy

    def object_pos(self, x, y):
        return x + (self.cx - self.player_x), y + (self.cy - self.player_y)


class SmoothCamera:
    def __init__(self):
        self.cx, self.cy = config.UNSCALED_SIZE[0] // 2, config.UNSCALED_SIZE[1] // 2
        self.camera_x, self.camera_y = 0, 0
        self.blit_x, self.blit_y = self.cx, self.cy
        self.player_x, self.player_y = 0, 0
        self.player_width, self.player_height = 0, 0
        self.origin_x, self.origin_y = 0, 0
        self.vel_x, self.vel_y = 0, 0
        self.offset_x, self.offset_y = 0, 0
        self.proportional = 0.2
        self.fade = 0.05

    def update_player(self, x, y):
        self.player_x, self.player_y = x, y

    def player_pos(self, x, y):
        return self.blit_x, self.blit_y

    def calculate(self):
        self.vel_x = self.proportional * (self.blit_x - self.cx)
        #self.vel_x = self.vel_x - self.fade if self.vel_x > 0 else self.vel_x + self.fade if self.vel_x < 0 else self.vel_x
        self.vel_y = self.proportional * (self.blit_y - self.cy)
        #self.vel_y = self.vel_y - self.fade if self.vel_y > 0 else self.vel_y + self.fade if self.vel_y < 0 else self.vel_y

    def update_camera(self):
        self.blit_x = self.cx + self.player_x - self.camera_x
        self.blit_y = self.cy + self.player_y - self.camera_y
        self.calculate()
        self.camera_x += self.vel_x
        self.camera_y += self.vel_y
        self.offset_x = self.cx - self.camera_x
        self.offset_y = self.cy - self.camera_y


    def object_pos(self, x, y):
        return x + self.offset_x, y + self.offset_y
