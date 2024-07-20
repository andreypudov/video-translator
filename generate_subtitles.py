"""Generate the subtitles file a video file"""

import argparse
from utils.video_to_images import video_to_images
from utils.subtitle_ocr import generate_subtitle

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

frames_dir = 'teahouse_frames'
video_to_images(args.input_video, y1_percent=int(args.subtitle_area), image_directory=frames_dir)
generate_subtitle(frames_dir, args.input_language, args.output_subtitles)
