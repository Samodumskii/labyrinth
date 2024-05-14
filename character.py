from json_restorable_interface import JsonRestorable
import pygame
from constants import *


class Character(JsonRestorable):
    """A class to represent a character."""
    def __init__(self):
        self.speed = SPEED
        self._keys = ["0"]
        self.directions = {'left': (-self.speed, 0), 'right': (self.speed, 0), 'up': (0, -self.speed),
                           'down': (0, self.speed)}
        self.img = pygame.image.load('img/character.png').convert_alpha()
        self.img = pygame.transform.scale(self.img,
                                          (TILE - 2 * THICKNESS, TILE - 2 * THICKNESS))
        self.rect = self.img.get_rect()
        self.coord_center = [TILE // 2, TILE // 2]
        self.rect.center = self.coord_center
        self._direction = (0, 0)

    def move(self):
        """Moving a character"""
        self.rect.move_ip(self.direction)
        self.coord_center = [x + y for x, y in zip(self.rect.center, self.direction)]

    def draw(self, game_surface):
        """Drawing a character on the screen"""
        game_surface.blit(self.img, self.rect)

    def take_key(self, key_list):
        """Get a key"""
        for key in key_list:
            if self.rect.collidepoint(key.rect.center):
                self.keys = key.color
                key_list.remove(key)

    def is_colliding(self, x, y, walls_collide_list):
        """Handling collisions with walls"""
        tmp_rect = self.rect.move(x, y)
        if tmp_rect.collidelist(walls_collide_list) == -1:
            return False
        return True

    @property
    def direction(self):
        """Direction of movement"""
        return self._direction

    @direction.setter
    def direction(self, direction):
        if direction in self.directions.values():
            self._direction = direction

    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, key):
        if self._keys == ["0"]:
            self._keys.pop()
        self._keys.append(key)

    def to_json(self):
        return {
            'keys': self._keys,
            'rect': self.coord_center,
        }

    def from_json(self, data):
        self._keys = data['keys']
        self.coord_center = data['rect']
        self.rect.center = self.coord_center

    def __eq__(self, other):
        if isinstance(other, Character):
            return self._keys == other._keys and self.coord_center == other.coord_center
        return False
