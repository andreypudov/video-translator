import collections.abc
import srt
import re


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
        sub.content = f"{index}:: {sub.content}"
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
    for line in filter(
        None, re.split(r"\d+:: ", string.strip().replace("\n", " ").replace("\r", ""))
    ):
        yield line


def decode_chunk(
    chunk: collections.abc.Generator[srt.Subtitle],
) -> collections.abc.Generator[srt.Subtitle]:
    """
    Decodes each subtitle in the given chunk by removing the index from the content.

    Args:
        chunk (collections.abc.Generator[srt.Subtitle]):
                               A generator of srt.Subtitle objects representing a chunk of subtitles.

    Yields:
        srt.Subtitle: The decoded subtitle with the index removed from its content.
    """
    for sub in chunk:
        sub.content = sub.content.split(":: ", 1)[1]
        yield sub


def decode_chunks(
    chunks: collections.abc.Generator[collections.abc.Generator[srt.Subtitle]],
) -> collections.abc.Generator[collections.abc.Generator[srt.Subtitle]]:
    """
    Decodes the subtitle chunks.

    Args:
        chunks: A generator of generators containing subtitle chunks.

    Yields:
        Decoded chunks.

    """
    for chunk in chunks:
        yield decode_chunk(chunk)
