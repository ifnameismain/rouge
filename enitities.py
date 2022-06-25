import config
from math import sqrt, sin, cos, radians
from pg_funcs import *


class Player:
    def __init__(self, x, y, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width, self.height = 16, 16
        self.color = color
        self.velX = 0
        self.velY = 0
        self.speed = 1
        self.leftPressed = False
        self.rightPressed = False
        self.upPressed = False
        self.downPressed = False
        self.running = False
        self.controls = {'left': pg.K_a, 'right': pg.K_d, 'up': pg.K_w, 'down': pg.K_s, 'sprint': pg.K_LSHIFT}
        self.move_state = {control: False for control in self.controls.values()}
        self.animation = load_animation_sequence('static/animation/player', (0, 0, 0))
        self.animation_timer, self.animation_index = 0, 0
        self.player_angle = 0

    def draw(self, win):
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

        win.blit(rotate_image(self.animation[self.animation_index], self.player_angle),
                             (self.x - self.width//2, self.y - self.height//2))


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
                self.player_angle = 180
            elif self.velY < 0:
                self.player_angle = 0
        elif self.velY == 0:
            if self.velX > 0:
                self.player_angle = 270
            elif self.velX < 0:
                self.player_angle = 90
        else:
            if self.velX > 0 and self.velY > 0:
                self.player_angle = 225
            elif self.velX > 0 > self.velY:
                self.player_angle = 315
            elif self.velX < 0 < self.velY:
                self.player_angle = 135
            elif self.velX < 0 and self.velY < 0:
                self.player_angle = 45


class Enemy:
    def __init__(self, x, y, color=(100, 250, 100), fov_angle=90, fov_range=40, aud_range=15, att_range=2):
        self.x = x
        self.y = y
        self.width, self.height = 16, 16
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.velX = 0
        self.velY = 0
        self.speed = 0.5
        self.running = False
        self.sleeping = False
        self.sleep_timer = 0
        self.enemy_angle = 90
        self.rot_angle = 60
        self.fov_angle = fov_angle
        self.fov_range = fov_range
        self.aud_range = aud_range
        self.att_range = att_range
        self.animation = load_animation_sequence('static/animation/enemy', (0, 0, 0))
        self.animation_timer, self.animation_index = 0, 0
        self.hit_box = 0

    def draw_2(self, win):
        # create surface for field of view semicircle
        radius = self.fov_range
        fov_surf = pg.Surface((2*radius, 2*radius))
        # Calculate angle center of eventual FOV circle slice.
        angle_center = self.fov_angle//2
        # Calculate rotation angle for FOV slice
        rotation_needed = self.enemy_angle - angle_center
        # draw semi-circle in centre of surface. image is now black with white semi circle
        pg.draw.circle(fov_surf, (255, 255, 255), (radius, radius), radius, radius-5, draw_top_left=True,
                       draw_bottom_left=True)
        # create black surface and ironically fill white (for Blend later)
        black_surf = pg.Surface((2*radius, 2*radius))
        black_surf.fill((255, 255, 255))
        # Blit black semicircle, image is now white with black semicircle
        pg.draw.circle(black_surf, (0, 0, 0), (radius, radius), radius, radius-5, draw_top_left=True,
                       draw_bottom_left=True)
        # rotate for surface blit
        black_surf = pg.transform.rotate(black_surf, self.fov_angle)
        # place images together and take the minimum. Should only be left with FOV slice thats white
        fov_surf.blit(black_surf, (0, 0), special_flags=pg.BLEND_RGB_MIN)
        # create light circle
        light_surf = pg.Surface((2 * radius, 2 * radius))
        for x in range(1, radius):
            pg.draw.circle(light_surf, (2*x, x, x), (radius, radius), radius - x)
        fov_surf.blit(light_surf, (0, 0), special_flags=pg.BLEND_RGB_MIN)
        # place images together and take the minimum. Should only be left with FOV slice thats receding white
        # rotate to position calculated
        fov_surf = pg.transform.rotate(fov_surf, rotation_needed)
        fov_surf.set_colorkey((0, 0, 0))
        # blit circle and character
        win.blit(fov_surf, (self.x-self.fov_range - self.width // 2, self.y-self.fov_range - self.height // 2))
        win.blit(rotate_image(self.animation[self.animation_index], self.enemy_angle),
                 (self.x - self.width // 2, self.y - self.height // 2))

    def draw(self, win):

        # Draws enemies FOV
        x1 = self.x
        y1 = self.y
        x2 = x1 - sin(radians(self.enemy_angle + (self.fov_angle / 2))) * self.fov_range
        y2 = y1 - cos(radians(self.enemy_angle + (self.fov_angle / 2))) * self.fov_range
        x3 = x1 - sin(radians(self.enemy_angle - (self.fov_angle / 2))) * self.fov_range
        y3 = y1 - cos(radians(self.enemy_angle - (self.fov_angle / 2))) * self.fov_range
        fov_points = [(x1, y1), (x2, y2), (x3, y3)]
        pg.draw.polygon(win, (200, 200, 200), fov_points)

        if not self.sleeping:
            self.animation_timer += 1
            if self.running:
                self.animation_timer += 3
            if self.animation_timer >= config.FRAME_RATE // 6:
                self.animation_index += 1
                if self.animation_index == len(self.animation):
                    self.animation_index = 0
                self.animation_timer = 0
        else:
            self.animation_timer, self.animation_index = 0, 0

        win.blit(rotate_image(self.animation[self.animation_index], self.enemy_angle),
                 (self.x - self.width // 2, self.y - self.height // 2))

    def update(self):
        pass

    def boundary_check(self):
        pass


