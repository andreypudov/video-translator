""" Extract subtitles from a video file. """

import argparse
import sys
import os


def __parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for transcribing subtitles script.

    Returns:
        arguments: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="transcribe_subtitles",
        description="Transcribing subtitles from an audio or video file",
    )

    parser.add_argument(
        "--input-media",
        help="the file name of the audio or video to be processed",
        required=True,
    )
    parser.add_argument(
        "--output-subtitle", help="the file name of the output subtitles", required=True
    )
    parser.add_argument(
        "--input-language",
        help="the language of the subtitles in the video",
        required=True,
    )

    return parser.parse_args()


def __check_arguments(args: argparse.Namespace) -> None:
    """
    Check the validity of the input arguments.

    This function checks if the input video file exists, if the output subtitle file already exists,
    and if the subtitle area value is within the valid range of 0 to 100.

    If any of the checks fail, an appropriate error message is printed and the program exits.
    """
    if not os.path.isfile(args.input_media):
        sys.exit(f"File {args.input_media} does not exist")

    if os.path.isfile(args.output_subtitle):
        sys.exit(f"File {args.output_subtitle} already exists")


def main():
    """
    Main function for transcribing subtitles from an audio or video.

    Args:
        None

    Returns:
        None
    """

    args = __parse_arguments()
    __check_arguments(args)

    # transcribe_subtitle(FRAMES_DIR, args.input_language, args.output_subtitle)


if __name__ == "__main__":
    main()
