class Reward:
    @classmethod
    def from_json(cls, reward_dict):
        id_num = reward_dict['_id']
        relicName = reward_dict['itemName']
        chance = float(reward_dict['chance']) / 100 #Conversion necessary to convert into percent
        rarity = reward_dict['rarity']
        return cls(id_num, relicName, chance, rarity)
    def __init__(self, id_num, relicName, chance, rarity):
        self.id = id_num
        self.relicName = relicName
        self.chance = chance
        self.rarity = rarity
    
    def __eq__(self, other):
        if not isinstance(other, Reward):
            return False
        else:
            return self.id == other.id
    def get_name(self):
        return self.relicName
    def get_chance(self):
        return self.chance
    def __hash__(self):
        return int(self.id, 16)
