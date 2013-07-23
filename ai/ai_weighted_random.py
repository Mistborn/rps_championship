"""An AI that throws a random move, with biased distribution."""

def move(data):
	import random
	pick = random.random()
	if pick <= 0.6:
		return 'p'
	elif pick <= 0.85:
		return 's'
	else:
		return 'r'