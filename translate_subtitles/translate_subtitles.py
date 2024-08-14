""" Translate subtitles from one language to another. """

import argparse
import sys
import os

from translate_subtitles.utils.subtitle import read_subtitle, write_subtitle
from translate_subtitles.utils.chunks import create_translation_chunks, translate_chunks


def __parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments for the translation script.

    Returns:
        arguments: An object containing the parsed command line-arguments.
    """

    parser = argparse.ArgumentParser(
        prog="translate_subtitles", description="Translate subtitles"
    )

    parser.add_argument(
        "--input-subtitle",
        help="the file name of the original subtitle file",
        required=True,
    )

    parser.add_argument(
        "--output-subtitle",
        help="the file name of the output subtitle file",
        required=True,
    )

    parser.add_argument(
        "--input-language",
        help="the language of the original subtitle file (ISO 639-1 language code)",
        required=True,
    )

    parser.add_argument(
        "--output-language",
        help="the language of the output subtitle file (ISO 639-1 language code)",
        required=True,
    )

    return parser.parse_args()


def __check_arguments(args: argparse.Namespace) -> None:
    """
    Check the validity of input and output subtitle files.

    This function checks if the input subtitle file exists and if the output subtitle file already exists.
    If the input subtitle file does not exist, it prints an error message and exits the program.
    If the output subtitle file already exists, it prints an error message and exits the program.
    """
    if not os.path.isfile(args.input_subtitle):
        sys.exit(f"File {args.input_subtitle} does not exist")

    if os.path.isfile(args.output_subtitle):
        sys.exit(f"File {args.output_subtitle} already exists")


def main():
    """
    Main function for translating subtitles.

    This function parses command line arguments, checks the arguments, and performs the translation process.

    Args:
        None

    Returns:
        None
    """

    args = __parse_arguments()
    __check_arguments(args)

    generator = args.input_subtitle
    for function in (
        read_subtitle,
        create_translation_chunks,
        lambda chunk: translate_chunks(
            chunk, args.input_language, args.output_language
        ),
        lambda chunk: write_subtitle(chunk, args.output_subtitle),
    ):
        generator = function(generator)


if __name__ == "__main__":
    main()
