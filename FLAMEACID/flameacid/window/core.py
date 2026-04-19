from FLAMEACID.flameacid.window.PyGame.pygame_loader import *

class Window:
    def __init__(self, size, name):
        self.Bro_Running = True
        self.Size = size
        self.Name = name
        self.Screen = None
        self.Background_Color = (0, 0, 0)

    def init(self):
        self.Screen = init(self.Size, self.Name)

    def make_rect(self, pos, size, color):
        make_rect(pos, size, color, self.Screen)

    def make_image(self, pos, size, angle, img_path):
        make_image(pos, size, angle, img_path, self.Screen)

    def make_circle(self, pos, radius, color):
        make_circle(pos, radius, color, self.Screen)

    def make_line(self, point1, point2, color="white"):
        make_line(point1, point2, self.Screen, color)

    def draw_triangle(self, color, position, points):
        draw_triangle(color, position, points, self.Screen)

    def make_pixel(self, pos, color):
        make_pixel(pos, color, self.Screen)

    def draw_shape(self, color, pos, points):
        draw_shape(color, pos, points, self.Screen)

    def fill(self, color):
        fill(color, self.Screen)
        self.Background_Color = color_swap(color)

    def update(self):
        update()

    def loop(self):
        for self.Event in pg.event.get():
            if self.Event.type == pg.QUIT:
                self.Bro_Running = False
                pg.quit()