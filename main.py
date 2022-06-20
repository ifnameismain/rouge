from screens import *

GAME_CAPTION = "Rouge"
UNSCALED_SIZE = (480, 280)
SCALED_SIZE = (480*2, 280*2)
FRAME_RATE = 60
CONTROLS = {'player': {'up': pg.K_w, 'down': pg.K_s, 'left': pg.K_a, 'right': pg.K_d}}


class Controller:
    def __init__(self):
        self.display = pg.display.get_surface()
        self.window = pg.Surface(UNSCALED_SIZE)
        self.game_running = True
        self.clock = pg.time.Clock()
        self.frame_rate = FRAME_RATE
        self.screen = None

    def get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_running = False
            else:
                self.screen.check_event(event)

    def main_loop(self):
        self.screen = SCREENS['game']
        while self.game_running:
            self.clock.tick(self.frame_rate)
            self.get_events()
            self.screen.update()
            self.screen.draw(self.window)
            self.display.blit(pg.transform.scale(self.window, SCALED_SIZE), (0, 0))
            pg.display.update()
        pg.quit()


if __name__ == '__main__':
    os.environ["SDL_VIDEO_CENTERED"] = "True"
    pg.display.init()
    pg.font.init()
    FONTS = {"BIG": pg.font.SysFont("arial", 100, True),
             "MEDIUM": pg.font.SysFont("arial", 50, True),
             "SMALL": pg.font.SysFont("arial", 30, True)}
    pg.display.set_caption(GAME_CAPTION)
    display_info = pg.display.Info()
    SCREEN_SIZE = (display_info.current_w, display_info.current_h)
    pg.display.set_mode(SCALED_SIZE)
    controller = Controller()
    SCREENS = {'game': GameScreen()}
    controller.main_loop()
