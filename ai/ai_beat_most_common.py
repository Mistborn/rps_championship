"""An AI that always throws whatever would defeat opponent's most common throw."""

def move(data):
	moves = data['moves']
	player_number = data['player_number']
	throw_occurences = {}

	beats = {'r': 'p',
			 'p': 's',
			 's': 'r'}

	for throw in ['r', 'p', 's']:
		throw_occurences[throw] = len([move for move in moves if move[-player_number] == throw])
	opps_most_common_throw = sorted(throw_occurences, key = lambda thing: throw_occurences[thing])[-1]
	return beats[opps_most_common_throw]
