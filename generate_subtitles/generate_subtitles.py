"""Generate the subtitles file a video file"""

import argparse
import sys
import os
from generate_subtitles.utils.mapper import get_writing_system
from generate_subtitles.utils.video_converter import convert_to_images
from generate_subtitles.utils.subtitle_ocr import generate_subtitle


def __parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for generating subtitles script.

    Returns:
        arguments: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="generate_subtitles", description="Generate subtitles from a video file"
    )

    parser.add_argument(
        "--input-video",
        help="the file name of the video to be processed",
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
    parser.add_argument(
        "--subtitle-area",
        help="the area of the subtitles on the frame (in percentage from the top left corner)",
        required=True,
    )

    return parser.parse_args()


def __check_arguments(args: argparse.Namespace, language: str) -> None:
    """
    Check the validity of the input arguments.

    This function checks if the input video file exists, if the output subtitle file already exists,
    and if the subtitle area value is within the valid range of 0 to 100.

    If any of the checks fail, an appropriate error message is printed and the program exits.
    """
    if not os.path.isfile(args.input_video):
        sys.exit(f"File {args.input_video} does not exist")

    if os.path.isfile(args.output_subtitle):
        sys.exit(f"File {args.output_subtitle} already exists")

    if language == "Unknown":
        sys.exit(f"Language {args.input_language} is not supported")

    if (
        not args.subtitle_area.isnumeric()
        or int(args.subtitle_area) < 0
        or int(args.subtitle_area) > 100
    ):
        sys.exit("Subtitle area should be between 0 and 100")


FRAMES_DIR = "frames"


def main():
    """
    Main function for generating subtitles from a video.

    Args:
        None

    Returns:
        None
    """

    args = __parse_arguments()
    language = get_writing_system(args.input_language)
    __check_arguments(args, language)

    convert_to_images(args.input_video, FRAMES_DIR, y1_percent=int(args.subtitle_area))
    generate_subtitle(FRAMES_DIR, args.input_language, args.output_subtitle)


if __name__ == "__main__":
    main()
