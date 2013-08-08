#! /usr/bin/env python3

"""Run all the unit tests."""

import unittest


def main():
	"""Run all the unit tests."""

	loader = unittest.TestLoader()
	tests = loader.discover(start_dir='unit_tests')
	runner = unittest.runner.TextTestRunner()
	runner.run(tests)


if __name__=='__main__':
	main()