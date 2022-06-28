import pygame as pg
from config import *
from pg_funcs import *


class Item:
    def __init__(self, name: str, description: str, category: str):
        self.name = name
        self.description = description
        self.category = category


class Flashlight(Item):
    def __init__(self, rarity: int, image: str, name: str, description: str, category: str):
        super().__init__('Flashlight', 'Lights the way ahead... But not behind!', 'Tool')
        self.range = 20 + (10 * rarity) # 30, 40, 50, 60
        self.fov = 120 - (10 * rarity) # 110, 100, 90, 80
        self.battery_life = float(30 + (10 * rarity)) # 40, 50, 60, 70 (seconds)
        self.turned_on = False


    def battery_used(self):
        if self.turned_on:
            self.battery_life -= 1/FRAME_RATE

    def battery_depleted(self):
        if not self.battery_life:
            self.turned_on = False


class Lantern(Item):
    def __init__(self, rarity: int, image: str, name: str, description: str, category: str):
        super().__init__('Lantern', 'Helps you find your way in the darkness', 'Tool')
        self.range = 15 + (5 * rarity)  # 20, 25, 30, 35
        self.fov = 360
        self.oil_amount = float(30 + (10 * rarity))  # 40, 50, 60, 70 (grams)
        self.turned_on = False

    def oil_used(self):
        if self.turned_on:
            self.oil_amount -= 1 / FRAME_RATE

    def oil_depleted(self):
        if not self.oil_amount:
            self.turned_on = False