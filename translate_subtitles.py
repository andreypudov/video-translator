"""Translate subtitles"""

import argparse
import collections.abc
import json
import sys
import os
import openai
import srt


def parse_arguments() -> argparse.Namespace:
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


def check_arguments(args: argparse.Namespace) -> None:
    """
    Check the validity of input and output subtitle files.

    This function checks if the input subtitle file exists and if the output subtitle file already exists.
    If the input subtitle file does not exist, it prints an error message and exits the program.
    If the output subtitle file already exists, it prints an error message and exits the program.
    """
    if not os.path.isfile(args.input_subtitle):
        print(f"File {args.input_subtitle} does not exist")
        sys.exit(1)

    if os.path.isfile(args.output_subtitle):
        print(f"File {args.output_subtitle} already exists")
        sys.exit(1)


def translate_string(
    client: openai.OpenAI, text: str, input_language: str, output_language: str
) -> str:
    """
    Translates the given text from the input language to the output language using the OpenAI GPT-4 model.

    Args:
        client (object): The instance of the OpenAI client.
        text (str): The text to be translated.
        input_language (str): The language of the input text.
        output_language (str): The language to translate the text into.

    Returns:
        str: The translated text.
    """
    prompt = (
        f"You will be provided with a sentence in {input_language}, "
        f"and your task is to translate it into {output_language}."
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": text},
        ],
        temperature=0.7,
        max_tokens=64,
        top_p=1,
    )

    response_json = json.loads(response.model_dump_json(indent=2))
    content = response_json["choices"][0]["message"]["content"]

    return content


def translate_subtitle(
    input_subtitle: str, input_language: str, output_language: str
) -> collections.abc.Generator[srt.Subtitle]:
    """
    Translates the content of a subtitle file from the input language to the output language.

    Args:
        input_subtitle (str): The path to the input subtitle file.
        input_language (str): The language code of the input subtitle.
        output_language (str): The language code of the desired output translation.

    Yields:
        Subtitle: A generator that yields each translated subtitle.

    """
    with open(input_subtitle, "r", encoding="utf-8") as file:
        content = file.read()
        input_subtitles = srt.parse(content)

        for sub in input_subtitles:
            translation = translate_string(
                client, sub.content, input_language, output_language
            )

            print(f"Subtitle: {sub.content}")
            print(f"Translation: {translation}\n")
            sub.content = translation

            yield sub


def compose_subtitle(subtitles: list, output_subtitle: str) -> None:
    """
    Composes a subtitle file from a list of subtitle objects and writes it to the specified output file.

    Args:
        subtitles (list): A list of subtitle objects.
        output_subtitle (str): The path to the output subtitle file.

    Returns:
        None
    """
    with open(output_subtitle, "w", encoding="utf-8") as file:
        content = srt.compose(subtitles)
        file.write(content)


client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
args = parse_arguments()
check_arguments()

subtitles = translate_subtitle(
    args.input_subtitle, args.input_language, args.output_language
)
compose_subtitle(subtitles, args.output_subtitle)
