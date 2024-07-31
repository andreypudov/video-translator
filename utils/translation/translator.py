"""Translate a given text from one language to another."""

import json
import openai
import os

from utils.models import TRANSLATION_MODEL


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
        f"You will be provided with a sentence in {input_language}, "
        f"and your task is to translate it into {output_language} "
        "keeping line index at the beginning and line separation."
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
        temperature=0.6,
        top_p=0.8,
    )

    response_json = json.loads(response.model_dump_json(indent=2))
    content = response_json["choices"][0]["message"]["content"]

    return content
