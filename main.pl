:- ensure_loaded('planet_mission.pl').
:- ensure_loaded('relic_drops.pl').
:- ensure_loaded('missionType_mission.pl').
:- ensure_loaded('mission_reward.pl').
:- ensure_loaded('enemy_mod_drops').
:- ensure_loaded('enemy_resource_drops').

rotationHelper(LETTER, NUMBER) :- 0 is mod(NUMBER, 4), LETTER = 'C', !.
rotationHelper(LETTER, NUMBER) :- NUM is NUMBER + 1, 0 is mod(NUM, 4), LETTER = 'B', !.
rotationHelper(LETTER, NUMBER) :- ((NUM is NUMBER + 2, 0 is mod(NUM, 4)); (NUM2 is NUMBER + 3, 0 is mod(NUM2, 4))), LETTER = 'A', !.


is_in_droptables_help(ITEM) :- mission_reward(_, _, ITEM, _).
is_in_droptables(ITEM) :- (var(ITEM) -> is_in_droptables_help(ITEM); (is_in_droptables_help(ITEM), !)).

is_not_vaulted_help(X) :- findall(ITEM, (relic_drops(RELIC, ITEM, _), is_in_droptables(RELIC)), BAG), sort(BAG, SORTED), member(X, SORTED).
is_not_vaulted(X) :- (var(X) -> is_not_vaulted_help(X); (is_not_vaulted_help(X), !)).


is_vaulted_help(X) :- findall(ITEM, is_not_vaulted(ITEM), NOT_VAULTED), findall(RELICITEM, relic_drops(_, RELICITEM, _), DUPLICATE_ALL_RELICITEMS), sort(DUPLICATE_ALL_RELICITEMS, ALL_RELIC_ITEMS), ord_subtract(ALL_RELIC_ITEMS, NOT_VAULTED, VAULTED_ITEMS), member(X, VAULTED_ITEMS). 
is_vaulted(X) :- (var(X) -> is_vaulted_help(X); (is_vaulted_help(X), !)).

is_not_transient(MISSION) :- planet_mission(_, MISSION).

%Gives odds that it won't have it, fromt-facing predicate must takes 1 - this result
odds_of_getting_item_help(_, _, ROTATION_NUM, PROBABILITY) :- ROTATION_NUM < 1, PROBABILITY = 1, !.
odds_of_getting_item_help(MISSION, ITEM, ROTATION_NUM, PROBABILITY) :- ROTATION_NUM > 0, rotationHelper(ROT_LETTER, ROTATION_NUM), NEXT_ROTATION_NUM is ROTATION_NUM - 1, ((mission_reward(MISSION, ROT_LETTER ,ITEM, INTERMEDIATE_PROB)) -> (odds_of_getting_item_help(MISSION, ITEM, NEXT_ROTATION_NUM, NEXT_PROB), INVERSE_PROBABILITY is 1 - INTERMEDIATE_PROB, PROBABILITY is INVERSE_PROBABILITY * NEXT_PROB); (odds_of_getting_item_help(MISSION, ITEM, NEXT_ROTATION_NUM, PROBABILITY))).

%Odds of getting at least one item per this number of rotations (Reward cycle)
odds_of_getting_item_help_dos(MISSION, ITEM, NUM_ROTATION, PROBABILITY) :- odds_of_getting_item_help(MISSION, ITEM, NUM_ROTATION, INVERSE_PROB), PROBABILITY is 1 - INVERSE_PROB.

%Odds of getting at least one item per this number of rotations (Reward cycle)
odds_of_getting_item(MISSION, ROT, ITEM, Z) :- findall(X, mission_reward(X, _, _, _),BAG), sort(BAG, SORTED), member(MISSION, SORTED), odds_of_getting_item_help_dos(MISSION, ITEM, ROT, Z), Z \= 0.
