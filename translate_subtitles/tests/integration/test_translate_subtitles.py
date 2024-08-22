""" Integration tests for the translate subtitles module. """

import unittest
import subprocess
import os
import srt


@unittest.skipUnless(os.getenv("TEST_TYPE") == "integration", "Skipping non-unit tests")
class TestTranslateSubtitles(unittest.TestCase):
    """
    Unit test suite for the translate subtitles module.
    """

    input_subtitle = "samples/leviathan.ru.srt"
    output_subtitle = "samples/leviathan_translated.en.srt"

    def test_translate_subtitles(self) -> None:
        """
        Test the translate_subtitles script.
        """

        self.assertIs(True, os.path.isfile(self.input_subtitle))
        self.assertIs(False, os.path.isfile(self.output_subtitle))

        subprocess.run(
            [
                "translate_subtitles",
                "--input-subtitle",
                self.input_subtitle,
                "--output-subtitle",
                self.output_subtitle,
                "--input-language",
                "ru",
                "--output-language",
                "en",
            ],
            check=True,
        )

        self.assertIs(True, os.path.isfile(self.output_subtitle))

        with (
            open(self.input_subtitle, "r", encoding="utf-8") as expected_file,
            open(self.output_subtitle, "r", encoding="utf-8") as actual_file,
        ):
            expected_content = expected_file.read()
            actual_content = actual_file.read()

            expected_subtitles = list(srt.parse(expected_content))
            actual_subtitles = list(srt.parse(actual_content))

            self.assertEqual(len(expected_subtitles), len(actual_subtitles))

    def tearDown(self):
        os.remove(self.output_subtitle)
