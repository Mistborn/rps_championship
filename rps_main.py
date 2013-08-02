#! /usr/bin/python3

"""A program for pitting rock-paper-scissors programs against each other.

Version 0.1

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


def play(player1, player2, total_rounds):
	print("Pitting {p1} against {p2}, for a total of {total_rounds} rounds.".format(
		p1 = player1.__name__,
		p2 = player2.__name__,
		total_rounds = total_rounds)
		)
	round_no = 1
	moves = []
	p1_points = 0
	p2_points = 0
	while round_no <= total_rounds:
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

		data = {'round': round_no,
				'p1_move': p1_move,
				'p2_move': p2_move,
				'p1_points': p1_points,
				'p2_points': p2_points,
				}

		if round_no % int(total_rounds/10) == 0:
			# Print out the intermediate result every 10th of the way.
			print("Round {round}: {p1_move} - {p2_move}. Score: {p1_points} - {p2_points}".format(**data))

		moves.append((p1_move, p2_move))
		round_no += 1

	return (p1_points, p2_points)


def main():
	# Pull all available AIs from the ai module.
	AIs_available = [module[1] for module in pkgutil.walk_packages(['ai'])]
	parser = argparse.ArgumentParser(
		description='Pit two rock-paper-scissors programs against each other.')
	parser.add_argument('--player1', '--p1', choices=AIs_available, default=None)
	parser.add_argument('--player2', '--p2', choices=AIs_available, default=None)
	parser.add_argument('--rounds', '-r', dest='total_rounds', type=int, default=100,
						help="Number of rounds to be played.")
	args = parser.parse_args()
	# Import the modules where the two AIs reside.
	module_1 = importlib.import_module('ai.' + (args.player1 or random.choice(AIs_available)))
	module_2 = importlib.import_module('ai.' + (args.player2 or random.choice(AIs_available)))
	# Create an instance of each AI.
	player1 = [cls[1] for cls in inspect.getmembers(module_1, inspect.isclass) if
				 cls[0].startswith("AI_")][0]()
	player2 = [cls[1] for cls in inspect.getmembers(module_2, inspect.isclass) if
				 cls[0].startswith("AI_")][0]()
	
	play(player1, player2, args.total_rounds)


if __name__ == '__main__':
	main()