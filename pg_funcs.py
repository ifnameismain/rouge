import pygame as pg
import os.path
import glob

def create_text_object(text, font, position: tuple, color, max_size=(0, 0), line_width=20):
    words = [line.split(' ') for line in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = max_size
    x, y = position
    init_y = y
    text_obj = []
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if max_height != 0:
                if x + word_width >= max_width:
                    x = position[0]  # Reset the x.
                    y += word_height  # Start on new row.
            text_obj.append((word_surface, (x, y)))
            x += word_width + space
        x = position[0]  # Reset the x.
        y += word_height + line_width  # Start on new row.
        if max_height != 0:
            if y-init_y > max_height - 0.5*font.size(' ')[0]:
                break
    return text_obj


def centred_text(text, font, centre_pos: tuple, color):
    text_surface = font.render(text, 0, color)
    text_width, text_height = text_surface.get_size()
    return text_surface, (centre_pos[0]-0.5*text_width, centre_pos[1]-0.5*text_height)


def blit_text_object(surface, text_obj):
    if type(text_obj) == list:
        for word in text_obj:
            surface.blit(word[0], word[1])
    else:
        surface.blit(text_obj[0], text_obj[1])


def create_button(pos, size, color=pg.color.Color('white'),
                  text_color=pg.color.Color('black'), text=None, font=None):
    _rect = (pg.rect.Rect(pos[0], pos[1], size[0], size[1]), color)
    if text:
        text_obj = centred_text(text, font, (pos[0]+0.5*size[0], pos[1]+0.5*size[1]), text_color)
        return _rect, text_obj
    else:
        return _rect


def get_mouse():
    from main import SCALED_SIZE, UNSCALED_SIZE
    pos = tuple(p* UNSCALED_SIZE[i]/SCALED_SIZE[i] for i, p in enumerate(pg.mouse.get_pos()))
    return pos


def draw_tile(window, pos, color, size, border=False, border_col=(255,255,255)):
    tile = pg.rect.Rect(pos[0], pos[1], size, size)
    window.fill(color, tile)
    if border:
        pg.draw.rect(window, border_col, tile, 2)


def flip_image(img, x_boolean=True, y_boolean=False):
    return pg.transform.flip(img, x_boolean, y_boolean)


def load_animation_sequence(descriptor, color_key=None):
    animations = []
    for path in glob.glob(descriptor.replace('\\', '/') + '/*'):
        animations.append(pg.image.load(path).convert())
        if color_key:
            animations[-1].set_colorkey(color_key)
    return animations


def load_tile_sequence(descriptor, color_key=None):
    animations = []
    animation_paths = []
    addons = {}
    for path in glob.glob(descriptor.replace('\\', '/') + '/*'):
        animations.append(pg.image.load(path).convert_alpha())
        path = path.replace('textures', 'texture_addons')
        animation_paths.append(path)
        if os.path.isfile(path):
            addons[path] = load_texture_addons(path)
        if color_key:
            animations[-1].set_colorkey(color_key)
    return animations, animation_paths, addons


def load_texture_addons(path, color_key=None):
    animations = []
    image = pg.image.load(path).convert_alpha()
    animations.append(image.copy())
    animations.append(flip_image(pg.transform.rotate(image.copy(), 90)).convert_alpha())
    animations.append(pg.transform.rotate(image.copy(), 90).convert_alpha())
    animations.append(flip_image(image.copy(), False, True).convert_alpha())
    if color_key:
        animations[-2].set_colorkey(color_key)
        animations[-1].set_colorkey(color_key)
    return animations


def load_sprites(descriptor, color_key=None):
    animations = []
    for path in glob.glob(descriptor.replace('\\', '/') + '/*'):
        if '.png' in path:
            animations.append(pg.image.load(path).convert_alpha())
            if color_key:
                animations[-1].set_colorkey(color_key)
        else:
            pass
    for path in glob.glob(descriptor.replace('\\', '/') + '/**/*', recursive=True):
        if '.png' in path and 'horizontal\\' in path:
            image = pg.image.load(path).convert_alpha()
            animations.append(image.copy())
            animations.append(flip_image(image.copy()))
            if color_key:
                animations[-2].set_colorkey(color_key)
                animations[-1].set_colorkey(color_key)
        elif '.png' in path and 'vertical\\' in path:
            image = pg.image.load(path).convert_alpha()
            animations.append(image.copy())
            animations.append(flip_image(image.copy(), False, True))
            if color_key:
                animations[-2].set_colorkey(color_key)
                animations[-1].set_colorkey(color_key)
        elif '.png' in path and 'all\\' in path:
            image = pg.image.load(path).convert_alpha()
            animations.append(image.copy())
            animations.append(flip_image(pg.transform.rotate(image.copy(), 90)))
            animations.append(pg.transform.rotate(image.copy(), 90))
            animations.append(flip_image(image.copy(), False, True))
            if color_key:
                animations[-2].set_colorkey(color_key)
                animations[-1].set_colorkey(color_key)
        else:
            pass

    return animations


def load_entity_animations(descriptor):
    d = descriptor.split('\\')[-1].replace('static/', '')[:-1]
    animations = {d: {}}
    for animation_path in glob.glob(descriptor+'*'):
        a = animation_path.split('\\')[-1]
        animations[d][a] = load_animation_sequence(animation_path, (0,0,0))
    return animations


def rotate_image(image, angle):
    return pg.transform.rotate(image, angle)

