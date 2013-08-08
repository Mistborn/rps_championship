#! /usr/bin/env python3

import unittest
import importlib
import inspect
import pkgutil



class TestAIs(unittest.TestCase):
	"""Test that all the AIs in the ai folder work right."""

	@classmethod
	def setUpClass(cls):
		"""Import all the AIs."""

		import ai
		cls.list_of_AIs = []
		AIs_available = [module[1] for module in pkgutil.walk_packages(path=['ai'], prefix='ai.')]

		for AI_module in AIs_available:
			module = importlib.import_module(name=AI_module)
			cls.list_of_AIs.append([clss[1] for clss in inspect.getmembers(module, inspect.isclass) if
							 clss[0].startswith("AI")][-1]())

		assert len(cls.list_of_AIs) > 0, "Make sure we imported some AIs."

	def test_first_move(self):
		"""Check that each AI can correctly handle the first move."""
		data = {'moves': [],
				'player_number': 1}
		for AI in self.list_of_AIs:
			self.assertTrue(AI.move(data) in ['r', 'p', 's'])

	def test_fourth_move(self):
		"""Test that each AI can do the fourth move (a randomly picked number > 0)."""
		data = {'moves': [('r','s'), ('r','p'), ('s','p')],
				'player_number': 2}
		for AI in self.list_of_AIs:
			self.assertTrue(AI.move(data) in ['r', 'p', 's'])

	def test_reset(self):
		"""Check that each AI handles the 'reset()' command for resetting the 
		AI state between rounds in a tournament."""
		for AI in self.list_of_AIs:
			AI.reset()

	
if __name__ == '__main__':
    unittest.main()