import json
import DataGetter
import sys
import os
from planet import Planet
from mission import Mission
from relic import Relic
from enemy import EnemyBuilder
from enemy import Enemy
from reward import Reward
#Converts json representation of warframe data into prolog facts and rules.

GLOBAL_FILE_PATH = ""
#converts string to prolog valid string
def convert_to_prolog_str(p_string):
    return p_string.strip().replace("'", "\\'")
def save_file(file_name, generator):
    file = open(file_name, "w+")
    for save_string in generator:
        file.write(save_string)
    file.close()
    
#Creates a list of relics from the given dict
def createAllRelics(fullJson):
    relics_dict_list = fullJson['relics']
    relics_list = []
    for relic_json in relics_dict_list:
        relic = Relic(relic_json)
        relics_list.append(relic)
    return relics_list
    
def saveRelicsToPrologFile(relics_list, save_name = "relic_drops.pl"):
    save_location = os.path.join(GLOBAL_FILE_PATH, save_name)
    def temp():
        for relic in relics_list:
            rewards_generator = relic.get_reward_generator()
            for reward in rewards_generator:
                prolog_fact = "relic_drops(\"{}\", \"{}\", {}).\n".format(convert_to_prolog_str(str(relic)), convert_to_prolog_str(reward.get_name()), reward.get_chance())
                yield prolog_fact
        #Create rule for dealing with relics strings that don't have state in them
        yield '% Rule for dealing with relic strs that don\'t include their state\n'
        yield 'relic_drops(NAME, ITEM, CHANCE) :- (var(NAME) -> fail; (relic_drops_help(NAME, ITEM, CHANCE))).\n'
        yield 'relic_drops_help(NAME, ITEM, CHANCE) :- (string_concat(_, ")", NAME) -> fail; (relic_drops(RELIC, ITEM, CHANCE), string_concat(NAME, " (Intact)", RELIC))).\n'
    save_file(save_location, temp())

def createAllPlanets(fullJson):
    planets_dict = fullJson['missionRewards']
    planets = []
    for p_name in planets_dict.keys():
        new_planet = Planet(p_name, planets_dict[p_name])
        planets.append(new_planet)
    return planets
def createAllMissions(planet_list):
    mission_list = []
    for planet in planet_list:
        g = planet.get_mission_name_generator()
        for mission_name in g:
            mission = planet.get_mission(mission_name)
            mission_list.append(mission)        
    
    return mission_list

def addTransientMissions(mission_list, transient_json):
    for place in transient_json:
        obj_name = place['objectiveName']
        mission = Mission(obj_name, place)
        mission_list.append(mission)
    

def savePlanetMissionRelationToPrologFile(planet_list, save_name = "planet_mission.pl"):
    save_location = os.path.join(GLOBAL_FILE_PATH, save_name)
    def temp():
        for planet in planet_list:
            g = planet.get_mission_name_generator()
            for mission_name in g:
                prolog_fact = "planet_mission(\"{}\", \"{}\").\n".format(convert_to_prolog_str(planet.get_name()), convert_to_prolog_str(mission_name))
                yield prolog_fact
    save_file(save_location, temp())

def saveMissionTypeMissionRelation(mission_list, save_name = "missionType_mission.pl"):
    save_location = os.path.join(GLOBAL_FILE_PATH, save_name)
    def temp():
        for mission in mission_list:
            prolog_fact = "missionType_mission(\"{}\", \"{}\").\n".format(convert_to_prolog_str(mission.get_game_mode()), convert_to_prolog_str(mission.get_name()))
            yield prolog_fact
    save_file(save_location, temp())

def saveMissionRewardsToProlog(mission_list, save_name = "mission_reward.pl"):
    save_location = os.path.join(GLOBAL_FILE_PATH, save_name)
    def temp():
        
        def fact_maker(a, b, c, d):
            return "mission_reward(\"{}\", {}, \"{}\", {}).\n".format(convert_to_prolog_str(a), b, convert_to_prolog_str(c), d)

        for mission in mission_list:
            if mission.has_rotations():
                list_gen = mission.get_rewards()
                #Forms facts for A rotation
                a_rot_list = next(list_gen)
                for reward in a_rot_list:
                    prolog_fact = fact_maker(mission.get_name(), '\'A\'', reward.get_name(), reward.get_chance())
                    yield prolog_fact
                b_rot_list = next(list_gen)
                for reward in b_rot_list:
                    prolog_fact = fact_maker(mission.get_name(), '\'B\'', reward.get_name(), reward.get_chance())
                    yield prolog_fact
                c_rot_list = next(list_gen)
                for reward in c_rot_list:
                    prolog_fact = fact_maker(mission.get_name(), '\'C\'', reward.get_name(), reward.get_chance())
                    yield prolog_fact
            else:
                reward_list = next(mission.get_rewards())
                for reward in reward_list:
                    prolog_fact = fact_maker(mission.get_name(), '_', reward.get_name(), reward.get_chance())
                    yield prolog_fact
    save_file(save_location, temp())

