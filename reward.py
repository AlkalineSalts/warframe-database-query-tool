class Reward:
    def __init__(self, reward_dict):
        self.id = reward_dict['_id']
        self.relicName = reward_dict['itemName']
        self.chance = float(reward_dict['chance']) / 100 #Conversion necessary to convert into percent
        self.rarity = reward_dict['rarity']
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
