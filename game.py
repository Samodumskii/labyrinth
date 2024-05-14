from dataclasses import dataclass
from character import Character
from door import Door
from key import Key
from puddle import Puddle


@dataclass
class Game:
    time: int
    labyrinth: list
    character: Character
    key_list: list[Key]
    door_list: list[Door]
    walls_collide_list: list
    puddle_list: list[Puddle]

    def __eq__(self, other):
        if isinstance(other, Game):
            if self.time == other.time and self.character == other.character:
                if Game.compare_lists(self.key_list, other.key_list, lambda x: (x.coord, x.color)):
                    if Game.compare_lists(self.door_list, other.door_list, lambda x: (x.coord, x.color)):
                        if Game.compare_lists(self.puddle_list, other.puddle_list, lambda x: (x.coord)):
                            if Game.compare_labyrinth(self.labyrinth, other.labyrinth):
                                return True
        return False

    @staticmethod
    def compare_lists(subject_list, other_subject_list, func):
        list1 = sorted(subject_list, key=func)
        list2 = sorted(other_subject_list, key=func)
        # Check the length of lists
        if len(list1) != len(list2):
            return False
        # Comparing each object in the lists
        for item1, item2 in zip(list1, list2):
            if item1 != item2:
                return False
        return True

    @staticmethod
    def compare_labyrinth(list1, list2):
        if len(list1) != len(list2) or len(list1[1]) != len(list2[1]):
            return False
        for y in range(len(list1)):
            for x in range(len(list1[y])):
                if list1[y][x] != list2[y][x]:
                    return False
        return True

