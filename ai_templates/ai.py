#! /usr/bin/python

"""A template for creating new AIs on-the-fly."""

class AI:
	"""An AI for playing rock-paper-scissors."""

	# Class constants.
	legal_moves = ['r', 'p', 's']
	beats = { # A dict of what beats what.
	'r': 'p',
	'p': 's',
	's': 'r'}

	def __init__(self, name='unnamed_AI'):
		self.__name__ = name

	def move(self, data):
		"""A placeholder move function."""
		return 'r'