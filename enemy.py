from reward import Reward
#Should be built with builder
class Enemy:
    def __init__(self, resource_drop_chance:int, resources:set, mod_drop_chance:int, mods:list, id_num, name):
        self.resource_drop_chance = resource_drop_chance
        self.resources = resources
        self.mod_drop_chance = mod_drop_chance
        self.mods = mods
        self.id = id_num
        self.name = name
    def get_resource_drop_chance(self):
        return self.resource_drop_chance
    def get_mod_drop_chance(self):
        return self.mod_drop_chance
    def get_resource_drops(self):
        return self.resources
    def get_mod_drops(self):
        return self.mods
    def get_name(self):
        return self.name
    def __hash__(self):
        return int(self.id, 16)
    def __eq__(self, other):
        if not isinstance(other, Reward):
            return False
        else:
            return self.id == other.id
    def __lt__(self, other):
        return __lt__(self.name, other.name)

class EnemyBuilder:
    def __init__(self, id_num):
        self.resource_drop_chance = 0
        self.mod_drop_chance = 0
        self.resources = set()
        self.mods = set()
        self.id = id_num
        self.name = None
    def add_resource(self, resource:Reward):
        self.resources.add(resource)
    def set_name(self, name):
        self.name = name
    def add_mod(self, mod:Reward):
        self.mods.add(mod)
    def set_mod_chance(self, mod_percent):
        self.mod_drop_chance = mod_percent
    def set_resource_chance(self, resource_percent):
        self.resource_drop_chance = resource_percent
    def __hash__(self):
        return int(self.id, 16)
    def __eq__(self, other):
        if not isinstance(other, Reward):
            return False
        else:
            return self.id == other.id
    def __eq__(self, other):
        if not isinstance(other, Reward):
            return False
        else:
            return self.id == other.id
    def build(self):
        return Enemy(self.resource_drop_chance, self.resources, self.mod_drop_chance, self.mods, self.id, self.name)
    
