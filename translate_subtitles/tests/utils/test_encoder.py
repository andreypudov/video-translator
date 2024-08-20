""" Test the encoder module. """

import datetime
import unittest
import srt

from translate_subtitles.utils.converter import to_list
from translate_subtitles.utils.encoder import decode_string, encode_chunk, encode_chunks


class TestEncoder(unittest.TestCase):
    """
    Unit test suite for the encoder module.
    """

    def setUp(self) -> None:
        """
        Set up the test case by initializing the necessary variables.
        """
        self.chunk = [
            srt.Subtitle(
                index=1,
                start=datetime.timedelta(seconds=1),
                end=datetime.timedelta(seconds=2),
                content="Lorem ipsum dolor sit amet.",
            ),
            srt.Subtitle(
                index=2,
                start=datetime.timedelta(seconds=3),
                end=datetime.timedelta(seconds=4),
                content="Лорем ипсум долор сит амет.",
            ),
        ]

        self.chunks = [self.chunk]

        self.encoded_chunk = [
            srt.Subtitle(
                index=1,
                start=datetime.timedelta(seconds=1),
                end=datetime.timedelta(seconds=2),
                content="| ::0:: Lorem ipsum dolor sit amet. |     |",
            ),
            srt.Subtitle(
                index=2,
                start=datetime.timedelta(seconds=3),
                end=datetime.timedelta(seconds=4),
                content="| ::1:: Лорем ипсум долор сит амет. |     |",
            ),
        ]

        self.encoded_chunks = [self.encoded_chunk]

        self.encoded_string = (
            "| Original | Translated |\n"
            "| --- | --- |\n"
            "| ::0:: Lorem ipsum dolor sit amet. | ::0:: Lorem ipsum dolor sit amet. |\n"
            "| ::1:: Лорем ипсум долор сит амет. | ::1:: Лорем ипсум долор сит амет. |"
        )

        self.decoded_string = [
            "Lorem ipsum dolor sit amet.",
            "Лорем ипсум долор сит амет.",
        ]

    def test_encode_chunk(self) -> None:
        """
        Test the encode_chunk function.

        This test verifies that the encoded chunk returned by the encode_chunk function matches the expected encoded chunk.

        Returns:
            None
        """
        actual = list(encode_chunk(self.chunk))
        self.assertListEqual(
            self.encoded_chunk, actual, "The encoded chunk is incorrect."
        )

    def test_encode_chunks(self) -> None:
        """
        Test the encode_chunks function.

        This test verifies that the encode_chunks function correctly encodes the given chunks and returns the expected result.
        """
        actual = to_list(encode_chunks(self.chunks))
        self.assertListEqual(
            self.encoded_chunks, actual, "The encoded chunks are incorrect."
        )

    def test_decode_string(self) -> None:
        """
        Test the decode_string function.

        This test case verifies that the decode_string function correctly decodes the encoded string and returns the
        expected result.
        """
        actual = list(decode_string(self.encoded_string))
        self.assertEqual(
            self.decoded_string, actual, "The decoded string is incorrect."
        )
