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
        with open(self.Asset_Json) as f:
            self.Data = json.load(f)

        self.Sheet = load(self.Data["target"])
        self.name_to_dict = {}

        for Texture in self.Data["textures"]:
            Name = Texture["name"]
            self.name_to_dict[Name] = Texture

    def _collect_data_(self, Texture):
        Type_Of_Data = Texture["type"]
        Asset = {}

        if Type_Of_Data == "tile":
            Name = Texture["name"]
            x, y = Texture["pos"]
            w, h = Texture["size"]
            Rect = pg.Rect(x, y, w, h)
            Asset[Name] = self.Sheet.subsurface(Rect).copy()

        elif Type_Of_Data == "spritesheet":
            Name = Texture["name"]
            x, y = Texture["pos"]
            w, h = Texture["size"]
            Frame_Width, Frame_Height = Texture["frame_size"]
            Rect = pg.Rect(x, y, w, h)
            Frame = self.Sheet.subsurface(Rect).copy()
            Asset[Name] = load_spritesheet(surface=Frame, frame_width=Frame_Width, frame_height=Frame_Height)
        
        return Asset

    def load_assets(self):
        """
        Loads EVERYTHING
        """
        for Texture in self.Data["textures"]:
            self.Assets.update(self._collect_data_(Texture))

    def get_asset(self, name):
        return self.Assets[name]
    
    def open_asset(self, name):
        """
        Loads smths
        """
        return self._collect_data_(self.name_to_dict[name])

    def add_asset(self, name, value):
        self.Assets[name] = value