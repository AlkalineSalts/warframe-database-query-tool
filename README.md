README

This will explain how to use this project.

This project uses a python script to generate prolog scripts that will 
hold information about warframe.

To use the python script, simply type in "python3 path_to_Parser.py".
This will require an internet connection to fetch the data.
The script will generate some prolog files, which hold the facts about the game.
To efficiently access these, one should use a prolog interpreter, such as SWI-Prolog.

For a command-line user, type in "swipl" to get started and upon it loading, type "ensure_loaded("path_to_Main.pl")"

For a GUI user, go to File -> Consult and then select Main.pl

Once it has loaded, you will now be able to query this knowledgebase! Some experience will be necessary 
to unlock the full potential that prolog can offer, but I'll show you some here.

A prolog program source file contains facts and rules, and from the interpreter the user asks questions about data in the database.

An example of using the database is shown with relic_drops.

relic_drops(Relic, Relic_State, Item, Probability).

Example usages:
relic_drops('Axi A13 Relic', 'Intact', 'Orthos Prime Blueprint', 0.11)

Stated as a question, this statement asks "Does An Axi A13 Relic that is Intact drop an Orthos Prime Blueprint at an 11% rate?".
If you want to determine something more general, variables can be added to show which conditions would make the statement true.

For example, if you want to see the drops of an Intact Axi A13 Relic and don't want to see the percentage chance of the item dropping,
the question would be formatted as: relic_drops('Axi A13 Relic', 'Intact', X, _).
This question, in english, is asking "What items drop from an Axi A13 Relic that is Intact?".

If instead you do want to see the percentage chance, the question can be reformatted as:
relic_drops('Axi A13 Relic', 'Intact', X, Y).
This is asking "What items drop from an Axi A13 Relic that is Intact and with what percent?". 

Prolog will give you one answer at a time. To see another answer, if it is present, type the ';' key. To stop prolog from providing answers,
type '.' Once the question has either exhausted valid answers or the '.' key has been pressed, you will be allowed to ask another question.

Prolog facts/rules:
relic_drops(Relic, Relic_State, Item, Probability).

planet_mission(Planet, Mission).

mission_reward(Mission, Rotation, Item, Probability).

missionType_mission(MissionType, Mission).

is_vaulted(Item).

is_not_vaulted(Item).

is_in_droptables(Item).
