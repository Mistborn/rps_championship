#! /usr/bin/env python3

"""A program for pitting rock-paper-scissors programs against each other.

Version x # Doesn't make sense to put in version numbers yet.

Data format:
{'player_number': player_number,
'moves': a list of tuples of all the moves played so far
} 
"""

import sys
import argparse
import ai
import random
import importlib
import pkgutil
import inspect


def determine_winner(throws):
	"""Determine which player won, when passed a tuple of their respective moves."""
	assert(len(throws) == 2)
	if throws[0] == throws[1]:
		return 0 # draw
	elif (throws == ('r', 's') or
		throws == ('p', 'r') or
		throws == ('s', 'p')):
		return 1 # First player wins
	else:
		return 2 # Second player wins


def play(player1, player2, rounds, verbosity=2):
	"""Pit two algorithms against each other for the specified number of rounds.
	Verbosity contros how much is printed to the console:
	0 - Nothing
	1 - Prints only result (with final score)
	2 - Prints roughly 10 intermediate results, and the final result.
	3 - Prints the throws and cumulative score each round. (Useful for debugging.)
	"""

	print_sub = {'p1_name': player1.__name__,
			'p2_name': player2.__name__,
			'rounds': rounds,}

	if verbosity >= 2:
		print("Pitting {p1_name} against {p2_name}, for a total of {rounds} rounds.".format(**print_sub))
	round_no = 1
	moves = []
	p1_points = 0
	p2_points = 0
	while round_no <= rounds:
		p1_move = player1.move({'player_number': 1,
							    'moves': moves})
		p2_move = player2.move({'player_number': 2,
								'moves': moves})

		# Make sure the AIs return a valid move
		assert p1_move in ['r', 'p', 's'], "Player 1 tried to make an invalid move."
		assert p2_move in ['r', 'p', 's'], "Player 2 tried to make an invalid move."

		winner = determine_winner((p1_move, p2_move))
		if winner == 1:
			p1_points += 1
		elif winner == 2:
			p2_points += 1

		print_sub['p1_move'] = p1_move
		print_sub['p2_move'] = p2_move
		print_sub['p1_points'] = p1_points
		print_sub['p2_points'] = p2_points
		print_sub['round'] = round_no

		# Output to the console
		if verbosity == 3:
			print("Round {round}: {p1_move} - {p2_move}. Score: {p1_points} - {p2_points}".format(**print_sub))
		elif verbosity == 2:
			# Print intermediate result roughly 10 times during the matchup.
			if round_no % int(rounds/10) == 0:
				print("Round {round}: {p1_move} - {p2_move}. Score: {p1_points} - {p2_points}".format(**print_sub))


		moves.append((p1_move, p2_move))
		round_no += 1

	if verbosity >= 1:
		print("Result: {p1_name} {p1_points} - {p2_points} {p2_name}".format(**print_sub))

	return (p1_points, p2_points)


def main():
	# Pull all available AIs from the ai module.
	AIs_available = [module[1] for module in pkgutil.walk_packages(['ai'])]
	parser = argparse.ArgumentParser(
		description='Pit two rock-paper-scissors programs against each other.')
	parser.add_argument('--player1', '--p1', choices=AIs_available, default=None)
	parser.add_argument('--player2', '--p2', choices=AIs_available, default=None)
	parser.add_argument('--rounds', '-r', dest='rounds', type=int, default=100,
						help="Number of rounds to be played.")
	parser.add_argument('--verbosity', '-v', type=int, default=2, help="How much to output\
					 to the console. 0 - Nothing, 1 - Only final result, 2 - Roughly 10\
					 intermediate results, 3 - Intermediate result every roundself.")
	args = parser.parse_args()
	# Import the modules where the two AIs reside.
	module_1 = importlib.import_module('ai.' + (args.player1 or random.choice(AIs_available)))
	module_2 = importlib.import_module('ai.' + (args.player2 or random.choice(AIs_available)))
	# Create an instance of each AI.
	player1 = [cls[1] for cls in inspect.getmembers(module_1, inspect.isclass) if
				 cls[0].startswith("AI")][-1]()
	player2 = [cls[1] for cls in inspect.getmembers(module_2, inspect.isclass) if
				 cls[0].startswith("AI")][-1]()
	
	play(player1, player2, args.rounds, verbosity=args.verbosity)


if __name__ == '__main__':
	main()