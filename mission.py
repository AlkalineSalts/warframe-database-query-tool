import json
from reward import Reward
def _form_list_of_rewards(rewards_json_list):
        return {Reward(idv_reward_json) for idv_reward_json in rewards_json_list}
class Mission:
        def __init__(self, name, mission_dict):
                self.name = name
                self.gameMode = mission_dict['gameMode']
                self.isEvent = mission_dict['isEvent']

                #This is a list of rewards, with each index representing the rewards recieved per full 'round'
                #For example, in a sabotage mission, which has only one set of rewards,
                #This has one list which contains another list of rewards
                #If this is something like defense, then it has three lists,
                #each of which contain a list of rewards per rotation 
                
                self.hasRotations = type(mission_dict['rewards']) is dict
                if (self.hasRotations):
                        r_dict = mission_dict['rewards']
                        self.list_of_rewards_list = []
                        self.list_of_rewards_list.append(_form_list_of_rewards(r_dict['A']))
                        self.list_of_rewards_list.append(_form_list_of_rewards(r_dict['B']))
                        self.list_of_rewards_list.append(_form_list_of_rewards(r_dict['C']))

                else:
                        r_list = mission_dict['rewards']
                        self.list_of_rewards_list = [_form_list_of_rewards(r_list)]
        def get_name(self):
                return self.name
        def get_game_mode(self):
                return self.gameMode
        def has_rotations(self):
                return self.hasRotations

        def get_rewards(self):
                if (self.hasRotations):
                        yield self.list_of_rewards_list[0]
                        yield self.list_of_rewards_list[1]
                        yield self.list_of_rewards_list[2]
                else:
                        yield self.list_of_rewards_list[0]
                        
        
