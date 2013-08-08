#! /usr/bin/env python3

import unittest
import rps_main


class TestPlay(unittest.TestCase):
	"""Test the main play() method in rps_main.py."""


	class DummyAI:
		"""A Dummy AI for testing the play function."""

		def __init__(self, throw='r'):
			"""Let us define what throw the AI makes, so that we can check if the
			play function tracks the score right."""
			self.throw = throw
			self.__name__ = "Dummy_" + throw

		def move(self, data):
			return self.throw

		def reset(self):
			pass


	def test_play(self):
		"""Make sure the play function tracks and returns results correctly."""
		RockAI, PaperAI = self.DummyAI('r'), self.DummyAI('p')
		result = rps_main.play(RockAI, PaperAI, rounds=58)

		self.assertTrue(len(result) == 2, "Check that the result is a 2-tuple, \
								or *some* kind of length 2 container, anyway.")
		self.assertTrue(result[0] == 0, "First AI should score 0 points.")
		self.assertTrue(result[1] == 58, "Second AI should score 58 points.")


if __name__ == '__main__':
    unittest.main()