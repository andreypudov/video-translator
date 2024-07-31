"""Read and write subtitle files"""

import collections.abc
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


def write_subtitle(
    subtitle: collections.abc.Generator[collections.abc.Generator[srt.Subtitle]],
    output_subtitle: str,
) -> None:
    """
    Writes the given list of subtitles to the specified output subtitle file.

    Args:
        subtitle (list): The list of subtitles to write.
        output_subtitle (str): The path of the output subtitle file.

    Returns:
        None
    """
    with open(output_subtitle, "w", encoding="utf-8") as file:
        content = "".join([srt.compose(sub) for sub in subtitle])
        file.write(content)
