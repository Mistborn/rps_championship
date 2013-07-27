"""An AI that throws a random move, with biased distribution."""

from ai_templates.ai import AI

class AI_random(AI):
	"""An AI that throws a weighted random move."""

	def move(self, data):
		import random
		pick = random.random()
		if pick <= 0.6:
			return 'p'
		elif pick <= 0.85:
			return 's'
		else:
			return 'r'