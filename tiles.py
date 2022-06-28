import pygame as pg
from config import *
from pg_funcs import *
from numpy.random import uniform
from time import sleep


class Tile:
    def __init__(self, offset: tuple, image_path: str, solid: bool):
        self.offset = offset
        self.solid = solid
        self.image_path = image_path



class Lamp(Tile):
    def __init__(self, power_on: bool, light_range: int, brightness: int, globe_quality: int, offset: tuple, image_path: str = "", solid: bool = True):
        super().__init__(self, offset, image_path, solid)
        self.power_on = power_on
        self.light_range = light_range
        self.brightness = brightness
        self.globe_quality = globe_quality # 1=good, 2=ok, 3=bad, 4=broken
        self.power_factor = [1, 0.8, 0.5, 0]
        self.power_factor_current = 0
        self.flicker_time = 10 # 10 frames before re-calc for flicker on / off

    def quality_setting(self):
        if globe_quality == 1:
            self.power_factor_current = self.power_factor[0]
        elif globe_quality == 2:
            self.power_factor_current = self.power_factor[1]
        elif globe_quality == 3:
            self.power_factor_current = self.power_factor[2]
        elif globe_quality == 4:
            self.power_factor_current = self.power_factor[3]

    def light_on(self):
        if self.flicker_time % 10 == 0:
            quality_setting()
            flicker_prob = uniform()
            if self.power_factor_current >= flicker_prob:
                self.power_on = True
            else:
                self.power_on = False
            self.flicker_time = 1
        self.flicker_time += 1

    def globe_degradation(self):
        pass



class Vase(Tile):
    def __init__(self, item_prob: float, offset: tuple, image_path: str = "", solid: bool = True):
        super().__init__(self, offset, image_path, solid)
        self.contain_item = False
        self.item_prob = item_prob
        self.item_rarity = None
        self.rarity_chance = ITEM_RARITY # basic, decent, frothy, sauced

    def get_rarity(self):
        x = uniform()
        if x >= self.rarity_chance[0]:
            self.item_rarity = "Basic"
        elif x >= self.rarity_chance[1]:
            self.item_rarity = "Decent"
        elif x >= self.rarity_chance[2]:
            self.item_rarity = "Frothy"
        elif x >= self.rarity_chance[3]:
            self.item_rarity = "Sauced"

    def check_item(self):
        x = uniform()
        if self.item_prob > x:
            self.contain_item = True
            get_rarity()






