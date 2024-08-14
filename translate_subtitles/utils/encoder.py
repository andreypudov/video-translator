""" This module contains the functions to encode and decode subtitles. """

import collections.abc
import re
import srt


def encode_chunk(
    chunk: collections.abc.Generator[srt.Subtitle],
) -> collections.abc.Generator[srt.Subtitle]:
    """
    Encodes each subtitle in the given chunk by adding its index to the content.

    Args:
        chunk (collections.abc.Generator[srt.Subtitle]):
                               A generator of srt.Subtitle objects representing a chunk of subtitles.

    Yields:
        srt.Subtitle: The encoded subtitle with the index added to its content.
    """
    for index, sub in enumerate(chunk):
        escaped = (str(sub.content)).replace("|", "/").replace("::", ":")
        sub.content = f"| ::{index}:: {escaped} |     |"
        yield sub


def encode_chunks(
    chunks: collections.abc.Generator[collections.abc.Generator[srt.Subtitle]],
) -> collections.abc.Generator[collections.abc.Generator[srt.Subtitle]]:
    """
    Encodes the subtitle chunks.

    Args:
        chunks: A generator of generators containing subtitle chunks.

    Yields:
        Encoded chunks.

    """
    for chunk in chunks:
        yield encode_chunk(chunk)


def decode_string(string: str) -> collections.abc.Generator[str]:
    """
    Decode a string by splitting it based on a pattern and yielding the decoded lines.

    Args:
        string (str): The string to be decoded.

    Yields:
        str: The decoded lines.

    """
    for line in string.split("\n")[2:]:
        columns = line.split("|")
        if len(columns) == 4:
            translation = columns[2].strip()
            yield "".join(filter(None, re.split(r"::\d+::", translation))).strip()
