from FLAMEACID.flameacid.window.core import *
import math as m

class Grid:

    def __init__(self, start_pos, end_pos, rows, columns, screen: Window):
        self.Start_Pos = list(start_pos)
        self.Start_Draw_Pos = list(start_pos)
        self.End_Pos = list(end_pos)
        self.End_Draw_Pos = list(end_pos)
        self.Rows = rows
        self.Columns = columns
        self.Screen = screen
        self.ecs_components = {}
        self.ecs_valubles = {}

        self.Size_Of_Tiles = [
            (self.End_Pos[0] - self.Start_Pos[0]) / self.Rows,
            (self.End_Pos[1] - self.Start_Pos[1]) / self.Columns
        ]

        self.Grid_Data = []

        for r in range(rows):
            Row = []
            for c in range(columns):
                Row.append(0)
            self.Grid_Data.append(Row)

    def draw_at(self, grid_coord, thing):
        self.Grid_Data[grid_coord[0]][grid_coord[1]] = thing

    def draw(self):
        for i in range(self.Rows):
            for j in range(self.Columns):
                if self.Grid_Data[i][j] != 0:
                    Tile = self.Grid_Data[i][j]
                    Pos = [
                        self.Start_Draw_Pos[0] + i * self.Size_Of_Tiles[0],
                        self.Start_Draw_Pos[1] + j * self.Size_Of_Tiles[1]
                    ]
                    Tile.Pos = Pos
                    Tile.Size = self.Size_Of_Tiles
                    Tile.draw(self.Screen)

    def move(self, delta):
        self.Start_Pos[0] += delta[0]
        self.Start_Pos[1] += delta[1]
        self.Start_Draw_Pos[0] += delta[0]
        self.Start_Draw_Pos[1] += delta[1]
        self.End_Pos[0] += delta[0]
        self.End_Pos[1] += delta[1]
        self.End_Draw_Pos[0] += delta[0]
        self.End_Draw_Pos[1] += delta[1]
    
    def attach_component(self, type_of_component, name, value):
        if type_of_component.lower() == "val":
            self.ecs_valubles[name] = value
        if type_of_component.lower() == "func":
            self.ecs_components[name] = value

    def run_ecs(self, function, *args):
        func = self.ecs_components[function]
        func(self, *args)


class Sprite:

    def __init__(self, image_path, pos, size, rotation, screen: Window):
        self.Image = image_path
        self.Pos = list(pos)
        self.Size = size
        self.Rotation = rotation
        self.ecs_components = {}
        self.ecs_valubles = {}
        self.screen = screen

    def draw(self, window):
        self.screen.make_image(self.Pos, self.Size, self.Rotation, self.Image)

    def move(self, delta):
        self.Pos[0] += delta[0]
        self.Pos[1] += delta[1]

    def change_image(self, img):
        self.Image = img
    
    def attach_component(self, type_of_component, name, value):
        if type_of_component.lower() == "val":
            self.ecs_valubles[name] = value
        if type_of_component.lower() == "func":
            self.ecs_components[name] = value

    def run_ecs(self, function, *args):
        func = self.ecs_components[function]
        func(self, *args)


class AnimatedSprite:

    def __init__(self, pos, size, surfaces, frame_duration, screen: Window):
        self.Surfaces = surfaces
        self.Frame_Duration = frame_duration
        self.Frame = 0
        self.Screen = screen
        self.Pos = pos
        self.ecs_components = {}
        self.ecs_valubles = {}
        self.Size = self.Surfaces[0].get_size() if size == "normal" else size

    def move(self, delta):
        self.Pos = (self.Pos[0] + delta[0], self.Pos[1] + delta[1])

    def update(self, dt):
        self.Frame = (self.Frame + dt * self.Frame_Duration) % len(self.Surfaces)

    def draw(self):
        Current_Frame = self.Surfaces[m.floor(self.Frame)]
        self.Screen.direct_draw(self.Pos, self.Size, Current_Frame)

    def attach_component(self, type_of_component, name, value):
        if type_of_component.lower() == "val":
            self.ecs_valubles[name] = value
        if type_of_component.lower() == "func":
            self.ecs_components[name] = value

    def run_ecs(self, function, *args):
        func = self.ecs_components[function]
        func(self, *args)

class FrogObject:
    def __init__(self, pos, rot, size):
        self.pos, self.size, self.rot = pos, size, rot
        self.ecs_components = {}
        self.ecs_valubles = {}

    def attach_component(self, type_of_component, name, value):
        if type_of_component.lower() == "val":
            self.ecs_valubles[name] = value
        if type_of_component.lower() == "func":
            self.ecs_components[name] = value

    def run_ecs(self, function, *args):
        func = self.ecs_components[function]
        func(self, *args)

class Keyframes:

    def __init__(self, keyframes: dict):
        self.Keyframes = keyframes
        self.Times = sorted(keyframes.keys())
        self.Elapsed_Time = 0.0
        self.Finished = False

    def lerp(self, a, b, t):
        """
        Linearly interpolate between two tuples of any size.
        - a: start tuple (e.g., (0,0) or (0,0,0) or (0,0,0,0))
        - b: end tuple (same length as a)
        - t: interpolation factor (0.0 to 1.0)
        Returns a tuple of the same length.
        """
        if not isinstance(a, tuple) or not isinstance(b, tuple):
            # Fallback for numbers
            return a + (b - a) * t

        # Works for tuples of ANY length
        return tuple(ai + (bi - ai) * t for ai, bi in zip(a, b))

    def lerp_number(self, a, b, t):
        return a + (b - a) * t

    def find_segment(self):
        if self.Elapsed_Time <= self.Times[0]:
            return self.Times[0], self.Times[0]

        for i in range(1, len(self.Times)):
            if self.Elapsed_Time < self.Times[i]:
                return self.Times[i - 1], self.Times[i]

        return self.Times[-1], self.Times[-1]

    def update(self, obj, deltu_tumo, ease=lambda t: t):
        if self.Finished:
            return

        self.Elapsed_Time += deltu_tumo

        Start_Time, End_Time = self.find_segment()

        Start_Pose = self.Keyframes[Start_Time]
        End_Pose = self.Keyframes[End_Time]

        if Start_Time == End_Time:
            obj.Pos, obj.Size, obj.Rotation = Start_Pose
            self.Finished = True
            return

        Segment_Length = End_Time - Start_Time
        t = (self.Elapsed_Time - Start_Time) / Segment_Length
        t = ease(max(0, min(1, t)))

        Start_Pos, Start_Scale, Start_Rot = Start_Pose
        End_Pos, End_Scale, End_Rot = End_Pose

        obj.Pos = self.lerp(Start_Pos, End_Pos, t)
        obj.Rotation = self.lerp_number(Start_Rot, End_Rot, t)
        obj.Size = self.lerp(Start_Scale, End_Scale, t)

        if t == 1:
            self.Elapsed_Time = 0.0
            self.Finished = True