import pygame as pg
from FLAMEACID.flameacid.window.utils import *
import math as m
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

def draw_triangle(color, position, points, playground, renderer, screen_size, vbo, Gl_Shader):
        Swapped_Color = color_swap(color)

        if renderer == "pygame":
            Abs_Points = [(position[0] + x, position[1] + y) for x, y in points]
            pg.draw.polygon(playground, Swapped_Color, Abs_Points)

        elif renderer == "opengl":
            Abs_Points = [(position[0] + x, position[1] + y) for x, y in points]
            Ndc_Points = [pixel_to_ndc(x, y, screen_size[0], screen_size[1]) for x, y in Abs_Points]
            Vertices = np.array([
                Ndc_Points[0][0], Ndc_Points[0][1], 0.0,
                Ndc_Points[1][0], Ndc_Points[1][1], 0.0,
                Ndc_Points[2][0], Ndc_Points[2][1], 0.0
            ], dtype=np.float32)

            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glBufferData(GL_ARRAY_BUFFER, Vertices.nbytes, Vertices, GL_DYNAMIC_DRAW)

            Pos_Loc = glGetAttribLocation(Gl_Shader, "position")
            glEnableVertexAttribArray(Pos_Loc)
            glVertexAttribPointer(Pos_Loc, 3, GL_FLOAT, False, 0, None)

            Color_Loc = glGetUniformLocation(Gl_Shader, "uColor")
            glUniform3f(Color_Loc, Swapped_Color[0]/255, Swapped_Color[1]/255, Swapped_Color[2]/255)

            glDrawArrays(GL_TRIANGLES, 0, 3)

def make_rect(pos, size, color, playground, renderer, screen_size, GL_shader, vbo):
        x, y = map(int, pos)
        w, h = map(int, size)
        Tri_1 = [[x, y], [x+w, y], [x, y+h]]
        Tri_2 = [[x, y+h], [x+w, y], [x+w, y+h]]
        draw_triangle(color, (0, 0), Tri_1, playground, renderer, screen_size, vbo, GL_shader)
        draw_triangle(color, (0, 0), Tri_2, playground, renderer, screen_size, vbo, GL_shader)

def make_image(pos, size, angle, img_path, playground):
        Image_Surface = load(img_path)

        s = Image_Surface.get_size() if size == "normal" else size
        Image_Surface = pg.transform.scale(Image_Surface, s)
        Image_Surface = pg.transform.rotate(Image_Surface, angle)
        playground.blit(Image_Surface, pos)

def make_circle(pos, radius, color, playground, renderer, screen_size, vbo, GL_shader, points=100):
    x, y = map(int, pos)
    Angle_Step = (2 * m.pi) / points

    for i in range(points):
        xi = round(radius * m.cos(i * Angle_Step)) + x
        yi = round(radius * m.sin(i * Angle_Step)) + y
        xj = round(radius * m.cos((i + 1) % points * Angle_Step)) + x
        yj = round(radius * m.sin((i + 1) % points * Angle_Step)) + y
        draw_triangle(color_swap(color), (0, 0), [[xi, yi], [xj, yj], list(pos)], playground, renderer, screen_size, vbo, GL_shader)

def make_line(point1, point2, playground, color="white"):
    pg.draw.line(playground, color_swap(color), point1, point2)

def make_pixel(pos, color, playground, renderer, screen_size, vbo, GL_shader):
    x, y = map(int, pos)
    make_rect((x, y), (1, 1), color, playground, renderer, screen_size, vbo, GL_shader)

def draw_shape(color, pos, points, playground, ):
        Abs_Points = [(pos[0] + x, pos[1] + y) for x, y in points]
        pg.draw.polygon(playground, color_swap(color), Abs_Points)

def fill(color, playground):
    Swapped_Color = color_swap(color)
    playground.fill(Swapped_Color)

def update(renderer):
    pg.display.flip()

def make_sound(file, mode=0, volume=0.5):
    pg.mixer.init()
    pg.mixer.music.set_volume(volume)
    Sound = pg.mixer.Sound(file)
    Sound.play(loops=mode)

def close_sound():
    pg.mixer.stop()