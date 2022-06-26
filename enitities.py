import config
from math import sqrt, sin, cos, radians
from pg_funcs import *
from particles import get_cone


class Entity:
    def __init__(self, x, y, animation_path="", trans_color=(0, 0, 0)):
        # movement
        self.x = x
        self.y = y
        self.velX = 0
        self.velY = 0
        self.speed = 1
        # animation
        self.animation = load_animation_sequence(f'static/animation/{animation_path}', trans_color)
        self.width, self.height = self.animation[0].get_size()
        self.animation_timer, self.animation_index = 0, 0
        self.rotation = 0

    def draw(self, win, camera):
        if self.animation_timer >= config.FRAME_RATE // 6:
            self.animation_index += 1
            if self.animation_index == len(self.animation):
                self.animation_index = 0
            self.animation_timer = 0
        else:
            self.animation_timer, self.animation_index = 0, 0
        win.blit(rotate_image(self.animation[self.animation_index], self.rotation),
                             (self.x - self.width//2, self.y - self.height//2))

    def update(self):
        pass


class Player(Entity):
    def __init__(self, x, y, animation_path="", trans_color=(0, 0, 0)):
        super().__init__(x, y, animation_path=animation_path, trans_color=trans_color)
        self.controls = {'left': pg.K_a, 'right': pg.K_d, 'up': pg.K_w, 'down': pg.K_s, 'sprint': pg.K_LSHIFT}
        self.move_state = {control: False for control in self.controls.values()}

    def draw(self, win, camera):
        if any((move for key, move in self.move_state.items() if key in
                (v for k, v in self.controls.items() if k in ['left', 'right', 'up', 'down']))):
            self.animation_timer += 1
            if self.move_state[self.controls['sprint']]:
                self.animation_timer += 1
            if self.animation_timer >= config.FRAME_RATE//6:
                self.animation_index += 1
                if self.animation_index == len(self.animation):
                    self.animation_index = 0
                self.animation_timer = 0
        else:
            self.animation_timer, self.animation_index = 0, 0
        x, y = camera.player_pos(self.x, self.y)
        image = rotate_image(self.animation[self.animation_index], self.rotation)
        w, h = image.get_size()
        win.blit(image, (x-w//2, y-h//2))

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
        if self.move_state[self.controls['sprint']]:
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

        # set player angle
        if self.velX == 0:
            if self.velY > 0:
                self.rotation = 180
            elif self.velY < 0:
                self.rotation = 0
        elif self.velY == 0:
            if self.velX > 0:
                self.rotation = 270
            elif self.velX < 0:
                self.rotation = 90
        else:
            if self.velX > 0 and self.velY > 0:
                self.rotation = 225
            elif self.velX > 0 > self.velY:
                self.rotation = 315
            elif self.velX < 0 < self.velY:
                self.rotation = 135
            elif self.velX < 0 and self.velY < 0:
                self.rotation = 45


class Enemy(Entity):
    def __init__(self, x, y, animation_path="", trans_color=(0, 0, 0),
                 fov_angle=90, fov_range=40):
        super().__init__(x, y, animation_path=animation_path, trans_color=trans_color)
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.rotation = 0
        self.rot_angle = 60
        self.cone = get_cone(fov_range, fov_angle)
        self.fov_angle = fov_angle
        self.fov_range = fov_range
        self.animation = load_animation_sequence('static/animation/enemy', (0, 0, 0))
        self.animation_timer, self.animation_index = 0, 0
        self.hit_box = 0

    def draw(self, win, camera):
        fov_surf = pg.transform.rotate(self.cone, self.rotation-self.fov_angle//2)
        # blit circle and character
        iw, ih = fov_surf.get_size()
        x, y = camera.object_pos(self.x, self.y)
        win.blit(fov_surf, (x - iw // 2, y - ih // 2))
        e_image = rotate_image(self.animation[self.animation_index], self.rotation)
        win.blit(e_image, (x - e_image.get_width() // 2, y - e_image.get_width() // 2))

    def update(self):
        pass

    def boundary_check(self):
        pass


