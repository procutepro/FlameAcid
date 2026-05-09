# acid/__init__.py

import random

messages = [
    "Hi from pratyush the idiot",
    "Frogs are watching you code",
    "If it crashes, it's a feature",
    "You are using a engine most people dispise",
    "You need to have a brain to not use this engine",
    "i will torture my code until it dies or works",
    "bob the cube will fix your depression"
]

print(random.choice(messages))

"""
ACID Engine - Game engine for Morons.
"""

__version__ = "0.1.1-frog-edition"
__author__ = "Pratyush Wani"
__license__ = "MIT"

from FLAMEACID.flameacid.window.core import Window

from FLAMEACID.flameacid.Flame3D.window import *

from FLAMEACID.flameacid.window.utils import (
    get_mouse_pos,
    has_clicked,
    has_pressed,
    has_just_pressed,
    triangulate_polygon,
    is_convex_polygon,
    line_points,
    fill_triangle,
    color_swap,
    load
)

from FLAMEACID.flameacid.window.sprites_and_objects import (
    Sprite,
    AnimatedSprite,
    Grid,
    FrogObject,
    Keyframes
)

from FLAMEACID.flameacid.window.software_renderer_lol import AcidImage

from FLAMEACID.flameacid.window.Asset_Loader import (
    load_spritesheet,
    AssetManager,
)