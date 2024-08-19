""" This module contains functions that print the progress of the subtitle translation. """

import collections.abc
import srt


def __print_progress(sub: srt.Subtitle) -> None:
    """
    Prints the progress of the subtitle translation.

    Args:
        sub (srt.Subtitle): The subtitle object.
    """
    begin_char = "\r" if sub.index != 1 else ""
    print(f"{begin_char}  >> {sub.index}: [{sub.end}] {sub.content:.40}...", end="")


def print_progress_chunk(
    chunk: collections.abc.Generator[srt.Subtitle],
) -> collections.abc.Generator[srt.Subtitle]:
    """
    Yields each subtitle in the chunk and updates the progress bar.

    Args:
        chunk (collections.abc.Generator[srt.Subtitle]):
                               A generator of srt.Subtitle objects representing a chunk of subtitles.

    Yields:
        srt.Subtitle: A generator that yields each subtitle.
    """
    for sub in chunk:
        __print_progress(sub)
        yield sub


def print_progress_chunks(
    chunks: collections.abc.Generator[collections.abc.Generator[srt.Subtitle]],
) -> collections.abc.Generator[collections.abc.Generator[srt.Subtitle]]:
    """
    Yields each chunk of subtitles and updates the progress bar.

    Args:
        chunks (collections.abc.Generator[collections.abc.Generator[srt.Subtitle]]):
                               A generator of generators containing subtitle chunks.
        progress:              The progress bar.

    Yields:
        collections.abc.Generator[collections.abc.Generator[srt.Subtitle]]:
                               A generator of generators containing subtitle chunks.
    """
    for chunk in chunks:
        yield print_progress_chunk(chunk)

    # new line after the progress information
    print("\n", end="")
