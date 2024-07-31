""" This module contains the functions to validate a translation. """


def __decode_string(value: str) -> tuple[int, str]:
    """
    Decode a string in the format '::number:: string' and return a tuple of the decoded values.

    Args:
        value (str): The string to decode.

    Returns:
        tuple[int, str]: A tuple containing the decoded number and string.

    """
    parts = value.split("::")
    if len(parts) != 3:
        return -1, ""

    number = int(parts[1].strip())
    string = parts[2].strip()

    return number, string


def translation_is_valid(translation: str, entries_number: int) -> bool:
    """
    Check if the translation is valid.

    Args:
        subtitle_list (list[srt.Subtitle]): The list of subtitles.
        entries_number (int): The number of entries in the translation.

    Returns:
        bool: True if the translation is valid, False otherwise.
    """
    translation_list = translation.split("\n")[2:]

    if len(translation_list) != entries_number:
        return False

    for line in translation_list:
        columns = line.split("|")
        if len(columns) != 4:
            return False

        o_index, o_value = __decode_string(columns[1].strip())
        t_index, t_value = __decode_string(columns[2].strip())

        if o_index != t_index:
            return False

        if not o_value or not t_value:
            return False

    return True
