"""An AI that always throws a random move."""

from ai_templates.ai import AI

class AI_random(AI):
	"""An AI that always throws a random move."""

	def __init__(self, name='ai_random'):
		self.__name__ = name
	
	def move(self, data):
		import random
		return random.choice(self.legal_moves)