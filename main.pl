:- ensure_loaded('planet_mission.pl').
:- ensure_loaded('relic_drops.pl').
:- ensure_loaded('missionType_mission.pl').
:- ensure_loaded('mission_reward.pl').

rotationHelper(LETTER, NUMBER) :- 0 is mod(NUMBER, 4), LETTER = 'C', !.
rotationHelper(LETTER, NUMBER) :- NUM is NUMBER + 1, 0 is mod(NUM, 4), LETTER = 'B', !.
rotationHelper(LETTER, NUMBER) :- ((NUM is NUMBER + 2, 0 is mod(NUM, 4)); (NUM2 is NUMBER + 3, 0 is mod(NUM2, 4))), LETTER = 'A', !.


is_in_droptables_help(ITEM) :- mission_reward(_, _, ITEM, _).
is_in_droptables(ITEM) :- (var(ITEM) -> is_in_droptables_help(ITEM); (is_in_droptables_help(ITEM), !)).

is_not_vaulted_help(X) :- findall(ITEM, (relic_drops(RELIC, _, ITEM, _), is_in_droptables(RELIC)), BAG), sort(BAG, SORTED), member(X, SORTED).
is_not_vaulted(X) :- (var(X) -> is_not_vaulted_help(X); (is_not_vaulted_help(X), !)).


is_vaulted_help(X) :- findall(ITEM, is_not_vaulted(ITEM), NOT_VAULTED), findall(RELICITEM, relic_drops(_, 'Intact', RELICITEM, _), DUPLICATE_ALL_RELICITEMS), sort(DUPLICATE_ALL_RELICITEMS, ALL_RELIC_ITEMS), ord_subtract(ALL_RELIC_ITEMS, NOT_VAULTED, VAULTED_ITEMS), member(X, VAULTED_ITEMS). 
is_vaulted(X) :- (var(X) -> is_vaulted_help(X); (is_vaulted_help(X), !)).