import json
from mission import Mission
class Planet:
    def __init__(self, name, missions_dict):
        self.name = name
        self.missions = {}
        for mission_name in missions_dict.keys():
            self.missions[mission_name] = Mission(mission_name, missions_dict[mission_name])

    def get_name(self):
        return self.name
    def get_mission(self, mission_name):
        return self.missions[mission_name]
    def get_mission_name_generator(self):
        for name in self.missions.keys():
            yield name
    def __str__(self):
        return self.get_name()
    def __repr__(self):
        return self.__str__()
