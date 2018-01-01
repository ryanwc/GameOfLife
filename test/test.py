#!/usr/bin/env python
"""
Run selected (or all) unit tests for the Game of Life.
"""
import unittest

from .test_game_of_life_cell import TestGameOfLifeCell
from .test_game_of_life_board import TestGameOfLifeBoard
from .test_game_of_life import TestGameOfLife


def main():
    test_classes_to_run = [TestGameOfLifeCell, TestGameOfLifeBoard,
                           TestGameOfLife]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

if __name__ == '__main__':
    main()
