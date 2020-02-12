# -*- coding: utf-8 -*-

"""
tea Utils

This module provides utility function that are used within tea
that are also useful for external consumption.
"""
from os import getcwd

from yaml import safe_load


FILE_CONFIG = "src/tea/config.yml"
PATH = getcwd()


def parser_settings(file_name=FILE_CONFIG, path=PATH):
    """
    Parser of config file.

    Parameters:
    -----------
    file_name : str
        configuration file name to do parsing

    path : str
        configuration file path

    Return:
    -------
        dictionary containing the keys of configuration file
    """
    sections = {}
    try:
        with open(f"{path}/{file_name}", "r") as ymlfile:
            config = safe_load(ymlfile)
        sections = config
    except FileNotFoundError:
        print(f"{path}/{file_name}'not found.")
    return sections
