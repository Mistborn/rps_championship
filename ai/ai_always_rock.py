#! /usr/bin/env python3

from ai_templates.ai import AI

class AIAlwaysRock(AI):
	"""An AI that always throws rock."""

	def __init__(self, name='ai_always_rock'):
		self.__name__ = name

	def move(self, data):
		return 'r'