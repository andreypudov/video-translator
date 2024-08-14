""" This module contains functions to create and print chunks of subtitles to be translated. """

import sys
import collections.abc
import srt
import tiktoken

from translate_subtitles.utils.models import TRANSLATION_MODEL
from translate_subtitles.utils.encoder import decode_string, encode_chunk
from translate_subtitles.utils.translator import translate_string
from translate_subtitles.utils.validator import translation_is_valid

TOKEN_LIMIT = TRANSLATION_MODEL.get("tokens") * 64 / 100
ENCODING = tiktoken.encoding_for_model(TRANSLATION_MODEL.get("name"))


def __num_tokens_from_string(string: str) -> int:
    """
    Calculates the number of tokens in a given string.

    Args:
        string (str): The input string.

    Returns:
        int: The number of tokens in the string.
    """

    return len(ENCODING.encode(string))


def __max_token_limit_exceeded(tokens: int) -> bool:
    """
    Checks if the token limit is exceeded.

    Args:
        tokens (int): The number of tokens in the subtitle.

    Returns:
        bool: True if the token limit is exceeded, False otherwise.
    """

    return tokens > TOKEN_LIMIT


def create_translation_chunks(
    subtitle: collections.abc.Generator[srt.Subtitle],
) -> collections.abc.Generator[collections.abc.Generator[srt.Subtitle]]:
    """
    Creates chunks of subtitles to be translated.

    Args:
        subtitle (collections.abc.Generator[srt.Subtitle]): A generator that yields each subtitle.

    Yields:
        collections.abc.Generator[srt.Subtitle]: A generator that yields each chunk of subtitles.
    """
    chunk = []
    total_tokens = 0

    for sub in subtitle:
        content = f"| {sub.content} | {sub.content} |"
        tokens = __num_tokens_from_string(content)

        if __max_token_limit_exceeded(total_tokens + tokens):
            yield chunk
            chunk = []
            total_tokens = 0

        chunk.append(sub)
        total_tokens += tokens

    if chunk:
        yield chunk


def __translate_chunk(
    chunk: collections.abc.Generator[srt.Subtitle],
    input_language: str,
    output_language: str,
) -> collections.abc.Generator[srt.Subtitle]:
    """
    Translates each subtitle in the given chunk from the input language to the output language.

    Args:
        chunk (collections.abc.Generator[srt.Subtitle]):
                               A generator of srt.Subtitle objects representing the subtitles to be translated.
        input_language (str):  The input language code.
        output_language (str): The output language code.

    Yields:
        collections.abc.Generator[srt.Subtitle]: A generator of srt.Subtitle objects with translated content.

    """
    # store the subtitles in a string
    subtitle_list = list(encode_chunk(chunk))
    original = "| Original | Translated |\n| --- | --- |\n" + "\n".join(
        [sub.content for sub in subtitle_list]
    )

    translation = translate_string(original, input_language, output_language)
    if not translation_is_valid(translation, len(subtitle_list)):
        if len(subtitle_list) <= 1:
            sys.exit("Error: The translation is invalid.")

        __translate_chunk(chunk[: len(chunk) // 2], input_language, output_language)
        __translate_chunk(chunk[len(chunk) // 2 :], input_language, output_language)

    translation_list = list(decode_string(translation))

    for _, (original, translation) in enumerate(zip(subtitle_list, translation_list)):
        original.content = translation
        yield original


def translate_chunks(
    chunks: collections.abc.Generator[collections.abc.Generator[srt.Subtitle]],
    input_language: str,
    output_language: str,
) -> collections.abc.Generator[collections.abc.Generator[srt.Subtitle]]:
    """
    Translates a sequence of subtitle chunks from one language to another.

    Args:
        chunks (collections.abc.Generator[collections.abc.Generator[srt.Subtitle]]):
                               A generator of generators containing subtitle chunks.
        input_language (str):  The language of the input subtitles.
        output_language (str): The language to translate the subtitles into.

    Yields:
        collections.abc.Generator[collections.abc.Generator[srt.Subtitle]]:
                               A generator of generators containing translated subtitle chunks.
    """
    for chunk in chunks:
        yield __translate_chunk(chunk, input_language, output_language)


def skip_chunks(
    chunks: collections.abc.Generator[collections.abc.Generator[srt.Subtitle]],
    number: int,
) -> collections.abc.Generator[collections.abc.Generator[srt.Subtitle]]:
    """
    Skips a given number of chunks.

    Args:
        chunks (collections.abc.Generator[collections.abc.Generator[srt.Subtitle]]):
                               A generator of generators containing subtitle chunks.
        number (int): The number of chunks to skip.

    Yields:
        collections.abc.Generator[collections.abc.Generator[srt.Subtitle]]:
                               A generator of generators containing subtitle chunks.
    """
    for _ in range(number):
        next(chunks)

    return chunks


def print_chunks(
    chunks: collections.abc.Generator[collections.abc.Generator[srt.Subtitle]],
) -> None:
    """
    Prints the content of each subtitle in each chunk.

    Args:
        chunks (collections.abc.Generator[collections.abc.Generator[srt.Subtitle]]):
                               A generator that yields each chunk of subtitles.

    Returns:
        None
    """
    for chunk in chunks:
        print_chunk(chunk)


def print_chunk(chunk: collections.abc.Generator[srt.Subtitle]) -> None:
    """
    Prints the content of each subtitle in a chunk.

    Args:
        chunk (collections.abc.Generator[srt.Subtitle]): A generator that yields each subtitle in the chunk.

    Returns:
        None
    """
    for sub in chunk:
        print(sub.content)
