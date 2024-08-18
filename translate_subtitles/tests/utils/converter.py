""" This module contains functions to convert generators to lists. """

import collections.abc


def to_list(generator: collections.abc.Generator[collections.abc.Generator]) -> list:
    """
    Converts a generator of generators to a list of lists.

    Args:
        generator (collections.abc.Generator[collections.abc.Generator]): The generator to convert.

    Returns:
        list: The list containing the elements of the generator.
    """
    return [list(inner_generator) for inner_generator in generator]
