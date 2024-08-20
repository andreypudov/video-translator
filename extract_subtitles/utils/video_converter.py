""" This module contains a function to convert a video file into a sequence of images. """

from datetime import timedelta
import os
import cv2


def convert_to_images(
    video_file: str,
    image_directory: str = None,
    frame_rate: int = 10,
    x1_percent: int = 0,
    x2_percent: int = 100,
    y1_percent: int = 80,
    y2_percent: int = 100,
) -> None:
    """
    Convert a video file into a sequence of images.

    Args:
        video_file (str): The path to the video file.
        image_directory (str, optional): The directory to save the extracted images.
                                         If not provided, a directory with the name of the video file will be created.
                                         Defaults to None.
        frame_rate (int, optional): The desired frame rate for the extracted images. Defaults to 10.
        x1_percent (int, optional): The percentage of the width to start cropping from (left side). Defaults to 0.
        x2_percent (int, optional): The percentage of the width to end cropping at (right side). Defaults to 100.
        y1_percent (int, optional): The percentage of the height to start cropping from (top side). Defaults to 80.
        y2_percent (int, optional): The percentage of the height to end cropping at (bottom side). Defaults to 100.

    Returns:
        None
    """
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    capture_rate = max(round(fps / frame_rate), 1)
    print(
        f"Capture the image every {capture_rate} frames to have {frame_rate} images per second."
    )

    frame_count = 0
    image_count = 0
    # Get the video file's name without extension
    video_name = os.path.splitext(os.path.basename(video_file))[0]

    # Create an output folder with a name corresponding to the video
    if image_directory is None:
        image_directory = f"{video_name}_frames"
    os.makedirs(image_directory, exist_ok=True)

    while cap.isOpened():
        frame_exists, frame = cap.read()
        if frame_exists:
            if frame_count % capture_rate == 0:
                timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
                timestamp_s = round(timestamp_ms / 1000, 2)
                timestamp = timedelta(seconds=timestamp_s)

                output_file = f"{image_directory}/frame_{timestamp}.jpg"

                # Get the dimensions of the image
                height, width = frame.shape[:2]

                # Calculate the pixel coordinates
                x1 = int(width * x1_percent / 100)
                y1 = int(height * y1_percent / 100)
                x2 = int(width * x2_percent / 100)
                y2 = int(height * y2_percent / 100)

                # Crop the image
                frame = frame[y1:y2, x1:x2]

                cv2.imwrite(output_file, frame)
                image_count += 1
                print(
                    f"Frame {frame_count} has been extracted and saved as {output_file}"
                )
                print(f"for frame : {frame_count}, timestamp is: {timestamp}")
        else:
            break
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    return
