from character import Character
from puddle import Puddle
from subject import Subject
from door import Door
from game import Game
from key import Key
from labyrinth import *
import json


def collide_door(game):
    """Handling the character's collision with doors"""
    for door in game.door_list:
        if game.character.rect.collidepoint(door.rect.center) and door.color in game.character.keys:
            return True
    return False


def collide_puddle(game):
    """Handling the character's collision with puddles"""
    for puddle in game.puddle_list:
        if game.character.rect.collidepoint(puddle.rect.center):
            pygame.time.wait(30)


def is_game_over(game):
    """End-of-game handling"""
    if game.time < 0:
        pygame.time.wait(700)
        return True
    return False


def create_game():
    """Creating object date classes for gameplay"""
    # get labyrinth
    labyrinth = generate_labyrinth()
    Subject.coord_subject = [[5, 5]]
    Key.count = 0
    Door.count = 0
    # Subjects and character settings
    character = Character()
    key_list = [Key() for i in range(3)]
    door_list = [Door() for i in range(3)]
    puddle_list = [Puddle() for i in range(2)]

    # collision list
    walls_collide_list = sum([cell.get_rects() for row in labyrinth for cell in row], [])
    game = Game(TIME, labyrinth, character, key_list, door_list, walls_collide_list, puddle_list)
    return game


def restore_game(game):
    """Restore object date classes for gameplay from JSON file."""
    try:
        with open("save_game.json", "r") as file:
            info = json.load(file)
            game.key_list = restore_game_component(info['Key'], game.key_list, type(Key()))
            game.door_list = restore_game_component(info['Door'], game.door_list, type(Door()))
            game.puddle_list = restore_game_component(info['Puddle'], game.puddle_list, type(Puddle()))
            game.labyrinth = restore_labyrinth(info['labyrinth'])
            game.walls_collide_list = sum([cell.get_rects() for row in game.labyrinth for cell in row], [])
            game.character.from_json(info['Character'])
            game.time = info['Time']
    except FileNotFoundError:
        print("You haven't saved the game yet")


def restore_game_component(list_info, list_obj, class_obj):
    """Restore component for object date classes."""
    list_restore_obj = []
    while list_info:
        info = list_info.pop()
        if list_obj:
            obj = list_obj.pop()
        else:
            obj = class_obj()
        obj.from_json(**info)
        list_restore_obj.append(obj)
    return list_restore_obj


def save_game(game):
    """Saving data to a JSON file"""
    info_labyrinth = save_labyrinth(game.labyrinth)
    info = {'labyrinth': info_labyrinth, 'Key': helper_save_game(game.key_list),
            'Door': helper_save_game(game.door_list),
            'Character': game.character.to_json(), 'Time': game.time, 'Puddle': helper_save_game(game.puddle_list)}
    with open("save_game.json", "w") as file:
        json.dump(info, file)


def helper_save_game(items):
    """Saving data to a JSON format"""
    info_items = []
    for item in items:
        info_items.append(item.to_json())
    return info_items
