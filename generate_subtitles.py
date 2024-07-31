"""Generate the subtitles file a video file"""

import argparse
import sys
import os
from utils.mapper import get_writing_system
from utils.media.video_converter import convert_to_images
from utils.media.subtitle_ocr import generate_subtitle


def parse_arguments() -> argparse.Namespace:
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


def check_arguments(args: argparse.Namespace, language: str) -> None:
    """
    Check the validity of the input arguments.

    This function checks if the input video file exists, if the output subtitle file already exists,
    and if the subtitle area value is within the valid range of 0 to 100.

    If any of the checks fail, an appropriate error message is printed and the program exits.
    """
    if not os.path.isfile(args.input_video):
        print(f"File {args.input_video} does not exist")
        sys.exit(1)

    if os.path.isfile(args.output_subtitle):
        print(f"File {args.output_subtitle} already exists")
        sys.exit(1)

    if language == "Unknown":
        print(f"Language {args.input_language} is not supported")
        sys.exit(1)

    if (
        not args.subtitle_area.isnumeric()
        or int(args.subtitle_area) < 0
        or int(args.subtitle_area) > 100
    ):
        print("Subtitle area should be between 0 and 100")
        sys.exit(1)


FRAMES_DIR = "frames"
args = parse_arguments()
language = get_writing_system(args.input_language)
check_arguments(args, language)

convert_to_images(args.input_video, FRAMES_DIR, y1_percent=int(args.subtitle_area))
generate_subtitle(FRAMES_DIR, args.input_language, args.output_subtitle)
