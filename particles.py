import config
import pygame as pg
import random
import time
import math


def create_lightmap(camera, sources, colors, sizes, obstacles: list = None):
    light_surf = pg.Surface((pg.display.Info().current_w, pg.display.Info().current_h))
    max_surf = light_surf.copy()
    obs_surf = light_surf.copy()
    max_light_intensity = 60
    max_surf.fill((max_light_intensity, max_light_intensity, max_light_intensity))
    light_intensity = 30
    light_step = 2
    light_radius = light_intensity * light_step
    for source, color, size in zip(sources, colors, sizes):
        source = [source[0]+(camera.cx - camera.player_x), source[1]+(camera.cy - camera.player_y)]
        surf = pg.Surface((light_radius*2, light_radius*2))
        # gradient light
        for x in range(1, light_radius, light_step):
            pg.draw.circle(surf, (x, x, x), (light_radius, light_radius), light_radius-x)
        # calculate obstacle polygon
        for o in obstacles:
            obs = [o[0]+1+(camera.cx - camera.player_x), o[1]+1+(camera.cy - camera.player_y), o[2]-3, o[3]-3]
            corners = [(obs[0], obs[1]), (obs[0] + obs[2], obs[1]), (obs[0] + obs[2], obs[1] + obs[3]),
                       (obs[0], obs[1] + obs[3])]
            # check relative side
            poly = []
            # binary search sides of polygon
            if source[0] <= obs[0]:
                if source[1] <= obs[1]:
                    poly.append(corners[0])
                    poly.append(corners[1])
                    for corner in [corners[1], corners[3]]:
                        poly.append(get_poly_coord(corner, source, light_radius))
                    poly.append(corners[3])
                elif source[1] <= obs[1] + obs[3]:
                    poly.append(corners[0])
                    for corner in [corners[0], corners[3]]:
                        poly.append(get_poly_coord(corner, source, light_radius))
                    poly.append(corners[3])
                else:
                    poly.append(corners[0])
                    for corner in [corners[0], corners[2]]:
                        poly.append(get_poly_coord(corner, source, light_radius))
                    poly.append(corners[2])
                    poly.append(corners[3])
            elif source[0] <= obs[0] + obs[2]:
                if source[1] <= obs[1]:
                    poly.append(corners[1])
                    for corner in [corners[1], corners[0]]:
                        poly.append(get_poly_coord(corner, source, light_radius))
                    poly.append(corners[0])
                else:
                    poly.append(corners[3])
                    for corner in [corners[3], corners[2]]:
                        poly.append(get_poly_coord(corner, source, light_radius))
                    poly.append(corners[2])
            else:
                if source[1] <= obs[1]:
                    poly.append(corners[0])
                    poly.append(corners[1])
                    poly.append(corners[2])
                    for corner in [corners[2], corners[0]]:
                        poly.append(get_poly_coord(corner, source, light_radius))
                elif source[1] <= obs[1] + obs[3]:
                    poly.append(corners[2])
                    for corner in [corners[2], corners[1]]:
                        poly.append(get_poly_coord(corner, source, light_radius))
                    poly.append(corners[1])
                else:
                    poly.append(corners[1])
                    poly.append(corners[2])
                    poly.append(corners[3])
                    for corner in [corners[3], corners[1]]:
                        poly.append(get_poly_coord(corner, source, light_radius))
            pg.draw.polygon(surf, (0, 0, 0),
                            [(corner[0] - source[0] + light_radius, corner[1] - source[1] + light_radius) for corner in poly])
        light_surf.blit(surf, (source[0]-light_radius, source[1]-light_radius), special_flags=pg.BLEND_RGB_ADD)

    max_surf.blit(light_surf, (0, 0), special_flags=pg.BLEND_RGB_MIN)
    for obs in obstacles:
        obs = [obs[0] + (camera.cx - camera.player_x), obs[1] + (camera.cy - camera.player_y), obs[2], obs[3]]
        pg.draw.rect(obs_surf, (120, 120, 120), obs)
    obs_surf.blit(max_surf, (0, 0), special_flags=pg.BLEND_RGB_MULT)
    max_surf.blit(obs_surf, (0, 0), special_flags=pg.BLEND_RGB_ADD)
    return max_surf


def get_poly_coord(c, source, radius):
    p = c
    run, rise = c[0] - source[0], c[1] - source[1]
    while (p[0] - source[0]) ** 2 + (p[1] - source[1]) ** 2 < 6 * radius ** 2:
        p = [p[0] + run, p[1] + rise]
    return p


def get_cone(radius, angle, center_width=5):
    # create surface for field of view semicircle
    fov_surf = pg.Surface((2 * radius, 2 * radius))
    # Calculate rotation angle for FOV slice
    # draw semi-circle in centre of surface. image is now black with white semi circle
    pg.draw.circle(fov_surf, (255, 255, 255), (radius, radius), radius, radius - center_width, draw_top_left=True,
                   draw_bottom_left=True)
    # create black surface and ironically fill white (for Blend later)
    black_surf = pg.Surface((2 * radius, 2 * radius))
    black_surf.fill((255, 255, 255))
    # Blit black semicircle, image is now white with black semicircle
    pg.draw.circle(black_surf, (0, 0, 0), (radius, radius), radius, radius - center_width, draw_top_left=True,
                   draw_bottom_left=True)
    # rotate for surface blit
    black_surf = pg.transform.rotate(black_surf, angle)
    # place images together and take the minimum. Should only be left with FOV slice thats white
    fov_surf.blit(black_surf, (0, 0), special_flags=pg.BLEND_RGB_MIN)
    # create light circle
    light_surf = pg.Surface((2 * radius, 2 * radius))
    for x in range(1, radius):
        pg.draw.circle(light_surf, (2 * x, x, x), (radius, radius), radius - x)
    # place images together and take the minimum. Should only be left with FOV slice thats receding white
    fov_surf.blit(light_surf, (0, 0), special_flags=pg.BLEND_RGB_MIN)
    fov_surf.set_colorkey((0, 0, 0))
    return fov_surf



class Flame:
    color = (10, 0, 0)

    def __init__(self, x, y):
        self.pos = [int(x), int(y)]
        self.vel = [random.uniform(-0.1, 0.1), random.uniform(-1, -1.5)]
        self.timer = 100

    def run(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.timer -= 1

    def draw(self, surface, size=1):
        radius = self.timer / 20
        surf = pg.Surface((size*2*radius, size*2*radius))
        pg.draw.circle(surf, self.color, (size*radius, size*radius), size*radius)
        pg.draw.circle(surf, pg.Color('orange'), (size*radius, size*radius), 0.5*size*radius)
        surface.blit(surf, self.pos, special_flags=pg.BLEND_RGB_ADD)
