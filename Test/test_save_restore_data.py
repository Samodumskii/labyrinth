from random import randrange
import pytest
from game_utils import *
import os

os.chdir('/Users/samodumskii/PycharmProjects/Labirint/')


@pytest.fixture
def game_instance(monkeypatch):
    """Creating object date classes for gameplay"""

    def mock_character_init(self):
        self.speed = SPEED
        self._keys = ["0"]
        self.directions = {'left': (-self.speed, 0), 'right': (self.speed, 0), 'up': (0, -self.speed),
                           'down': (0, self.speed)}
        self.coord_center = [TILE // 2, TILE // 2]
        self._direction = (0, 0)

    def mock_subject_init(self):
        self.coord = [0, 0]
        self.set_pos()

    def mock_set_pos(self, coord=None):
        if coord is None:
            rand_coord = [randrange(COLS) * TILE + 5, randrange(ROWS) * TILE + 5]
            if rand_coord in Subject.coord_subject:
                self.set_pos()
            else:
                self.coord = rand_coord
                Subject.coord_subject.append(self.coord)
        else:
            self.coord = coord

    def mock_door_from_json(self, color, coord):
        self.color = color
        self.set_pos(coord)

    def mock_character_from_json(self, data):
        self._keys = data['keys']
        self.coord_center = data['rect']

    monkeypatch.setattr("character.Character.__init__", mock_character_init)
    monkeypatch.setattr("character.Character.from_json", mock_character_from_json)
    monkeypatch.setattr("subject.Subject.__init__", mock_subject_init)
    monkeypatch.setattr("subject.Subject.set_pos", mock_set_pos)
    monkeypatch.setattr("door.Door.from_json", mock_door_from_json)
    return create_game()


@pytest.fixture
def temp_save_file():
    filename = "save_game.json"
    yield filename
    if os.path.exists(filename):
        os.remove(filename)


def test_save_game(game_instance, temp_save_file):
    """Test saving a game data"""
    game_instance_to_json = {'labyrinth': save_labyrinth(game_instance.labyrinth),
                             'Key': helper_save_game(game_instance.key_list),
                             'Door': helper_save_game(game_instance.door_list),
                             'Character': game_instance.character.to_json(), 'Time': game_instance.time,
                             'Puddle': helper_save_game(game_instance.puddle_list)}
    save_game(game_instance)
    assert os.path.exists(temp_save_file)
    with open(temp_save_file, "r") as file:
        saved_data = json.load(file)
        assert saved_data == game_instance_to_json


def test_save_and_restore(game_instance):
    """Test saving and restoring a game data"""
    save_game(game_instance)
    # Change variables for second_instance
    second_instance = create_game()
    second_instance.key_list.pop()
    second_instance.time = 10
    second_instance.character.coord_center = (150, 160)
    # restore first instance
    restore_game(second_instance)
    assert second_instance == game_instance
