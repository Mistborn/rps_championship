#! /usr/bin/env python3

from ai_templates.ai import AI
import random

class AIBeatLast(AI):
	"""An AI that always throws the move that would beat opponent's previous move."""

	def __init__(self, name='ai_beat_last'):
		self.__name__ = name

	def move(self, data):
		if not data['moves']: # If this is the first turn.
			return random.choice(self.legal_moves)
		else:
			player_number = data['player_number']
			opps_last_move = data['moves'][-1][-player_number]
			return self.beats[opps_last_move]
