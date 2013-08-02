#! /usr/bin/env python3

from ai_templates.ai import AI
import random

class AIWeightedRandom(AI):
	"""An AI that throws a weighted random move."""

	def __init__(self, name='ai_weighted_random'):
		self.__name__ = name

	def move(self, data):
		pick = random.random()
		if pick <= 0.6:
			return 'p'
		elif pick <= 0.85:
			return 's'
		else:
			return 'r'