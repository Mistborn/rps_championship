#! /usr/bin/python3

"""An AI that adapts its moves based on what it thinks the opponent is most
likely to throw next. Considers the following:
- total throws made by opponent
- total throws made by self
- for each 5-long streak of own throws, what the opponent did next
- for each 5-long streak of opponent throws, what the opponent did next
"""

import random
from collections import defaultdict
from ai_templates 

class AI_apdaptive:

	def __init__(self, name='ai_adaptive'):
		self.__name__ = name

	round_number = 0

	own_throws = {'r': 0,
				  'p': 0,
				  's': 0}

	opp_throws = {'r': 0,
				  'p': 0,
				  's': 0}

	beats = {'r': 'p', 'p': 's', 's': 'r'}

	def defaultdict_int():
		return defaultdict(int)

	own_throws_mapping = defaultdict(lambda: defaultdict(int))
	opp_throws_mapping = defaultdict(defaultdict_int)


	def move(self, data):
		moves = data['moves']
		player_number = data['player_number']
		if moves:
			own_throws[moves[player_number-1]] += 1
			opp_throws[moves[-player_number]] += 1
		if len(moves) < 6:
			# Play randomly for the first six rounds
			return random.choice['r','p','s']
		else:
		


		round_number +=1

