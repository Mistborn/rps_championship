"""An AI that always throws whatever would defeat opponent's most common throw."""

throw_occurences = {'r': 0,
					'p': 0,
					's': 0}
beats = {'r': 'p',
		 'p': 's',
		 's': 'r'}

def move(data):
	moves = data['moves']
	player_number = data['player_number']
	if moves: # If this isn't the first round.
		# Add opponent's last move to cumulative count.
		throw_occurences[moves[-1][-player_number]] += 1

	opps_most_common_throw = sorted(throw_occurences, key = lambda x: throw_occurences[x])[-1]
	return beats[opps_most_common_throw]