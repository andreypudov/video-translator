"""Test the encoder module"""

import datetime
import unittest
import srt

from translate_subtitles.utils.encoder import decode_string, encode_chunk, encode_chunks


class TestEncoder(unittest.TestCase):
    """
    Unit test suite for the encoder module.

    This class contains a suite of unit tests designed to verify the correct functionality of the encoding and decoding
    functions in the encoder module, specifically `encode_chunk`, `encode_chunks`, and `decode_string`. The tests ensure
    that subtitles are correctly encoded into a specific format and that encoded strings can be accurately decoded back to
    their original form.

    Attributes:
        chunk (list): A list of `srt.Subtitle` objects representing a sample subtitle chunk.
        chunks (list): A list containing multiple chunks, where each chunk is a list of `srt.Subtitle` objects.
        encoded_chunk (list): A list of `srt.Subtitle` objects representing the expected result after encoding `chunk`.
        encoded_chunks (list): A list containing encoded chunks, where each encoded chunk is a list of `srt.Subtitle` objects.
        encoded_string (str): A string representing the expected encoded result of the subtitles.
        decoded_string (list): A list of strings representing the expected result after decoding `encoded_string`.

    Methods:
        setUp():
            Prepares the test fixtures before each test method is executed.

        test_encode_chunk():
            Tests that the `encode_chunk` function correctly encodes a single chunk of subtitles.

        test_encode_chunks():
            Tests that the `encode_chunks` function correctly encodes multiple chunks of subtitles.

        test_decode_string():
            Tests that the `decode_string` function correctly decodes an encoded string of subtitles.
    """

    def setUp(self):
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

    def test_encode_chunk(self):
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

    def test_encode_chunks(self):
        """
        Test the encode_chunks function.

        This test verifies that the encode_chunks function correctly encodes the given chunks and returns the expected result.
        """
        actual = [list(generator) for generator in encode_chunks(self.chunks)]
        self.assertListEqual(
            self.encoded_chunks, actual, "The encoded chunks are incorrect."
        )

    def test_decode_string(self):
        """
        Test the decode_string function.

        This test case verifies that the decode_string function correctly decodes the encoded string and returns the expected result.
        """
        actual = list(decode_string(self.encoded_string))
        self.assertEqual(
            self.decoded_string, actual, "The decoded string is incorrect."
        )


if __name__ == "__main__":
    unittest.main()
