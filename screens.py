import config
from pg_funcs import *
from particles import *
from enitities import *
from map import Map
from camera import *


class GameScreen:
    def __init__(self):
        self.player = Player(0, 0, animation_path='player')
        self.enemy_list = [Enemy(100, 100, animation_path='enemy'), Enemy(100, 200, animation_path='enemy')]
        self.flames = []
        self.offset = 0
        self.timer = 0
        self.camera = PlayerCamera()
        # self.flame_positions = [[40, 180]]
        # self.flame_positions = [[100, 120]]
        self.walls = [(130, 100, 10, 60), (180, 100, 50, 60), (190, 70, 3, 10)]
        self.light_map = create_lightmap(self.camera, [[self.player.x, self.player.y]], [Flame.color for _ in range(1)],
                        [0 for _ in range(1)], self.walls)

    def check_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in self.player.controls.values():
                self.player.handle_key_press(event.key, True)
        elif event.type == pg.KEYUP:
            if event.key in self.player.controls.values():
                self.player.handle_key_press(event.key, False)

    def update(self):
        for event in pg.event.get():
            self.check_event(event)
        self.player.update()
        for enemy in self.enemy_list:
            enemy.rotation += 1
            enemy.update()
        # for flame in self.flame_positions.copy():
        #     self.flames.append(Flame(*flame))
        # for flame in self.flames.copy():
        #     flame.run()
        #     if flame.timer == 90:
        #         self.flames.remove(flame)
        self.timer += 1
        if self.timer > 60:
            self.timer = 0
        #self.flame_positions = [[*get_mouse()]]
        # if self.timer % 5 == 0:
        #     self.flame_positions = [[f[0] + 1, f[1]] for f in self.flame_positions]
        self.light_map = create_lightmap(self.camera, [[self.player.x, self.player.y]],
                                         [Flame.color for _ in range(1)],
                                         [0 for _ in range(1)], self.walls)

    def draw(self, surface):
        surface.fill((0, 0, 0))
        for flame in self.flames:
            flame.draw(surface)
        self.camera.update_player(self.player.x, self.player.y)
        self.camera.update_camera()
        for enemy in self.enemy_list:
            enemy.draw(surface, self.camera)
        self.player.draw(surface, self.camera)
        surface.blit(self.light_map, (0, 0), special_flags=pg.BLEND_RGB_ADD)