#! /usr/bin/python3

""" A quick test file to run a round-robin tournament
between random AIs from the ai module."""

from rps_tournament import rps_tournament
import pkgutil
import importlib
import random
import inspect

AIs_available = [module[1] for module in pkgutil.walk_packages(['ai'])]

list_of_AIs = []

for i in range(10):
	module = importlib.import_module('ai.' + random.choice(AIs_available))
	# Import the 
	player = [cls[1] for cls in inspect.getmembers(module, inspect.isclass) if
				 (cls[0][:2] == "AI" and cls[0][-2:] != "AI")][0]()
	list_of_AIs.append(player)

rps_tournament.run(list_of_AIs)