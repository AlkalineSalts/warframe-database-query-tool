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

