#! /usr/bin/env python3

from ai_templates.ai import AI
import random

class AIBeatMostCommon(AI):
	"""An AI that always throws whatever would defeat opponent's most common throw."""

	def __init__(self, name='ai_beat_most_common'):
		self.__name__ = name

	throw_occurences = {'r': 0,
						 'p': 0,
						 's': 0}
	
	def move(self, data):
		moves = data['moves']
		player_number = data['player_number']
		if moves: # If this isn't the first round.
			# Add opponent's last move to cumulative count.
			self.throw_occurences[moves[-1][-player_number]] += 1

		# Figure out opponent's most common throw. If there is more than one
		# that's been most common, return a random pick from those.
		opps_most_common_throws = [throw for throw in self.legal_moves if 
									self.throw_occurences[throw] == max(self.throw_occurences.values())]
		return self.beats[random.choice(opps_most_common_throws)]