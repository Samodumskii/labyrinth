import pygame

from json_restorable_interface import JsonRestorable
from subject import Subject
from constants import *


class Puddle(Subject, JsonRestorable):
    """A class to represent puddles."""
    def __init__(self):
        super().__init__()

    def set_path_icon(self):
        """Setting the path to an icon"""
        return f'img/puddle.png'

    def to_json(self):
        return {'coord': self.coord}

    def from_json(self, coord):
        self.set_pos(coord)

    def __eq__(self, other):
        if isinstance(other, Puddle):
            return self.coord == other.coord
        return False
