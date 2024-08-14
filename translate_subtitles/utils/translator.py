""" Translate a given text from one language to another. """

import os
import json
import openai

from translate_subtitles.utils.models import TRANSLATION_MODEL


OPENAI_CLIENT = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def translate_string(text: str, input_language: str, output_language: str) -> str:
    """
    Translates the given text from the input language to the output language.

    Args:
        text (str): The text to be translated.
        input_language (str): The language of the input text.
        output_language (str): The language to translate the text into.

    Returns:
        str: The translated text.
    """
    prompt = (
        f"You will be provided with a table of sentences in {input_language}, "
        f"and your task is to translate it into {output_language}, "
        "using the following table format:\n"
        "\n"
        "| Original | Translated |\n"
        "| --- | --- |\n"
        "| Sentence 1 | Translation 1 |\n"
        "| Sentence 2 | Translation 2 |\n"
        "| Sentence 3 | Translation 3 |\n"
        "\n"
        "Provide the result keeping the original sentences in the 'Original' column "
        "and the translations in the 'Translated' column. Translate row by row."
    )

    response = OPENAI_CLIENT.chat.completions.create(
        model=TRANSLATION_MODEL.get("name"),
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": text},
        ],
    )

    response_json = json.loads(response.model_dump_json(indent=2))
    content = response_json["choices"][0]["message"]["content"]

    return content
