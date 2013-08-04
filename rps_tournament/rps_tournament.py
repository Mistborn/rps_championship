#! /usr/bin/env python3


def run(list_of_AIs, rounds_per_match=1000):
	"""Pit multiple RPS algorithms against each other in a round-robin
	tournament."""

	assert len(list_of_AIs) >= 2, "Needs at least two AIs for a tournament."
	import rps_main
	play = rps_main.play
	stats = {}

	for AI_index in range(len(list_of_AIs)):
		# Keep track of the AIs' scores.
		stats[AI_index] = {
		'wins': 0,
		'draws': 0,
		'partial_score': 0
		}
	

	for first_AI_index in range(len(list_of_AIs)):
		for second_AI_index in range(first_AI_index + 1, len(list_of_AIs)):
			# Pit two selected AIs against each other.
			(p1_points, p2_points) = play(list_of_AIs[first_AI_index],
										  list_of_AIs[second_AI_index],
										  rounds_per_match)

			# Update each AI's overall score.
			if p1_points > p2_points:
				stats[first_AI_index]['wins'] += 1
			elif p2_points > p1_points:
				stats[second_AI_index]['wins'] += 1
			else:
				stats[first_AI_index]['draws'] += 1
				stats[second_AI_index]['draws'] += 1
				
			stats[first_AI_index]['partial_score'] += p1_points
			stats[second_AI_index]['partial_score'] += p2_points

	# Sort the AIs based on how well they did in the tournament.
	sorted_indices = sorted(stats.keys(),
						 key = lambda index: (
						 	stats[index]['wins'],
						 	stats[index]['draws'],
						 	stats[index]['partial_score']),
						 reverse  = True)

	# Print out the final standings.
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

	# Return the results in a script-friendly format.
	stats['final_standings'] = sorted_indices
	return stats