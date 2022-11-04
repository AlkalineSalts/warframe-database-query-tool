from enum import Enum
import json
from reward import Reward


   
class Relic:
    def __init__(self, json_dict):
        self.tier = json_dict['tier']
        self.relicName = json_dict['relicName']
        self.state = json_dict['state']
        self.rewards = [Reward(reward_json) for reward_json in json_dict['rewards']]

    #Generator for the rewards attached to a relic
    def get_reward_generator(self):
        for reward in self.rewards:
            yield reward
    def get_tier(self):
        return self.tier

    def get_state(self):
        return self.state
    
    def __str__(self):
        return "{} {} Relic".format(self.tier, self.relicName)
    def __repr__(self):
        return self.__str__()
