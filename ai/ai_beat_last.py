"""An AI that always throws the move that would beat opponent's previous move."""

from ai_templates.ai import AI

class AI_beat_last(AI):

	def move(self, data):
		if not data['moves']: # If this is the first turn.
			import random
			return random.choice(self.legal_moves)
		else:
			player_number = data['player_number']
			opps_last_move = data['moves'][-1][-player_number]
			return self.beats[opps_last_move]
