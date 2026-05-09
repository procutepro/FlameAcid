import moderngl as mgl
import pygame as pg
import glm
import sys
import numpy as np
import Flame3D.obj_laoder as obj
import os

def send_my_friend_to_gf_gpu(shader, stuff, name):
    shader[name].write(stuff)

class Mesh:
    def __init__(self, model_path, pos, size, rotation, ctx, shader_name):
        self.pos = pos
        self.size = size
        self.rotation = rotation

        self.model_path = model_path
        self.ctx = ctx

        model_data = obj.load_obj(model_path)
        faces = model_data[0]
        self.name = model_data[1]
        self.mtlfile = model_data[2]
        vbo_data = []
        for tri in faces:
            vbo_data.extend(tri)

        self.shader = self.ctx.shaders[shader_name]
        
        self.vbo = ctx.ctx.buffer(np.array(vbo_data, dtype='f4').tobytes())
        self.vao = ctx.ctx.vertex_array(self.shader, [
            (self.vbo, '3f 2f', 'in_position', 'in_uv')
        ])

        self.transform_matrix = self.get_model_matrix()

        self.projection_mat()

        self.load_texture()

    def load_texture(self):

        path = ""
        
        with open(self.mtlfile) as f:
            data = f.readlines()
        
        for i in data:
            cmd = i.split(" ")[0]
            parts = i.split(" ")[1:]

            if cmd == "map_Kd":
                path = parts[0]

        img = pg.image.load(path.strip())
        img = pg.transform.flip(img, False, True)
        img_data = pg.image.tostring(img, 'RGBA', True)

        self.texture = self.ctx.ctx.texture(img.get_size(), 4, img_data)
        self.texture.filter = (mgl.NEAREST, mgl.NEAREST)
    
    def get_model_matrix(self):
        model = glm.mat4()
        model = glm.translate(model, self.pos)
        model = glm.scale(model, self.size)
        model = glm.rotate(model, glm.radians(self.rotation[0]), (1,0,0))
        model = glm.rotate(model, glm.radians(self.rotation[1]), (0,1,0))
        return model
    
    def projection_mat(self):
        aspect = self.ctx.size[0]/self.ctx.size[1]
        self.mat = glm.perspective(self.ctx.camera.fovy, aspect, self.ctx.camera.near, self.ctx.camera.far)
    
    def render(self):
        self.shader['u_model'].write(self.transform_matrix)
        self.shader['u_view'].write(self.ctx.camera.mat)
        self.shader['u_projection'].write(self.mat)
        if hasattr(self, 'texture'):
            self.texture.use()
            self.shader['u_texture'].value = 0
        self.vao.render()

class Camera:
    def __init__(self, near=0.01, far=1000, pos=(0, 0, 0), target=(0, 0, 0), up=(0, 1, 0), fovy=60):
        self.near = near
        self.far = far
        self.pos = glm.vec3(pos)
        self.target = glm.vec3(target)
        self.up = glm.vec3(up)
        self.fovy = glm.radians(fovy)
        self.update_matrix()
    
    def update_matrix(self):
        """Call this whenever pos/target changes"""
        self.mat = glm.lookAt(self.pos, self.target, self.up)
    
    def move_forward(self, distance):
        direction = glm.normalize(self.target - self.pos)
        self.pos += direction * distance
        self.target += direction * distance
        self.update_matrix()
    
    def move_right(self, distance):
        direction = glm.normalize(self.target - self.pos)
        right = glm.normalize(glm.cross(direction, self.up))
        self.pos += right * distance
        self.target += right * distance
        self.update_matrix()
    
    def orbit(self, delta_yaw, delta_pitch):
        """Rotate around target (uses spherical coordinates)"""
        radius = glm.distance(self.pos, self.target)
        
        # Get current angles
        direction = self.pos - self.target
        yaw = glm.atan(direction.z, direction.x)
        pitch = glm.asin(direction.y / radius)
        
        # Update angles
        yaw += glm.radians(delta_yaw)
        pitch += glm.radians(delta_pitch)
        pitch = glm.clamp(pitch, -glm.radians(89), glm.radians(89))
        
        # Calculate new position
        self.pos.x = self.target.x + radius * glm.cos(yaw) * glm.cos(pitch)
        self.pos.z = self.target.z + radius * glm.sin(yaw) * glm.cos(pitch)
        self.pos.y = self.target.y + radius * glm.sin(pitch)
        
        self.update_matrix()

class Window:
    def __init__(self, size, name):
        pg.init()
        self.Size = glm.vec2(size[0], size[1])
        self.size = size

        self.camera = None

        pg.display.set_mode(self.size, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption(name)
        self.ctx = mgl.create_context()

        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0

        self.Bro_Running = True

        self.shaders = {}

        vert_source = r"Flame3D\\shaders\\default.vert"
        frag_source = r"Flame3D\\shaders\\default.frag"

        self.load_shader("default", vert_source, frag_source)

    def set_camera(self, camera):
        self.camera = camera
    
    def loop(self):
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
    
    def update(self):
        self.handle_events()
        pg.display.flip()
        if not self.Bro_Running:
            pg.quit()
            sys.exit()
    
    def fill_color(self, color):
        self.ctx.clear(color[0]/255, color[1]/255, color[2]/255, 1.0)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.Bro_Running = False
    
    def load_shader(self, name, vert_path, frag_path):
        with open(vert_path, "r", encoding="utf-8") as f:
            vert_source = f.read()
        with open(frag_path, "r", encoding="utf-8") as f:
            frag_source = f.read()

        program = self.ctx.program(
            vertex_shader=vert_source,
            fragment_shader=frag_source
        )
        self.shaders[name] = program

        return program