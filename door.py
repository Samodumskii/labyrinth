import pygame

from json_restorable_interface import JsonRestorable
from subject import Subject
from constants import *


class Door(Subject, JsonRestorable):
    """A class to represent doors."""
    def __init__(self):
        super().__init__()
        self.color = COLOR_DICT[Door.count]
        if Door.count == MAX_COUNT:
            Door.count = 0
        else:
            Door.count += 1

    def set_path_icon(self):
        """Setting the path to an icon"""
        return f'img/door_{COLOR_DICT[Door.count]}.png'

    def to_json(self):
        return {'color': self.color,
                'coord': self.coord
                }

    def from_json(self, color, coord):
        self.color = color
        self.img = pygame.image.load(f'img/door_{self.color}.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
        self.set_pos(coord)

    def __eq__(self, other):
        if isinstance(other, Door):
            return self.color == other.color and self.coord == other.coord
        return False
