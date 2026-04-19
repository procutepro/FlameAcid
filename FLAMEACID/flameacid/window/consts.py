import pygame as pg

TEMPLATE_VERTEX_SHADER = """
#version 330
in vec3 position;
void main() {
    gl_Position = vec4(position, 1.0);
}
"""

TEMPLATE_FRAGMENT_SHADER = """
#version 330
out vec4 outColor;
uniform vec3 uColor;
void main() {
    outColor = vec4(uColor, 1.0);
}
"""

COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "gray": (128, 128, 128),
    "orange": (255, 165, 0),
    "pink": (255, 142, 203),
    "purple": (128, 0, 128),
    "brown": (165, 42, 42),
    "lime": (0, 255, 0),
    "navy": (0, 0, 128),
    "teal": (0, 128, 128),
    "olive": (128, 128, 0),
    "maroon": (128, 0, 0),
    "silver": (192, 192, 192),
}

COLORS_LIST = list(COLORS.keys())

KEY_MAPPING = {
    # Letters
    "a": pg.K_a, "b": pg.K_b, "c": pg.K_c, "d": pg.K_d, "e": pg.K_e,
    "f": pg.K_f, "g": pg.K_g, "h": pg.K_h, "i": pg.K_i, "j": pg.K_j,
    "k": pg.K_k, "l": pg.K_l, "m": pg.K_m, "n": pg.K_n, "o": pg.K_o,
    "p": pg.K_p, "q": pg.K_q, "r": pg.K_r, "s": pg.K_s, "t": pg.K_t,
    "u": pg.K_u, "v": pg.K_v, "w": pg.K_w, "x": pg.K_x, "y": pg.K_y, "z": pg.K_z,

    # Numbers
    "0": pg.K_0, "1": pg.K_1, "2": pg.K_2, "3": pg.K_3, "4": pg.K_4,
    "5": pg.K_5, "6": pg.K_6, "7": pg.K_7, "8": pg.K_8, "9": pg.K_9,

    # Arrows
    "up": pg.K_UP, "down": pg.K_DOWN, "left": pg.K_LEFT, "right": pg.K_RIGHT,

    # Common keys
    "space": pg.K_SPACE, "enter": pg.K_RETURN, "esc": pg.K_ESCAPE,
    "tab": pg.K_TAB, "shift": pg.K_LSHIFT, "ctrl": pg.K_LCTRL, "alt": pg.K_LALT,
    "backspace": pg.K_BACKSPACE, "capslock": pg.K_CAPSLOCK, "delete": pg.K_DELETE,
    "home": pg.K_HOME, "end": pg.K_END, "pageup": pg.K_PAGEUP, "pagedown": pg.K_PAGEDOWN,
    "insert": pg.K_INSERT, "printscreen": pg.K_PRINT, "pause": pg.K_PAUSE,

    # Function keys
    "f1": pg.K_F1, "f2": pg.K_F2, "f3": pg.K_F3, "f4": pg.K_F4, "f5": pg.K_F5,
    "f6": pg.K_F6, "f7": pg.K_F7, "f8": pg.K_F8, "f9": pg.K_F9, "f10": pg.K_F10,
    "f11": pg.K_F11, "f12": pg.K_F12,

    # Numpad
    "[0]": pg.K_KP0, "[1]": pg.K_KP1, "[2]": pg.K_KP2, "[3]": pg.K_KP3, "[4]": pg.K_KP4,
    "[5]": pg.K_KP5, "[6]": pg.K_KP6, "[7]": pg.K_KP7, "[8]": pg.K_KP8, "[9]": pg.K_KP9,
    "[.]": pg.K_KP_PERIOD, "[/]": pg.K_KP_DIVIDE, "[*]": pg.K_KP_MULTIPLY,
    "[-]": pg.K_KP_MINUS, "[+]": pg.K_KP_PLUS, "[enter]": pg.K_KP_ENTER,
    "[equals]": pg.K_KP_EQUALS,

    # Symbols
    "minus": pg.K_MINUS, "equals": pg.K_EQUALS, "leftbracket": pg.K_LEFTBRACKET,
    "rightbracket": pg.K_RIGHTBRACKET, "backslash": pg.K_BACKSLASH, "semicolon": pg.K_SEMICOLON,
    "quote": pg.K_QUOTE, "comma": pg.K_COMMA, "period": pg.K_PERIOD, "slash": pg.K_SLASH,
    "grave": pg.K_BACKQUOTE,

    # Modifiers
    "lshift": pg.K_LSHIFT, "rshift": pg.K_RSHIFT, "lctrl": pg.K_LCTRL, "rctrl": pg.K_RCTRL,
    "lalt": pg.K_LALT, "ralt": pg.K_RALT, "lsuper": pg.K_LSUPER, "rsuper": pg.K_RSUPER,
}