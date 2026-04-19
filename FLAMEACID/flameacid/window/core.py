from FLAMEACID.flameacid.window.main_loader.loader import *

class Window:
    def __init__(self, size, name, renderer="pygame"):
        self.Bro_Running = True
        self.Size = size
        self.Name = name
        self.Screen = None
        self.Background_Color = (0, 0, 0)
        self.renderer = renderer

    def init(self):
        pg.init()

        if self.renderer == "pygame":
            self.Screen = pg.display.set_mode(self.Size)

        elif self.renderer == "opengl":
            pg.display.set_mode(self.Size, pg.OPENGL | pg.DOUBLEBUF)

            self.Gl_Shader = compileProgram(
                compileShader(TEMPLATE_VERTEX_SHADER, GL_VERTEX_SHADER),
                compileShader(TEMPLATE_FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
            )

            self.Vbo = glGenBuffers(1)
            glUseProgram(self.Gl_Shader)

        pg.display.set_caption(self.Name)

    def make_rect(self, pos, size, color):
        make_rect(pos, size, color, self.Screen, self.renderer, self.Size, self.Gl_Shader, self.Vbo)

    def make_image(self, pos, size, angle, img_path):
        make_image(pos, size, angle, img_path, self.Screen)

    def make_circle(self, pos, radius, color):
        make_circle(pos, radius, color, self.Screen, self.renderer, self.Size, self.Gl_Shader, self.Vbo)

    def make_line(self, point1, point2, color="white"):
        make_line(point1, point2, self.Screen, color)

    def draw_triangle(self, color, position, points):
        draw_triangle(color, position, points, self.Screen, self.renderer, self.Size, self.Gl_Shader, self.Vbo)

    def make_pixel(self, pos, color):
        make_pixel(pos, color, self.renderer, self.Screen, self.Size, self.Vbo, self.Gl_Shader)

    def draw_shape(self, color, pos, points):
        draw_shape(color, pos, points, self.Screen)

    def fill(self, color):
        fill(color, self.Screen)
        self.Background_Color = color_swap(color)

    def update(self):
        update(self.renderer)

    def loop(self):
        for self.Event in pg.event.get():
            if self.Event.type == pg.QUIT:
                self.Bro_Running = False
                pg.quit()