"""Generate the subtitles file a video file"""

import argparse

parser = argparse.ArgumentParser(
    prog="generate_subtitles", description="Generate subtitles from a video file"
)

parser.add_argument(
    "--input-video", help="the file name of the video to be processed", required=True
)
parser.add_argument(
    "--output-subtitles", help="the file name of the output subtitles", required=True
)
parser.add_argument(
    "--input-language", help="the language of the subtitles in the video", required=True
)
parser.add_argument(
    "--subtitle-area",
    help="the area of the subtitles on the frame (in percentage from the top left corner)",
    required=True,
)

args = parser.parse_args()
