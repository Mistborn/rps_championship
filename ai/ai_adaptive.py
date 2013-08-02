#! /usr/bin/env python3

import random
from collections import defaultdict
from ai_templates.ai import AI


class AIAdaptive(AI):
	"""An AI that adapts its moves based on what it thinks the opponent is most
	likely to throw next. Considers the following:
	- total throws made by opponent
	- total throws made by self
	- for each 5-long streak of own throws, what the opponent did next
	- for each 5-long streak of opponent throws, what the opponent did next
	"""

	def __init__(self, name='ai_adaptive'):
		self.__name__ = name

	own_throws = {'r': 0,
				  'p': 0,
				  's': 0}

	opp_throws = {'r': 0,
				  'p': 0,
				  's': 0}

	# Create a dict mapping each sequence of own 5 throws to what throw the
	# opponent did next, how many times.
	own_throws_mapping = defaultdict(lambda: defaultdict(int))
	# Same for the opponent's throws.
	opp_throws_mapping = defaultdict(lambda: defaultdict(int))

	def move(self, data):

		def weighted_choice(choices):
			"""When passed a dict assigning weight to each choice, it
			chooses an element with a chance proportional to that element's
			weight."""
			total = sum(weight for (choice, weight) in choices.items())
			r = random.uniform(0, total)
			upto = 0
			for choice, weight in choices.items():
				upto += weight
				if upto > r:
					return choice
			assert False, "Shouldn't get here"


		moves = data['moves']
		player_number = data['player_number']
		if moves:
			# Add each player's moves to a running total.
			self.own_throws[moves[-1][player_number-1]] += 1
			self.opp_throws[moves[-1][-player_number]] += 1
		if len(moves) < 6:
			# Play randomly for the first six rounds
			return random.choice(['r','p','s'])
		else:
			# Update the mappings of 5-sequences of moves to what opponent
			# move followed them.
			self.own_throws_mapping[tuple([move[player_number-1] for move in moves[-6:-1]])][moves[-1][-player_number]] += 1
			self.opp_throws_mapping[tuple([move[-player_number] for move in moves[-6:-1]])][moves[-1][-player_number]] += 1

			# Now let's add up all the weighted factors for picking our next move.
			choices = {'r': 0, 'p': 0, 's': 0}

			# Note that each of the four factors is weighted equally,
			# so if, for example, factor 1 suggests that we play 'r',
			# we add 1 to the weight of choice 'r'. However, if factor
			# 1 suggests both 'r' or 's' as good choices, we add 0.5 
			# to each of them.

			# 1. Opponent's most common move (let's assume he's likely to make
			# his most common move again.)
			most_common_throws = [throw for throw in self.opp_throws if
								  self.opp_throws[throw] == max(self.opp_throws.values())]
			for throw in most_common_throws:
				choices[self.beats[throw]] += 1/len(most_common_throws)

			# 2. Our most common throw so far. Assume the opponent will try to
			# beat it, and stay one step ahead of him.
			most_common_throws = [throw for throw in self.own_throws if
								  self.own_throws[throw] == max(self.own_throws.values())]
			for throw in most_common_throws:
				choices[self.beats[self.beats[throw]]] += 1/len(most_common_throws)
			
			# 3. Check the last 5 moves made by opponent. If he made the same 5
			# moves at some point in the past, see what he followed it up with,
			# and try to beat that.
			last_5_opp_moves = tuple([move[-player_number] for move in moves[-5:]])
			if last_5_opp_moves in self.opp_throws_mapping:
				most_common_no = max(self.opp_throws_mapping[last_5_opp_moves].values())
				most_common_throws = [throw for throw in self.opp_throws_mapping[last_5_opp_moves] if
									  self.opp_throws_mapping[last_5_opp_moves][throw] == most_common_no]
				for throw in most_common_throws:
					choices[self.beats[throw]] += 1/len(most_common_throws)

			# 4. Check the last 5 moves made by ourselves. If we made the same 5
			# moves at some point in the past, see what the opponent followed up
			# with, and try to beat that.
			last_5_own_moves = tuple([move[player_number -1] for move in moves[-5:]])
			if last_5_own_moves in self.own_throws_mapping:
				most_common_no = max(self.own_throws_mapping[last_5_own_moves].values())
				most_common_throws = [throw for throw in self.own_throws_mapping[last_5_own_moves] if
									  self.own_throws_mapping[last_5_own_moves][throw] == most_common_no]
				for throw in most_common_throws:
					choices[self.beats[throw]] += 1/len(most_common_throws)

			# And now let's choose!

			return weighted_choice(choices)
			
