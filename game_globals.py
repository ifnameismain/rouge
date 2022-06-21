import pygame as pg

# init pygame
pg.display.init()
pg.font.init()

# window specs
GAME_CAPTION = "Rouge"
UNSCALED_SIZE = (480, 280)
SCALED_SIZE = (480*2, 280*2)
FRAME_RATE = 60

# player specs
CONTROLS = {'player': {'up': pg.K_w, 'down': pg.K_s, 'left': pg.K_a, 'right': pg.K_d}}

# game specs
FONTS = {"BIG": pg.font.SysFont("arial", 100, True),
         "MEDIUM": pg.font.SysFont("arial", 50, True),
         "SMALL": pg.font.SysFont("arial", 30, True)}

