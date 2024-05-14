import pytest
from labyrinth import generate_labyrinth


@pytest.fixture
def labyrinth():
    """Labyrinth generation."""
    return generate_labyrinth()


def test_generate_labyrinth(labyrinth):
    """Test of labyrinth generation."""
    new_labyrinth = generate_labyrinth()
    assert len(new_labyrinth) == len(labyrinth)
    assert len(new_labyrinth[0]) == len(labyrinth[0])
    for row in new_labyrinth:
        for cell in row:
            assert cell.visited


def test_player_can_reach_all_cells(labyrinth):
    """Test the reachability of all cells in the labyrinth"""
    start_cell = labyrinth[0][0]
    visited_cells = set()
    queue = [start_cell]
    # BFS checking the availability of all cells
    while queue:
        current_cell = queue.pop(0)
        visited_cells.add(current_cell)
        neighbors = current_cell.list_cells
        for neighbor in neighbors:
            if neighbor not in visited_cells and not (check_wall_between_cells(current_cell, neighbor)) and neighbor not in queue:
                queue.append(neighbor)
    assert len(visited_cells) == len(labyrinth[0]) * len(labyrinth)


def check_wall_between_cells(current_cell, next_cell):
    dx = current_cell.x - next_cell.x
    dy = current_cell.y - next_cell.y
    if dx == 1 and not (current_cell.walls['left'] or next_cell.walls['right']):
        return False
    elif dx == -1 and not (current_cell.walls['right'] or next_cell.walls['left']):
        return False
    elif dy == 1 and not (current_cell.walls['top'] or next_cell.walls['bottom']):
        return False
    elif dy == -1 and not (current_cell.walls['bottom'] or next_cell.walls['top']):
        return False
    else:
        return True
