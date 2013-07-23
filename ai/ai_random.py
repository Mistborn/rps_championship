"""An AI that always throws a random move."""

def move(data):
	import random
	return random.choice(['r', 'p', 's'])