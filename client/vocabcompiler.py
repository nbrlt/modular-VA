# -*- coding: utf-8-*-
"""
Iterates over all the WORDS variables in the modules and creates a
vocabulary for the respective stt_engine if needed.
"""

import logging

from client import brain
from client import jasperpath

def get_phrases_from_module(module):
    """
    Gets phrases from a module.

    Arguments:
        module -- a module reference

    Returns:
        The list of phrases in this module.
    """
    return module.WORDS if hasattr(module, 'WORDS') else []


def get_keyword_phrases():
    """
    Gets the keyword phrases from the keywords file in the jasper data dir.

    Returns:
        A list of keyword phrases.
    """
    phrases = []

    with open(jasperpath.data('keyword_phrases'), mode="r") as f:
        for line in f:
            phrase = line.strip()
            if phrase:
                phrases.append(phrase)

    return phrases


def get_all_phrases():
    """
    Gets phrases from all modules.

    Returns:
        A list of phrases in all modules plus additional phrases passed to this
        function.
    """
    phrases = []

    modules = brain.Brain.get_modules()
    for module in modules:
        phrases.extend(get_phrases_from_module(module))

    return sorted(list(set(phrases)))
