"""Test the models module"""

import unittest

from translate_subtitles.utils.models import TRANSLATION_MODEL


class TestModels(unittest.TestCase):
    """
    Unit test suite for the models module.
    """

    def test_model_name(self) -> None:
        """
        Test case to verify the correctness of the model name.
        """
        self.assertEqual(
            "gpt-3.5-turbo-1106",
            TRANSLATION_MODEL.get("name"),
            "The model name is incorrect.",
        )

    def test_model_tokens(self) -> None:
        """
        Test the number of tokens in the translation model.
        """
        self.assertEqual(
            4_096, TRANSLATION_MODEL.get("tokens"), "The model tokens are incorrect."
        )
