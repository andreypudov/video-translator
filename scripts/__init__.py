"""This module contains the scripts to generate and translate subtitles"""

from generate_subtitles.generate_subtitles import main as generate_subtitles
from translate_subtitles.translate_subtitles import main as translate_subtitles


def generate_subtitles_script():
    """
    Generates script by calling the generate_subtitles function.
    """
    generate_subtitles()


def translate_subtitles_script():
    """
    Generates script by calling the translate_subtitles function.
    """
    translate_subtitles()
