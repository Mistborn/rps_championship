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
		assert p1_move in ['r', 'p', 's'], 'Player 1 tried to make an invalid move.'
		assert p2_move in ['r', 'p', 's'], 'Player 2 tried to make an invalid move.'

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
		print("Round {round}: {p1_move} - {p2_move}. Score: {p1_points} - {p2_points}".format(**data))

		moves.append((p1_move, p2_move))
		round_no += 1


def main():
	parser = argparse.ArgumentParser(
		description='Pit two rock-paper-scissors programs against each other.')
	parser.add_argument('AIs', nargs=2)
	parser.add_argument('--rounds', dest='total_rounds', type=int, default=100)
	args = parser.parse_args()
	import ai.ai_weighted_random as player1
	import ai.ai_beat_last as player2

	play(player1, player2, args.total_rounds)





if __name__ == '__main__':
	main()