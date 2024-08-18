""" Test the subtitle module. """

from unittest import mock

import datetime
import unittest
import srt

from translate_subtitles.utils.subtitle import read_subtitle

SUBTITLE_CONTENT = (
    "1\n"
    "00:00:00,498 --> 00:00:02,827\n"
    "- Here's what I love most\n"
    "about food and diet.\n"
    "\n"
    "2\n"
    "00:00:02,827 --> 00:00:06,383\n"
    "We all eat several times a day,\n"
    "and we're totally in chargev\n"
    "\n"
    "3\n"
    "00:00:06,383 --> 00:00:09,427\n"
    "of what goes on our plate\n"
    "and what stays off.\n"
)


class TestSubtitle(unittest.TestCase):
    """
    Unit test suite for the subtitle module.
    """

    def setUp(self) -> None:
        """
        Prepare the test fixtures.
        """
        self.subtitles = [
            srt.Subtitle(
                index=1,
                start=datetime.timedelta(milliseconds=498),
                end=datetime.timedelta(seconds=2, milliseconds=827),
                content="- Here's what I love most about food and diet.",
            ),
            srt.Subtitle(
                index=2,
                start=datetime.timedelta(seconds=2, milliseconds=827),
                end=datetime.timedelta(seconds=6, milliseconds=383),
                content="We all eat several times a day, and we're totally in chargev",
            ),
            srt.Subtitle(
                index=3,
                start=datetime.timedelta(seconds=6, milliseconds=383),
                end=datetime.timedelta(seconds=9, milliseconds=427),
                content="of what goes on our plate and what stays off.",
            ),
        ]

    @mock.patch("builtins.open", mock.mock_open(read_data=SUBTITLE_CONTENT))
    def test_read_subtitle(self) -> None:
        """
        Test the read_subtitle function.
        """
        actual = list(read_subtitle("subtitle.srt"))
        print(actual)
        self.assertEqual(
            self.subtitles,
            actual,
        )
