import pygame

from json_restorable_interface import JsonRestorable
from subject import Subject
from pygame import draw
from constants import *


class Key(Subject, JsonRestorable):
    """A class to represent keys."""
    def __init__(self):
        super().__init__()
        self.color = COLOR_DICT[Key.count]
        if Key.count == MAX_COUNT:
            Key.count = 0
        else:
            Key.count += 1

    def set_path_icon(self):
        """Setting the path to an icon"""
        return f'img/key.png'

    def draw(self, game_surface):
        draw.rect(game_surface, self.color, self.rect)
        super().draw(game_surface)

    def to_json(self):
        return {'color': self.color,
                'coord': self.coord
                }

    def from_json(self, color, coord):
        self.color = color
        self.set_pos(coord)

    def __eq__(self, other):
        if isinstance(other, Key):
            return self.color == other.color and self.coord == other.coord
        return False

    def __hash__(self):
        return hash((self.color, self.coord))