#! /usr/bin/python3


def rps_tournament(list_of_AIs, rounds_per_match=1000):
	"""Pit multiple RPS algorithms against each other in a round-robin
	tournament."""

	assert len(list_of_AIs) >= 2, "Needs at least two AIs for a tournament."
	import rps_main
	play = rps_main.play
	stats = {}

	for AI_index in range(len(list_of_AIs)):
		# Need to keep track of the AIs by index rather than by object
		# reference, because we can have the same AI playing in the tournament
		# multiple times.
		stats[AI_index] = {
		'wins': 0,
		'draws': 0,
		'partial_score': 0
		}
	

	for first_AI in range(len(list_of_AIs)):
		for second_AI in range(first_AI + 1, len(list_of_AIs)):
			(p1_points, p2_points) = play(list_of_AIs[first_AI],
										  list_of_AIs[second_AI],
										  rounds_per_match)

			if p1_points > p2_points:
				stats[first_AI]['wins'] += 1
			elif p2_points > p1_points:
				stats[second_AI]['wins'] += 1
			else:
				stats[first_AI]['draws'] += 1
				stats[second_AI]['draws'] += 1
				
			stats[first_AI]['partial_score'] += p1_points
			stats[second_AI]['partial_score'] += p2_points

	sorted_indices = sorted(stats.keys(),
						 key = lambda index: (
						 	stats[index]['wins'],
						 	stats[index]['draws'],
						 	stats[index]['partial_score']),
						 reverse  = True)

	print("")
	print("Final results:")
	print("--------------")
	place = 1
	for index in sorted_indices:
		print("{place_str}. {name} - Wins: {wins} Draws: {draws} Partial_score: {partial_score}".format(
			place_str=place,
			name=list_of_AIs[index].__name__,
			wins=stats[index]['wins'],
			draws=stats[index]['draws'],
			partial_score=stats[index]['partial_score']
			))
		place += 1
