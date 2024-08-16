"""Test the chunks module"""

import unittest

from translate_subtitles.utils.chunks import (
    __max_token_limit_exceeded as max_token_limit_exceeded,
    __num_tokens_from_string as num_tokens_from_string,
)


class TestChunks(unittest.TestCase):
    """
    Unit test suite for the chunks module.
    """

    def setUp(self):
        """
        Set up the test case by initializing the necessary variables.
        """
        self.token_length = {
            "Lorem ipsum dolor sit amet.": 6,
            "Лорем ипсум долор сит амет.": 16,
        }

    def test_num_tokens_from_string(self):
        """
        Test the __num_tokens_from_string function.
        """
        for string, expected in self.token_length.items():
            actual = num_tokens_from_string(string)
            self.assertEqual(expected, actual)

    def test_max_token_limit_exceeded(self):
        """
        Test the __max_token_limit_exceeded function.
        """
        self.assertIs(False, max_token_limit_exceeded(100))
        self.assertIs(False, max_token_limit_exceeded(2621))
        self.assertIs(True, max_token_limit_exceeded(2622))
