"""Test the chunks module"""

import unittest
import datetime
import srt

from translate_subtitles.utils.chunks import (
    __max_token_limit_exceeded as max_token_limit_exceeded,
    __num_tokens_from_string as num_tokens_from_string,
    create_translation_chunks,
)


class TestChunks(unittest.TestCase):
    """
    Unit test suite for the chunks module.
    """

    def setUp(self):
        """
        Set up the test case by initializing the necessary variables.
        """
        # sample string with 120 tokens
        self.sample_subtitle = "蝸雄化半鼻在步比免告很壯男意言愛福。燈婆下進找去虎葉假示丁跳兄壯羊裏，也小自植而物巴河校錯能麼住耳面麼這：呀香校福休遠央早荷甲很什氣消。"

        self.token_length = {
            "Lorem ipsum dolor sit amet.": 6,
            "Лорем ипсум долор сит амет.": 16,
            self.sample_subtitle: 120,
        }

        # 10 subtitles with 120 * 10 = 1200 tokens each (< 2622 / 2 = 1311 tokens)
        self.small_chunk_to_translate = [
            self.__create_subtitle(self.sample_subtitle, index) for index in range(10)
        ]
        self.small_translated_chunk = [self.small_chunk_to_translate]

        # 20 subtitles with 120 * 20 = 2400 tokens each (> 2622 / 2 = 1311 tokens)
        self.large_chunk_to_translate = [
            self.__create_subtitle(self.sample_subtitle, index) for index in range(20)
        ]
        self.large_translated_chunk = [
            self.large_chunk_to_translate[:10],
            self.large_chunk_to_translate[10:],
        ]

    def __create_subtitle(self, content: str, index: int) -> srt.Subtitle:
        """
        Create a subtitle object with the given content and index.

        Args:
            content (str): The content of the subtitle.
            index (int): The index of the subtitle.

        Returns:
            srt.Subtitle: The created subtitle object.
        """
        return srt.Subtitle(
            index=index,
            start=datetime.timedelta(seconds=index - 1),
            end=datetime.timedelta(seconds=index),
            content=content,
        )

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

    def test_create_translation_chunks_small(self):
        """
        Test the create_translation_chunks function.
        """
        actual = [
            list(generator)
            for generator in create_translation_chunks(self.small_chunk_to_translate)
        ]
        self.assertEqual(self.small_translated_chunk, actual)

    def test_create_translation_chunks_large(self):
        """
        Test the create_translation_chunks function.
        """
        actual = [
            list(generator)
            for generator in create_translation_chunks(self.large_chunk_to_translate)
        ]
        self.assertEqual(self.large_translated_chunk, actual)
