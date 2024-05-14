from constants import *
from cell import Cell


def restore_labyrinth(data):
    """Restoring a labyrinth from JSON."""
    rows, cols = len(data), len(data[0])
    cell_map = [[Cell(0, 0) for _ in range(cols)] for _ in range(rows)]
    for y in range(rows):
        for x in range(cols):
            cell_data = data[y][x]
            cell_map[y][x].from_json(cell_data, cell_map)
    return cell_map


def remove_walls(current, next):
    """Removal of walls between neighboring cells."""
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False


def generate_labyrinth():
    """Labyrinth generation."""
    list_cells = [[Cell(col, row) for col in range(COLS)] for row in range(ROWS)]
    current_cell = list_cells[0][0]
    stack = []
    break_count = 1
    while break_count < ROWS * COLS:
        current_cell.visited = True
        next_cell = current_cell.check_neighbors([cell for row in list_cells for cell in row])
        if next_cell:
            next_cell.visited = True
            break_count += 1
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
    return list_cells


def save_labyrinth(labyrinth):
    """Saving the labyrinth."""
    return [[cell.to_json() for cell in row] for row in labyrinth]
