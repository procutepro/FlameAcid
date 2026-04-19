import pygame as pg
from FLAMEACID.flameacid.window.utils import *

def init(size, name):
    Playground = pg.display.set_mode(size)
    pg.display.set_caption(name)
    return Playground

def make_rect(pos, size, color, playground):
        x, y = map(int, pos)
        w, h = map(int, size)

        pg.draw.rect(playground, color_swap(color), pg.Rect(x, y, w, h))

def make_image(pos, size, angle, img_path, playground):
        Image_Surface = load(img_path)

        s = Image_Surface.get_size() if size == "normal" else size
        Image_Surface = pg.transform.scale(Image_Surface, s)
        Image_Surface = pg.transform.rotate(Image_Surface, angle)
        playground.blit(Image_Surface, pos)

def make_circle(pos, radius, color, playground, points=100):
        x, y = map(int, pos)
        pg.draw.circle(playground, color_swap(color), (x, y), radius)
    
def make_line(point1, point2, playground, color="white"):
    pg.draw.line(playground, color_swap(color), point1, point2)

def draw_triangle(color, position, points, playground):
        Swapped_Color = color_swap(color)
        Abs_Points = [(position[0] + x, position[1] + y) for x, y in points]
        pg.draw.polygon(playground, Swapped_Color, Abs_Points)

def make_pixel(pos, color, playground):
    x, y = map(int, pos)
    make_rect((x, y), (1, 1), color, playground)

def draw_shape(color, pos, points, playground):
        Abs_Points = [(pos[0] + x, pos[1] + y) for x, y in points]
        pg.draw.polygon(playground, color_swap(color), Abs_Points)

def fill(color, playground):
    Swapped_Color = color_swap(color)
    playground.fill(Swapped_Color)

def update():
    pg.display.update()

def make_sound(file, mode=0, volume=0.5):
    pg.mixer.init()
    pg.mixer.music.set_volume(volume)
    Sound = pg.mixer.Sound(file)
    Sound.play(loops=mode)

def close_sound():
    pg.mixer.stop()