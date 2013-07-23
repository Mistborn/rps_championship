"""An AI that always throws the move that would beat opponent's previous move."""

def move(data):
	if not data['moves']: # If this is the first turn.
		import random
		return random.choice(['r','p','s'])
	else:
		beats = {'r': 'p',
				 'p': 's',
				 's': 'r'}
		player_number = data['player_number']
		opps_last_move = data['moves'][-1][-player_number]
		return beats[opps_last_move]
