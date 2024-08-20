""" Test the chunks module. """

from unittest import mock

import unittest
import datetime
import srt

from translate_subtitles.utils.converter import to_list
from translate_subtitles.utils.chunks import (
    __max_token_limit_exceeded as max_token_limit_exceeded,
    __num_tokens_from_string as num_tokens_from_string,
    create_translation_chunks,
    skip_chunks,
    translate_chunks,
)


class TestChunks(unittest.TestCase):
    """
    Unit test suite for the chunks module.
    """

    def setUp(self) -> None:
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
        self.small_original_chunk = [
            self.__create_subtitle(self.sample_subtitle, index) for index in range(10)
        ]
        self.small_chunk_to_translate = [self.small_original_chunk]
        self.small_translated_chunk = self.small_chunk_to_translate

        # 20 subtitles with 120 * 20 = 2400 tokens each (> 2622 / 2 = 1311 tokens)
        self.large_original_chunk = [
            self.__create_subtitle(self.sample_subtitle, index) for index in range(20)
        ]
        self.large_chunk_to_translate = [
            self.large_original_chunk[:10],
            self.large_original_chunk[10:],
        ]
        self.large_translated_chunk = self.large_chunk_to_translate

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

    def test_num_tokens_from_string(self) -> None:
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

    def test_create_translation_chunks_small(self) -> None:
        """
        Test the create_translation_chunks function.
        """
        actual = to_list(create_translation_chunks(self.small_original_chunk))
        self.assertListEqual(self.small_chunk_to_translate, actual)

    def test_create_translation_chunks_large(self) -> None:
        """
        Test the create_translation_chunks function.
        """
        actual = to_list(create_translation_chunks(self.large_original_chunk))
        self.assertListEqual(self.large_chunk_to_translate, actual)

    @mock.patch(
        "translate_subtitles.utils.chunks.translate_string",
        side_effect=lambda text, _, __: text,
    )
    def test_translate_chunks_small(self, _) -> None:
        """
        Test the translate_chunks function.
        """
        actual = to_list(translate_chunks(self.small_chunk_to_translate, "zh", "en"))
        self.assertListEqual(self.small_translated_chunk, actual)

    @mock.patch(
        "translate_subtitles.utils.chunks.translate_string",
        side_effect=lambda text, _, __: text,
    )
    def test_translate_chunks_large(self, _) -> None:
        """
        Test the translate_chunks function.
        """
        actual = to_list(translate_chunks(self.large_chunk_to_translate, "zh", "en"))
        self.assertListEqual(self.large_translated_chunk, actual)

    def test_skip_chunks(self) -> None:
        """
        Test the skip_chunks function.
        """
        skip = 1
        actual = to_list(skip_chunks(iter(self.large_chunk_to_translate), skip))
        self.assertListEqual(self.large_chunk_to_translate[skip:], actual)
