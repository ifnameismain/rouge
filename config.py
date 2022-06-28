import pygame as pg

pg.display.init()
pg.font.init()
GAME_CAPTION = "Rouge"
UNSCALED_SIZE = (480, 280)
SCALED_SIZE = (480*2, 280*2)
FRAME_RATE = 60
CONTROLS = {'player': {'up': pg.K_w, 'down': pg.K_s, 'left': pg.K_a, 'right': pg.K_d}}
FONTS = {"BIG": pg.font.SysFont("arial", 100, True),
         "MEDIUM": pg.font.SysFont("arial", 50, True),
         "SMALL": pg.font.SysFont("arial", 30, True)}
TILE_SIZE = (16, 16)
ITEM_RARITY = [0, 0.5, 0.75, 0.9] # basic, decent, frothy, sauced