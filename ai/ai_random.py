#! /usr/bin/env python3

from ai_templates.ai import AI
import random

class AIRandom(AI):
	"""An AI that always throws a random move."""

	def __init__(self, name='ai_random'):
		self.__name__ = name
	
	def move(self, data):
		return random.choice(self.legal_moves)