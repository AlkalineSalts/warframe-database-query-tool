:- ensure_loaded('planet_mission.pl').
:- ensure_loaded('relic_drops.pl').
:- ensure_loaded('missionType_mission.pl').
:- ensure_loaded('mission_reward.pl').

rotationHelper(LETTER, NUMBER) :- 0 is mod(NUMBER, 4), LETTER = 'C', !.
rotationHelper(LETTER, NUMBER) :- NUM is NUMBER + 1, 0 is mod(NUM, 4), LETTER = 'B', !.
rotationHelper(LETTER, NUMBER) :- ((NUM is NUMBER + 2, 0 is mod(NUM, 4)); (NUM2 is NUMBER + 3, 0 is mod(NUM2, 4))), LETTER = 'A', !.



is_not_vaulted(X) :- findall(ITEM, (relic_drops(RELIC, ITEM, _), mission_reward(_, _, RELIC, _)), BAG), sort(BAG, SORTED), member(X, SORTED).
is_vaulted(X) :- findall(ITEM, is_not_vaulted(ITEM), NOT_VAULTED), findall(RELICITEM, relic_drops(_, RELICITEM, _), ALL_RELIC_ITEMS), ord_subtract(ALL_RELIC_ITEMS, NOT_VAULTED, VAULTED_ITEMS), member(X, VAULTED_ITEMS). 