def buildAllEnemies(fullJson):
    miscItems = fullJson["miscItems"]
    enemyToMods = fullJson["enemyModTables"]
    id_to_builder = {}
    def get_enemy_builder(id_num, enemy_json):
        builder = id_to_builder.get(id_num, None)
        if builder is None:
            builder = EnemyBuilder(id_num)
            builder.set_name(enemy_json["enemyName"])
            id_to_builder[id_num] = builder
        return builder
    for enemy_mods_json in enemyToMods:
        builder = get_enemy_builder(enemy_mods_json["_id"], enemy_mods_json)
        builder.set_mod_chance(float(enemy_mods_json["enemyModDropChance"])/100)
        for mod in enemy_mods_json["mods"]:
            chance = mod['chance']
            if (chance is None):
                continue
            mod_id = mod["_id"]
            mod_name = mod["modName"]
            chance = float(chance)/100
            rarity = mod["rarity"]
            builder.add_mod(Reward(mod_id, mod_name, chance, rarity))

    for enemy_json in miscItems:
        builder = get_enemy_builder(enemy_json["_id"], enemy_json)
        builder.set_resource_chance(float(enemy_json["enemyItemDropChance"])/100)
        for resource in enemy_json["items"]:
            reward = Reward.from_json(resource)
            builder.add_resource(reward)
    enemy_list = list(id_to_builder.values())
    for i in range(len(enemy_list)):
        enemy_list[i] = enemy_list[i].build()
    return enemy_list
        
def saveEnemyDataToProlog(enemy_list):
    def get_prolog_fact(fact_name, enemy, reward):
        fact = "{}(\"{}\", \"{}\", {}).\n".format(fact_name, convert_to_prolog_str(enemy.get_name()), convert_to_prolog_str(reward.get_name()), reward.get_chance())
        return fact
    def getModList(enemy):
        return enemy.get_mod_drops()
    def getResourceList(enemy):
        return enemy.get_resource_drops()
    def genericEnemyToProlog(enemy_list, save_name, fact_name, get_rewards):
        save_location = os.path.join(GLOBAL_FILE_PATH, save_name)
        def a():
            for enemy in enemy_list:
                for reward in get_rewards(enemy):
                    fact = get_prolog_fact(fact_name, enemy, reward)
                    yield fact
        save_file(save_location, a())
                
    
    genericEnemyToProlog(enemy_list, "enemy_mod_drops.pl", "enemy_mod_drops", getModList)
    genericEnemyToProlog(enemy_list, "enemy_resource_drops.pl", "enemy_resource_drops", getResourceList)
    

#Generates prolog facts
if __name__ == "__main__":
    #Sets up prolog facts for relics
    GLOBAL_FILE_PATH = os.path.dirname(sys.argv[0])
    fullJson = DataGetter.getJson()
    
    relicsList = createAllRelics(fullJson)
    saveRelicsToPrologFile(relicsList)
    del relicsList

    planet_list = createAllPlanets(fullJson)
    savePlanetMissionRelationToPrologFile(planet_list)
    
    mission_list = createAllMissions(planet_list)
    
    saveMissionTypeMissionRelation(mission_list)

    addTransientMissions(mission_list, fullJson['transientRewards'])
    
    def split_mission_list(regular_mission_list, caches_mission_list):
        #Removes caches missions from the regular list of missions, as they must be dealt
        #with in a unique manner
        i = 0
        while i < len(regular_mission_list):
            mission = regular_mission_list[i]
            if mission.get_game_mode() == "Caches":
                caches_mission_list.append(mission)
                del regular_mission_list[i]
            else:
                i += 1
                
    caches_list = []
    split_mission_list(mission_list, caches_list)
    saveMissionRewardsToProlog(mission_list)
    del mission_list
    
    enemy_list = buildAllEnemies(fullJson)
    saveEnemyDataToProlog(enemy_list)
    
    
                
            
    
    

    
