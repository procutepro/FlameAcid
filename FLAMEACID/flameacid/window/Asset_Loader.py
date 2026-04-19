import pygame as pg
from FLAMEACID.flameacid.window.utils import *
import json

def load_spritesheet(path=None, surface=None, frame_width=None, frame_height=None):
    Sheet = surface if path is None else load(path)
    Frames = []
    Sheet_W, Sheet_H = Sheet.get_size()

    for y in range(0, Sheet_H, frame_height):
        for x in range(0, Sheet_W, frame_width):
            Rect = pg.Rect(x, y, frame_width, frame_height)
            Frames.append(Sheet.subsurface(Rect).copy())

    return Frames

class AssetManager:

    def __init__(self, asset_json):
        self.Asset_Json = asset_json
        self.Assets = {}

    def load_assets(self):
        with open(self.Asset_Json) as f:
            Data = json.load(f)

        Sheet = load(Data["target"])

        for Texture in Data["textures"]:
            Type_Of_Data = Texture["type"]

            if Type_Of_Data == "tile":
                Name = Texture["name"]
                x, y = Texture["pos"]
                w, h = Texture["size"]
                Rect = pg.Rect(x, y, w, h)
                self.Assets[Name] = Sheet.subsurface(Rect).copy()

            elif Type_Of_Data == "spritesheet":
                Name = Texture["name"]
                x, y = Texture["pos"]
                w, h = Texture["size"]
                Frame_Width, Frame_Height = Texture["frame_size"]
                Rect = pg.Rect(x, y, w, h)
                Frame = Sheet.subsurface(Rect).copy()
                self.Assets[Name] = load_spritesheet(surface=Frame, frame_width=Frame_Width, frame_height=Frame_Height)

    def get_asset(self, name):
        return self.Assets[name]

    def add_asset(self, name, value):
        self.Assets[name] = value