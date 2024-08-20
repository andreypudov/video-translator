""" Integration tests for the translate subtitles module. """

import unittest
import subprocess
import os
import srt


class TestTranslateSubtitles(unittest.TestCase):
    """
    Unit test suite for the translate subtitles module.
    """

    def test_translate_subtitles(self) -> None:
        """
        Test the translate_subtitles script.
        """
        input_subtitle = "samples/leviathan.ru.srt"
        output_subtitle = "samples/leviathan_translated.en.srt"

        self.assertIs(True, os.path.isfile(input_subtitle))
        self.assertIs(False, os.path.isfile(output_subtitle))

        subprocess.run(
            [
                "translate_subtitles",
                "--input-subtitle",
                input_subtitle,
                "--output-subtitle",
                output_subtitle,
                "--input-language",
                "ru",
                "--output-language",
                "en",
            ],
            check=True,
        )

        self.assertIs(True, os.path.isfile(output_subtitle))

        with (
            open(input_subtitle, "r", encoding="utf-8") as expected_file,
            open(output_subtitle, "r", encoding="utf-8") as actual_file,
        ):
            expected_content = expected_file.read()
            actual_content = actual_file.read()

            expected_subtitles = list(srt.parse(expected_content))
            actual_subtitles = list(srt.parse(actual_content))

            self.assertEqual(len(expected_subtitles), len(actual_subtitles))
