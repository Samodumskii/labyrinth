from constants import *
from json_restorable_interface import JsonRestorable
import pygame
from random import choice


class Cell(JsonRestorable):
    """A class to represent cells."""
    def __init__(self, x, y):
        self.list_cells = []
        self.x, self.y = x, y
        self.visited = False
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.thickness = THICKNESS

    def draw(self, screen):
        """Drawing a cell on the screen."""
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(screen, pygame.Color((64, 64, 64)), (x, y, TILE, TILE))
        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color('orange'), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color('orange'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color('orange'), (x, y + TILE), (x, y), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color('orange'), (x + TILE, y + TILE), (x, y + TILE), 2)

    @staticmethod
    def check_cell(x, y, list_cells):
        """Check that a cell exists in the matrix."""
        if x < 0 or x > COLS - 1 or y < 0 or y > ROWS - 1:
            return False
        return list_cells[Cell.find_index(x, y)]

    @staticmethod
    def find_index(x, y):
        return x + y * COLS

    def get_rects(self):
        """Get the existing sides of the cell."""
        rects = []
        x, y = self.x * TILE, self.y * TILE
        if self.walls['top']:
            rects.append(pygame.Rect((x, y), (TILE, self.thickness)))
        if self.walls['right']:
            rects.append(pygame.Rect((x + TILE, y), (self.thickness, TILE)))
        if self.walls['bottom']:
            rects.append(pygame.Rect((x, y + TILE), (TILE, self.thickness)))
        if self.walls['left']:
            rects.append(pygame.Rect((x, y), (self.thickness, TILE)))
        return rects

    def check_neighbors(self, list_cells):
        """Checking whether neighboring cells exist.
            And returns a random neighboring cell."""
        self.list_cells = []
        neighbors = []
        top = Cell.check_cell(self.x, self.y - 1, list_cells)
        right = Cell.check_cell(self.x + 1, self.y, list_cells)
        bottom = Cell.check_cell(self.x, self.y + 1, list_cells)
        left = Cell.check_cell(self.x - 1, self.y, list_cells)
        for cell in (top, right, bottom, left):
            if cell:
                self.list_cells.append(cell)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False

    def to_json(self):
        list_cells_serialized = [[cell.x, cell.y, cell.walls] for cell in self.list_cells]

        return {
            'x': self.x,
            'y': self.y,
            'visited': self.visited,
            'walls': self.walls,
            'list_cells': list_cells_serialized,
        }

    def from_json(self, data, cell_map):
        self.x = data['x']
        self.y = data['y']
        self.visited = data.get('visited', False)
        self.walls = data['walls']
        self.thickness = data.get('thickness', THICKNESS)
        self.list_cells = []
        if 'list_cells' in data:
            for cell_info in data['list_cells']:
                x, y = cell_info[:2]
                if 0 <= x < len(cell_map[0]) and 0 <= y < len(cell_map):
                    self.list_cells.append(cell_map[y][x])

    def __eq__(self, other):
        if isinstance(other, Cell):
            if (self.x == other.x and self.y == other.y and self.walls == other.walls and
                    Cell.compare_list_cells(self.list_cells, other.list_cells)):
                return True
        return False

    @staticmethod
    def compare_list_cells(list1, list2):
        if len(list1) != len(list2):
            return False
        for cell_1, cell_2 in zip(list1, list2):
            if cell_1.x != cell_2.x or cell_1.y != cell_2.y or cell_1.walls != cell_2.walls:
                return False
        return True

    def __hash__(self):
        return hash((self.x, self.y))