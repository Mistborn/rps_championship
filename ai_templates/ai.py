#! /usr/bin/env python3

"""A template for creating new AIs on-the-fly. (And also the class that
the included AIs inherit from)."""

class AI:
	"""A base class for AIs that play rock-paper-scissors."""

	# Class constants.
	legal_moves = ['r', 'p', 's']
	beats = { # A dict of what beats what.
	'r': 'p',
	'p': 's',
	's': 'r'}

	def __init__(self, name='unnamed_AI'):
		# Set the AI name (used by some of the playing scripts.)
		self.__name__ = name


	def reset(self):
		"""Resets the AI state between individual games in a tournament."""
		pass

	def move(self, data):
		"""A placeholder move function."""
		return 'r'