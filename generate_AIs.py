#! /usr/bin/python3

"""A short test script for generating AIs on-the-fly, then pitting them
against each other in a tournament."""


def main():
	import random
	from copy import copy
	from ai_templates.ai import AI
	from rps_tournament import rps_tournament

	list_of_AIs = []

	for count in range(15):
		new_AI = AI(name='Random_AI_'+str(count+1))

		# Generate random move algorithm
		choices = copy(AI.legal_moves)
		random.shuffle(choices)
		print(choices)
		first_prob = random.random()
		second_prob = first_prob + (1-first_prob)/random.random()
		def move(data):
			import random
			roll = random.random()
			if roll < first_prob:
				return choices[0]
			elif roll < second_prob:
				return choices[1]
			else:
				return choices[2]

		new_AI.move = move
		list_of_AIs.append(new_AI)

	rps_tournament.run(list_of_AIs)


if __name__ == '__main__':
	main()