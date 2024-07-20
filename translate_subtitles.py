"""Translate subtitles"""

import argparse
import json
import openai
import os
import srt


def parse_arguments():
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


def check_arguments():
    if not os.path.isfile(args.input_subtitle):
        print(f"File {args.input_subtitle} does not exist")
        exit(1)

        if os.path.isfile(args.output_subtitle):
            print(f"File {args.output_subtitle} already exists")
            exit(1)


def translate(client, text, input_language, output_language):
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


def translate_subtitle(input_subtitle, input_language, output_language):
    with open(input_subtitle, "r") as file:
        content = file.read()
        input_subtitles = srt.parse(content)

        for sub in input_subtitles:
            translation = translate(
                client, sub.content, args.input_language, args.output_language
            )

            print(f"Subtitle: {sub.content}")
            print(f"Translation: {translation}\n")
            sub.content = translation

            yield sub


def compose_subtitle(subtitles, output_subtitle):
    with open(output_subtitle, "w") as file:
        content = srt.compose(subtitles)
        file.write(content)


client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
args = parse_arguments()
check_arguments()

subtitles = translate_subtitle(
    args.input_subtitle, args.input_language, args.output_language
)
compose_subtitle(subtitles, args.output_subtitle)
