import config
import pygame as pg


class StationaryCamera:
    def __init__(self):
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

    def player_pos(self, x, y):
        self.player_x, self.player_y = x, y
        return self.cx, self.cy

    def object_pos(self, x, y):
        return x + (self.cx - self.player_x), y + (self.cy - self.player_y)