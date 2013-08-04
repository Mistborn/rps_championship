#! /usr/bin/env python3

import random
from collections import defaultdict
from ai_templates.ai import AI


class AIAdaptive2(AI):
	"""An AI that adapts its moves based on what it thinks the opponent is most
	likely to throw next. Considers the following:
	- total throws made by opponent
	- total throws made by self
	- for each 5-long streak of own throws, what the opponent did next
	- for each 5-long streak of opponent throws, what the opponent did next

	On top of that, this AI changes the weight of each of those factors based
	on which ones have been successful so far.
	"""

	def __init__(self, name='ai_adaptive2'):
		self.__name__ = name

		self.own_throws = {'r': 0,
						  'p': 0,
						  's': 0}

		self.opp_throws = {'r': 0,
						  'p': 0,
						  's': 0}

		# Initialize the weights for each of the move decision factors
		self.weights = [1, 1, 1, 1]

		# Create a dict mapping each sequence of own 5 throws to what throw the
		# opponent did next, how many times.
		self.own_throws_mapping = defaultdict(lambda: defaultdict(int))
		# Same for the opponent's throws.
		self.opp_throws_mapping = defaultdict(lambda: defaultdict(int))
		# Example:
		# opp_throws_mapping[('r','r','p','s','p')] == {'r': 1}
		#  means that at some point in the past, the opponent played the sequence
		# of moves ('r', 'r', 'p', 's', 'p'), and then followed it up with 'r'. He
		# played that particular sequence of moves only once so far.

		# Initialize keeping track of move guesses for the purposes of updating
		# the weights of each move decision factor.
		self.guesses = [[],[],[],[]]

		# How much to change the weight of each factor upon success/failure
		self.success_modifier = 1.1 # Successfully predicted opponent's exact move
		self.partial_success_modifier = 1.04 # Partial success (guessed two possibilities)
		self.failure_modifier = 0.9 # Wrong prediction



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
			
			# Update factor weighing based on which ones predicted the
			# opponent's move well.
			opp_move = moves[-1][-player_number]
			desired_move = self.beats[opp_move]
			for index in range(4):
				# If the factor abstained from influencing the decision.
				if len(self.guesses[index]) in [0, 3]:
					pass
				# If the factor was wrong.
				elif desired_move not in self.guesses[index]:
					self.weights[index] *= self.failure_modifier
				# If the factor guessed exactly the correct move
				elif len(self.guesses[index]) == 1:
					self.weights[index] *= self.success_modifier
				# If the factor suggested two possibilities, one of them right.
				elif len(self.guesses[index]) == 2:
					self.weights[index] *= self.partial_success_modifier
				else:
					assert False, "Sanity check. Shouldn't get here."
				# Clean up the guess for next turn.
				del self.guesses[index][:]

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
				choices[self.beats[throw]] += 1/len(most_common_throws)*self.weights[0]
				# Update our guesses for weigthing the factors next turn.
				self.guesses[0].append(self.beats[throw])

			# 2. Our most common throw so far. Assume the opponent will try to
			# beat it, and stay one step ahead of him.
			most_common_throws = [throw for throw in self.own_throws if
								  self.own_throws[throw] == max(self.own_throws.values())]
			for throw in most_common_throws:
				choices[self.beats[self.beats[throw]]] += 1/len(most_common_throws)*self.weights[1]
				self.guesses[1].append(self.beats[self.beats[throw]])

			# 3. Check the last 5 moves made by opponent. If he made the same 5
			# moves at some point in the past, see what he followed it up with,
			# and try to beat that.
			last_5_opp_moves = tuple([move[-player_number] for move in moves[-5:]])
			if last_5_opp_moves in self.opp_throws_mapping:
				most_common_no = max(self.opp_throws_mapping[last_5_opp_moves].values())
				most_common_throws = [throw for throw in self.opp_throws_mapping[last_5_opp_moves] if
									  self.opp_throws_mapping[last_5_opp_moves][throw] == most_common_no]
				for throw in most_common_throws:
					choices[self.beats[throw]] += 1/len(most_common_throws)*self.weights[2]
					self.guesses[2].append(self.beats[throw])

			# 4. Check the last 5 moves made by ourselves. If we made the same 5
			# moves at some point in the past, see what the opponent followed up
			# with, and try to beat that.
			last_5_own_moves = tuple([move[player_number -1] for move in moves[-5:]])
			if last_5_own_moves in self.own_throws_mapping:
				most_common_no = max(self.own_throws_mapping[last_5_own_moves].values())
				most_common_throws = [throw for throw in self.own_throws_mapping[last_5_own_moves] if
									  self.own_throws_mapping[last_5_own_moves][throw] == most_common_no]
				for throw in most_common_throws:
					choices[self.beats[throw]] += 1/len(most_common_throws)*self.weights[3]
					self.guesses[3].append(self.beats[throw])


			# And now let's choose!

			return weighted_choice(choices)
			
