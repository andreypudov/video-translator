""" Read and write subtitle files. """

import collections.abc
from io import TextIOWrapper
import srt


def read_subtitle(input_subtitle: str) -> collections.abc.Generator[srt.Subtitle]:
    """
    Reads a subtitle file and yields each subtitle.

    Args:
        input_subtitle (str): The path to the input subtitle file.

    Yields:
        Subtitle: A generator that yields each subtitle.
    """
    with open(input_subtitle, "r", encoding="utf-8") as file:
        content = file.read()
        subtitle = srt.parse(content)

        for sub in subtitle:
            content = sub.content.strip().replace("\n", " ").replace("\r", "")
            sub.content = content

            yield sub


def __write_chunk(
    chunk: collections.abc.Generator[srt.Subtitle],
    file: TextIOWrapper,
    subtitle_index: int,
) -> int:
    """
    Writes the given list of subtitles to the specified output subtitle file.

    Args:
        chunk: A generator of srt.Subtitle objects representing a chunk of subtitles.
        file (TextIOWrapper): The file object to write the subtitles to.
        subtitle_index (int): The index of the subtitle.

    Returns:
        int: The updated index.
    """
    sub_list = []
    for sub in chunk:
        sub.index = subtitle_index
        sub_list.append(sub)

        subtitle_index += 1

    content = srt.compose(sub_list)

    file.write(content)
    file.flush()

    return subtitle_index


def write_subtitle(
    chunks: collections.abc.Generator[collections.abc.Generator[srt.Subtitle]],
    output_subtitle: str,
) -> None:
    """
    Writes the given list of subtitles to the specified output subtitle file.

    Args:
        chunks: A generator of generators containing subtitle chunks.
        output_subtitle (str): The path of the output subtitle file.

    Returns:
        None
    """
    index = 1
    with open(output_subtitle, "w", encoding="utf-8") as file:
        for chunk in chunks:
            index = __write_chunk(chunk, file, index)
