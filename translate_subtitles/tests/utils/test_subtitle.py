""" Test the subtitle module. """

from unittest import mock

import datetime
import unittest
import srt

from translate_subtitles.utils.subtitle import (
    count_subtitles,
    read_subtitle,
    write_subtitle,
)

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

ANDREY_RUBLEV_CONTENT_1 = (
    "1\n"
    "00:00:18,839 --> 00:00:22,300\n"
    "Andrey Rublev\n"
    "\n"
    "2\n"
    "00:02:25,830 --> 00:02:27,530\n"
    "Pull the rope.\n"
    "\n"
    "3\n"
    "00:02:27,840 --> 00:02:29,539\n"
    "This is one?\n\n"
)

ANDREY_RUBLEV_CONTENT_2 = (
    "4\n"
    "00:02:34,840 --> 00:02:36,539\n"
    "Arkhip, give me the strap.\n"
    "\n"
    "5\n"
    "00:02:36,840 --> 00:02:38,539\n"
    "Hold it.\n"
    "\n"
    "6\n"
    "00:02:42,849 --> 00:02:43,669\n"
    "Take it.\n\n"
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

        self.chunk = [
            [
                srt.Subtitle(
                    index=1,
                    start=datetime.timedelta(seconds=18, milliseconds=839),
                    end=datetime.timedelta(seconds=22, milliseconds=300),
                    content="Andrey Rublev",
                ),
                srt.Subtitle(
                    index=2,
                    start=datetime.timedelta(minutes=2, seconds=25, milliseconds=830),
                    end=datetime.timedelta(minutes=2, seconds=27, milliseconds=530),
                    content="Pull the rope.",
                ),
                srt.Subtitle(
                    index=3,
                    start=datetime.timedelta(minutes=2, seconds=27, milliseconds=840),
                    end=datetime.timedelta(minutes=2, seconds=29, milliseconds=539),
                    content="This is one?",
                ),
            ],
            [
                srt.Subtitle(
                    index=4,
                    start=datetime.timedelta(minutes=2, seconds=34, milliseconds=840),
                    end=datetime.timedelta(minutes=2, seconds=36, milliseconds=539),
                    content="Arkhip, give me the strap.",
                ),
                srt.Subtitle(
                    index=5,
                    start=datetime.timedelta(minutes=2, seconds=36, milliseconds=840),
                    end=datetime.timedelta(minutes=2, seconds=38, milliseconds=539),
                    content="Hold it.",
                ),
                srt.Subtitle(
                    index=6,
                    start=datetime.timedelta(minutes=2, seconds=42, milliseconds=849),
                    end=datetime.timedelta(minutes=2, seconds=43, milliseconds=669),
                    content="Take it.",
                ),
            ],
        ]

    @mock.patch("builtins.open", mock.mock_open(read_data=SUBTITLE_CONTENT))
    def test_read_subtitle(self) -> None:
        """
        Test the read_subtitle function.
        """
        actual = list(read_subtitle("subtitle.srt"))
        self.assertEqual(
            self.subtitles,
            actual,
        )

    @mock.patch("builtins.open")
    def test_write_subtitle(self, open_mock: mock.MagicMock) -> None:
        """
        Test the write_subtitle function.
        """
        write_subtitle(self.chunk, "output.srt")

        open_mock.assert_has_calls(
            [
                mock.call("output.srt", "w", encoding="utf-8"),
                mock.call().__enter__(),
                mock.call().__enter__().write(ANDREY_RUBLEV_CONTENT_1),
                mock.call().__enter__().write(ANDREY_RUBLEV_CONTENT_2),
                mock.call().__exit__(None, None, None),
            ]
        )

    @mock.patch("builtins.open", mock.mock_open(read_data=SUBTITLE_CONTENT))
    def test_count_subtitles(self) -> None:
        """
        Test the count_subtitles function.
        """
        actual = count_subtitles("subtitle.srt")
        self.assertEqual(3, actual)
