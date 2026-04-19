from PIL import Image
import numpy as np
from FLAMEACID.flameacid.window.consts import *
from FLAMEACID.flameacid.window.core import *

class AcidImage:

    def __init__(self, size, screen: Window):
        self.Size = size
        self.Screen = screen
        self.W = int(size[0])
        self.H = int(size[1])
        self.Buffer = [[(0, 0, 0) for _ in range(self.W)] for _ in range(self.H)]
        self.Drawn_Pixels = []

    def draw_pixel(self, pos, color):
        Fixed_Pos = (max(pos[0] - 1, 0), max(pos[1] - 1, 0))
        Final_Color = tuple(color_swap(color))
        self.Buffer[Fixed_Pos[1]][Fixed_Pos[0]] = Final_Color
        self.Drawn_Pixels.append((Fixed_Pos, Final_Color))

    def draw_line(self, start_pos, end_pos, color):
        Line_Pos = line_points(start_pos, end_pos)
        for i in Line_Pos:
            self.draw_pixel(i, color_swap(color))

    def draw_triangle(self, pos1, pos2, pos3, color):
        Triangle_Points = fill_triangle(pos1, pos2, pos3)
        for i in Triangle_Points:
            self.draw_pixel(i, color_swap(color))

    def draw(self, pos, shader=None):
        for i in self.Drawn_Pixels:
            x = i[0][0]
            y = i[0][1]
            Color = color_swap(i[1])

            if shader is None:
                Final_Pos = (x + pos[0], y + pos[1])
                if Final_Pos[0] < self.Screen.Size[0] and Final_Pos[1] < self.Screen.Size[1]:
                    if not list(Color) == list(self.Screen.Background_Color):
                        self.Screen.make_pixel(Final_Pos, Color)
            else:
                u = x / self.Screen.Size[0]
                v = y / self.Screen.Size[1]
                Old_R = Color[0] / 255
                Old_G = Color[1] / 255
                Old_B = Color[2] / 255
                Shaded = shader(u, v, (Old_R, Old_G, Old_B))
                Final_Color = (Shaded[0] * 255, Shaded[1] * 255, Shaded[2] * 255)
                self.Screen.make_pixel((x + pos[0], y + pos[1]), Final_Color)

    def export(self, filepath, shader=None):
        Export_Buffer = np.zeros((self.H, self.W, 3), dtype=np.uint8)

        for y in range(self.H):
            for x in range(self.W):
                Old_Color = self.Buffer[y][x]

                if shader is None:
                    r, g, b = Old_Color
                else:
                    Old_R = Old_Color[0] / 255
                    Old_G = Old_Color[1] / 255
                    Old_B = Old_Color[2] / 255
                    u = x / self.W
                    v = y / self.H
                    Shaded = shader(u, v, (Old_R, Old_G, Old_B))
                    r = int(Shaded[0] * 255)
                    g = int(Shaded[1] * 255)
                    b = int(Shaded[2] * 255)

                Export_Buffer[y, x] = [r, g, b]

        Img = Image.fromarray(Export_Buffer)
        Img.save(filepath)