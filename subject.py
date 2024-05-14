from abc import ABC, abstractmethod
import pygame
from random import randrange
from constants import *


class Subject(ABC):
    count = 0
    coord_subject = []

    def __init__(self):
        self.img = pygame.image.load(self.set_path_icon()).convert_alpha()
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
        self.rect = self.img.get_rect()
        self.coord = (0, 0)
        self.set_pos()

    @abstractmethod
    def set_path_icon(self):
        raise NotImplementedError("The set_path_icon method must be implemented in subclasses.")

    def set_pos(self, coord=None):
        """Setting an object on the screen"""
        if coord is None:
            rand_coord = [randrange(COLS) * TILE + 5, randrange(ROWS) * TILE + 5]
            if rand_coord in Subject.coord_subject:
                self.set_pos()
            else:
                self.coord = rand_coord
                self.rect.topleft = self.coord
                Subject.coord_subject.append(self.coord)
        else:
            self.coord = coord
            self.rect.topleft = self.coord

    def draw(self, game_surface):
        """Drawing an object on the screen"""
        game_surface.blit(self.img, self.rect)
