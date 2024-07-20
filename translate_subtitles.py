import argparse

parser = argparse.ArgumentParser(prog = "translate_subtitles", description = "Translate subtitles")

parser.add_argument("--input-subtitle", help = "the file name of the original subtitle file", required = True)
parser.add_argument("--output-subtitle", help = "the file name of the output subtitle file", required = True)
parser.add_argument("--input-language", help = "the language of the original subtitle file (ISO 639-1 language code)", required = True)
parser.add_argument("--output-language", help = "the language of the output subtitle file (ISO 639-1 language code)", required = True)

args = parser.parse_args()
