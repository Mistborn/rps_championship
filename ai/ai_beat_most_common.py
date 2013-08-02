"""An AI that always throws whatever would defeat opponent's most common throw."""

from ai_templates.ai import AI

class AI_beat_most_common(AI):

	def __init__(self, name='ai_beat_most_common'):
		self.__name__ = name

	throw_occurences = {'r': 0,
						 'p': 0,
						 's': 0}
	
	def move(self, data):
		import random
		moves = data['moves']
		player_number = data['player_number']
		if moves: # If this isn't the first round.
			# Add opponent's last move to cumulative count.
			self.throw_occurences[moves[-1][-player_number]] += 1

		# Figures out opponent's most common throw. If there is more than one
		# that's been most common, return a random pick from those.
		opps_most_common_throw = sorted(self.throw_occurences, 
										key = lambda x: (self.throw_occurences[x], random.random()))[-1]
		return self.beats[opps_most_common_throw]